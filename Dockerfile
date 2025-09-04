# Multi-stage Dockerfile for CrewAI Research Application
FROM node:18-alpine AS frontend-builder

# Build frontend
WORKDIR /app/frontend
COPY frontend/synapse-research/package*.json ./
RUN npm ci
COPY frontend/synapse-research/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster Python package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy Python dependencies and source code
COPY pyproject.toml ./
COPY src/ ./src/
COPY start_api.py ./

# Install Python dependencies directly from pyproject.toml
RUN uv pip install --system -e .

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create startup script that serves both frontend and backend on port 8000
RUN echo '#!/bin/bash\n\
# Start the FastAPI server which will also serve the frontend\n\
cd /app\n\
uv run uvicorn src.crewai_flow_workshop1.api_server:app --host 0.0.0.0 --port ${PORT:-8000}\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port 8000 (AWS App Runner will map this)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start both services
CMD ["/app/start.sh"]