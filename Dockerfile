# Multi-stage Dockerfile for CrewAI Research Application
FROM node:18-alpine as frontend-builder

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

# Copy Python dependencies
COPY pyproject.toml ./
COPY uv.lock* ./

# Install Python dependencies
RUN uv sync --no-dev

# Copy application code
COPY src/ ./src/
COPY start_api.py ./

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create a simple static file server for frontend
RUN echo '#!/bin/bash\n\
# Start backend API\n\
uv run python start_api.py &\n\
\n\
# Start simple HTTP server for frontend on port 3000\n\
cd frontend/dist && python -m http.server 3000 &\n\
\n\
# Wait for any process to exit\n\
wait -n\n\
\n\
# Exit with status of process that exited first\n\
exit $?' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start both services
CMD ["/app/start.sh"]