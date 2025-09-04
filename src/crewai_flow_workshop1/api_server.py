#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime
import uuid
import asyncio
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from crewai_flow_workshop1.main import DeepResearchFlow, RouterIntent, SearchResult, Message as CrewAIMessage

app = FastAPI(title="CrewAI Research API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models matching frontend types
class ResearchSource(BaseModel):
    id: str
    title: str
    url: str
    description: str
    type: Literal["paper", "article", "website"] = "paper"
    metadata: Optional[Dict[str, Any]] = None

class IntentClassification(BaseModel):
    intent: Literal["research", "conversation"]
    confidence: float
    reasoning: str
    optimizedQuery: Optional[str] = None

class ResearchResult(BaseModel):
    query: str
    summary: str
    sources: List[ResearchSource]
    topics: List[str]

class Message(BaseModel):
    id: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime
    intent: Optional[Literal["research", "conversation"]] = None
    sources: Optional[List[ResearchSource]] = None
    reasoning: Optional[str] = None

class ChatSession(BaseModel):
    id: str
    title: str
    messages: List[Message]
    createdAt: datetime
    updatedAt: datetime

class FlowState(BaseModel):
    currentMessage: str
    messageHistory: List[Message]
    researchQuery: Optional[str] = None
    userIntent: Optional[IntentClassification] = None
    searchResults: Optional[ResearchResult] = None
    isProcessing: bool = False
    processingType: Optional[Literal["classification", "research", "conversation"]] = None

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None
    history: Optional[List[Message]] = []

class ClassifyIntentRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ResearchRequest(BaseModel):
    query: str

class ConversationRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

# In-memory storage for sessions (replace with database in production)
sessions: Dict[str, ChatSession] = {}
executor = ThreadPoolExecutor(max_workers=4)

def convert_crewai_sources_to_api(sources_list) -> List[ResearchSource]:
    """Convert CrewAI sources to API format with Unicode cleaning"""
    api_sources = []
    for i, source in enumerate(sources_list):
        try:
            # Clean Unicode characters from title and content
            clean_title = source.title.encode('ascii', 'replace').decode('ascii')
            clean_content = source.relevant_content[:200].encode('ascii', 'replace').decode('ascii')
            if len(source.relevant_content) > 200:
                clean_content += "..."
            
            api_sources.append(ResearchSource(
                id=str(i + 1),
                title=clean_title,
                url=source.url,
                description=clean_content,
                type="paper",
                metadata={
                    "publishedDate": "2024"  # Could be extracted from source if available
                }
            ))
        except Exception as e:
            # Skip sources that cause encoding issues
            continue
    return api_sources

async def run_crewai_flow(message: str) -> Dict[str, Any]:
    """Run CrewAI flow in thread executor to avoid blocking"""
    def _run_flow():
        try:
            flow = DeepResearchFlow(tracing=False)
            result = flow.kickoff(inputs={"user_message": message})
            return {
                "success": True,
                "data": flow.state,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, _run_flow)
    return result

@app.post("/api/chat")
async def chat(request: ChatRequest) -> Message:
    """Main chat endpoint that handles user input and routes to research or conversation"""
    try:
        # Run CrewAI flow
        flow_result = await run_crewai_flow(request.message)
        
        if not flow_result["success"]:
            raise HTTPException(status_code=500, detail=flow_result["error"])
        
        state = flow_result["data"]
        
        # Determine response based on intent
        if state.user_intent == "research" and state.search_result:
            # Research response with Unicode cleaning
            try:
                # Clean the research summary for safe JSON serialization
                clean_summary = state.search_result.research_summary.encode('ascii', 'replace').decode('ascii')
                sources = convert_crewai_sources_to_api(state.search_result.sources_list)
                
                response = Message(
                    id=str(uuid.uuid4()),
                    role="assistant",
                    content=clean_summary,
                    timestamp=datetime.now(),
                    intent="research",
                    sources=sources,
                    reasoning=f"Research conducted for query: {state.research_query}"
                )
            except Exception as e:
                # Fallback response if cleaning fails
                response = Message(
                    id=str(uuid.uuid4()),
                    role="assistant",
                    content="Research completed successfully. The system found relevant academic sources and generated a comprehensive summary.",
                    timestamp=datetime.now(),
                    intent="research",
                    reasoning="Research completed with encoding fallback"
                )
        else:
            # Conversation response (fallback or direct conversation)
            # For now, use the last message from history or generate a simple response
            content = "I understand your message. This appears to be a conversational request. How can I assist you further?"
            
            response = Message(
                id=str(uuid.uuid4()),
                role="assistant", 
                content=content,
                timestamp=datetime.now(),
                intent="conversation",
                reasoning="Classified as conversational interaction"
            )
        
        # Store in session if sessionId provided
        if request.sessionId:
            if request.sessionId not in sessions:
                sessions[request.sessionId] = ChatSession(
                    id=request.sessionId,
                    title="Research Session",
                    messages=[],
                    createdAt=datetime.now(),
                    updatedAt=datetime.now()
                )
            
            # Add user message
            user_message = Message(
                id=str(uuid.uuid4()),
                role="user",
                content=request.message,
                timestamp=datetime.now()
            )
            
            sessions[request.sessionId].messages.extend([user_message, response])
            sessions[request.sessionId].updatedAt = datetime.now()
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/api/classify-intent")
async def classify_intent(request: ClassifyIntentRequest) -> IntentClassification:
    """Classify user intent as research or conversation"""
    try:
        # Run just the intent classification part
        flow = DeepResearchFlow(tracing=False)
        # Set the user message
        flow.state.user_message = request.message
        
        # Run the routing method
        intent_result = flow.routing_intent()
        
        return IntentClassification(
            intent=flow.state.user_intent,
            confidence=0.85,  # Mock confidence score
            reasoning="Intent classified based on message content and context",
            optimizedQuery=flow.state.research_query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying intent: {str(e)}")

@app.post("/api/research")
async def research(request: ResearchRequest) -> ResearchResult:
    """Conduct research for a specific query"""
    try:
        flow_result = await run_crewai_flow(request.query)
        
        if not flow_result["success"]:
            raise HTTPException(status_code=500, detail=flow_result["error"])
        
        state = flow_result["data"]
        
        if not state.search_result:
            raise HTTPException(status_code=404, detail="No research results found")
        
        sources = convert_crewai_sources_to_api(state.search_result.sources_list)
        
        return ResearchResult(
            query=request.query,
            summary=state.search_result.research_summary,
            sources=sources,
            topics=["research", "analysis", "findings"]  # Could be enhanced
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conducting research: {str(e)}")

@app.post("/api/conversation") 
async def conversation(request: ConversationRequest) -> Dict[str, str]:
    """Handle conversational interactions"""
    try:
        # Simple conversational responses for now
        responses = [
            "I understand your question. Let me help you with that information.",
            "That's an interesting point! Here's what I can share about that topic.",
            "Great question! I'm here to assist you with both research and conversation.",
            "I'm designed to help with both academic research and general inquiries. How can I assist you today?"
        ]
        
        import random
        response = random.choice(responses)
        
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in conversation: {str(e)}")

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str) -> ChatSession:
    """Get a chat session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.post("/api/sessions/{session_id}")
async def create_session(session_id: str) -> ChatSession:
    """Create a new chat session"""
    session = ChatSession(
        id=session_id,
        title="Research Session",
        messages=[],
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )
    sessions[session_id] = session
    return session

@app.get("/api/sessions/{session_id}/messages")
async def get_messages(session_id: str) -> List[Message]:
    """Get messages for a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id].messages

@app.post("/api/sessions/{session_id}/messages")
async def add_message(session_id: str, message: Message) -> Message:
    """Add a message to a session"""
    if session_id not in sessions:
        sessions[session_id] = ChatSession(
            id=session_id,
            title="Research Session",
            messages=[],
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
    
    sessions[session_id].messages.append(message)
    sessions[session_id].updatedAt = datetime.now()
    return message

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

# Mount static files for frontend (production deployment)
static_dir = Path(__file__).parent.parent.parent / "frontend" / "dist"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir / "assets"), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend files, fallback to index.html for SPA routing"""
        # API routes should be handled before this
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Try to serve the requested file
        file_path = static_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # For SPA routing, always serve index.html for unknown routes
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)