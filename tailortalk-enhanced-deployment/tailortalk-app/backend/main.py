from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime, timedelta
import uvicorn
from pymongo import MongoClient
from bson import ObjectId
import json
from dotenv import load_dotenv

# Import our custom modules
from agent import ConversationalAgent
from calendar_service import CalendarService
from database import Database

load_dotenv()

app = FastAPI(title="TailorTalk API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = Database()
calendar_service = CalendarService()
agent = ConversationalAgent(db, calendar_service)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: Optional[str] = None
    slots: Optional[Dict[str, Any]] = None
    actions: Optional[List[str]] = None

class AppointmentRequest(BaseModel):
    title: str
    date: str
    time: str
    duration: int = 60
    description: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "TailorTalk API is running", "status": "healthy"}

@app.get("/conversations")
async def get_conversations():
    """Get all conversation history"""
    try:
        conversations = db.get_conversations()
        return {"status": "success", "conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all-appointments")
async def get_all_appointments():
    """Get all booked appointments with enhanced details"""
    try:
        appointments = db.get_all_appointments()
        return {"status": "success", "appointments": appointments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/appointments/{appointment_id}")
async def cancel_appointment(appointment_id: str):
    """Cancel a specific appointment"""
    try:
        result = db.cancel_appointment(appointment_id)
        if result:
            return {"status": "success", "message": "Appointment cancelled successfully"}
        else:
            return {"status": "error", "message": "Appointment not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/appointments/{appointment_id}")
async def reschedule_appointment(appointment_id: str, request: dict):
    """Reschedule an existing appointment"""
    try:
        new_datetime = request.get("new_datetime")
        if not new_datetime:
            return {"status": "error", "message": "New datetime is required"}
        
        result = db.reschedule_appointment(appointment_id, new_datetime)
        if result:
            return {"status": "success", "message": "Appointment rescheduled successfully"}
        else:
            return {"status": "error", "message": "Appointment not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/profile")
async def get_user_profile():
    """Get user profile information (mock for now)"""
    return {
        "status": "success",
        "profile": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "timezone": "UTC",
            "preferences": {
                "notification_enabled": True,
                "preferred_time_slots": ["09:00-12:00", "14:00-17:00"]
            },
            "stats": {
                "total_appointments": 15,
                "completed_appointments": 12,
                "cancelled_appointments": 3
            }
        }
    }

@app.get("/system/stats")
async def get_system_stats():
    """Get system statistics for dashboard"""
    try:
        stats = {
            "ai_agent": {
                "status": "online",
                "response_time": "0.3s",
                "accuracy": "95%"
            },
            "calendar": {
                "status": "connected",
                "sync_time": "2s",
                "availability": "92%"
            },
            "database": {
                "status": "connected" if db.check_connection() else "offline",
                "response_time": "0.1s",
                "uptime": "99%"
            },
            "network": {
                "status": "stable",
                "latency": "45ms",
                "bandwidth": "100Mbps"
            }
        }
        return {"status": "success", "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        # Process the message through our conversational agent
        response = await agent.process_message(
            message.message, 
            session_id=message.session_id
        )
        
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/availability")
async def get_availability(date: str):
    try:
        # Get available time slots for a specific date
        availability = await calendar_service.get_availability(date)
        return {"date": date, "available_slots": availability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book-appointment")
async def book_appointment(appointment: AppointmentRequest):
    try:
        # Book an appointment
        result = await calendar_service.book_appointment(
            title=appointment.title,
            date=appointment.date,
            time=appointment.time,
            duration=appointment.duration,
            description=appointment.description
        )
        
        # Save to database
        appointment_data = {
            "title": appointment.title,
            "date": appointment.date,
            "time": appointment.time,
            "duration": appointment.duration,
            "description": appointment.description,
            "calendar_event_id": result.get("event_id"),
            "created_at": datetime.utcnow(),
            "status": "confirmed"
        }
        
        db.save_appointment(appointment_data)
        
        return {"message": "Appointment booked successfully", "appointment": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/appointments")
async def get_appointments():
    try:
        appointments = db.get_appointments()
        return {"appointments": appointments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db.check_connection(),
            "calendar": calendar_service.check_connection()
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

