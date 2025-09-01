from typing import List, Literal
from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    role: Literal["user", "assistant"] = "user" 
    content: str
    timestamp: datetime = datetime.now()


class ConversationHandler(BaseModel):
    """Handles conversation message history and related operations"""
    messages: List[Message] = []

    def add_message(self, role: str, content: str) -> Message:
        """Add a message to the conversation history"""
        new_message = Message(role=role, content=content)
        self.messages.append(new_message)
        return new_message
    
    def extend_messages(self, messages: List[Message]):
        """Extend conversation history with multiple messages"""
        self.messages.extend(messages)
    
    def get_messages(self) -> List[Message]:
        """Get the current conversation history"""
        return self.messages
    
    def get_latest_message(self) -> Message | None:
        """Get the most recent message"""
        return self.messages[-1] if self.messages else None
    
    def get_messages_by_role(self, role: str) -> List[Message]:
        """Get all messages from a specific role"""
        return [msg for msg in self.messages if msg.role == role]
    
    def clear_history(self):
        """Clear all messages from history"""
        self.messages.clear()
    
    def print_conversation(self):
        """Print the conversation history in a readable format"""
        print("\n=== Conversation History ===")
        if not self.messages:
            print("No messages in conversation history.")
        else:
            for message in self.messages:
                timestamp_str = message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp_str}] {message.role}: {message.content}")
        print("=" * 30 + "\n")
    
    def to_dict(self) -> dict:
        """Convert conversation history to dictionary"""
        return self.model_dump()
    
    def to_json(self, indent: int = 2) -> str:
        """Convert conversation history to JSON string"""
        return self.model_dump_json(indent=indent)
    
    def get_conversation_summary(self) -> dict:
        """Get a summary of the conversation"""
        user_messages = self.get_messages_by_role("user")
        assistant_messages = self.get_messages_by_role("assistant")
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "first_message_time": self.messages[0].timestamp if self.messages else None,
            "last_message_time": self.messages[-1].timestamp if self.messages else None
        }
