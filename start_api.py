#!/usr/bin/env python3

"""
Startup script for the CrewAI Research API server
"""

import uvicorn
from src.crewai_flow_workshop1.api_server import app

if __name__ == "__main__":
    print("Starting CrewAI Research API Server...")
    print("API will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print()
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )