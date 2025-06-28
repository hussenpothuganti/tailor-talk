#!/bin/bash

# TailorTalk Startup Script
echo "Starting TailorTalk Application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Check if we're starting backend or frontend
if [ "$1" = "backend" ]; then
    echo "Starting Backend Server..."
    cd backend
    pip install -r requirements.txt
    python main.py
elif [ "$1" = "frontend" ]; then
    echo "Starting Frontend Server..."
    cd frontend
    pip install -r requirements.txt
    streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0
else
    echo "Usage: $0 [backend|frontend]"
    echo "Starting both services..."
    
    # Start backend in background
    cd backend
    pip install -r requirements.txt
    python main.py &
    BACKEND_PID=$!
    
    # Start frontend
    cd ../frontend
    pip install -r requirements.txt
    streamlit run app.py --server.port ${STREAMLIT_PORT:-8501} --server.address 0.0.0.0 &
    FRONTEND_PID=$!
    
    echo "Backend PID: $BACKEND_PID"
    echo "Frontend PID: $FRONTEND_PID"
    echo "Application started successfully!"
    echo "Backend: http://localhost:8000"
    echo "Frontend: http://localhost:8501"
    
    # Wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
fi

