from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        # MongoDB connection string provided by user
        self.connection_string = "mongodb+srv://shaikmahammadhussain835:pgBZgM9gYvXmLzw1@hussain.vo52sy7.mongodb.net/?retryWrites=true&w=majority&appName=Hussain"
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        try:
            # Add SSL configuration to handle connection issues
            self.client = MongoClient(
                self.connection_string,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            self.db = self.client.tailortalk
            # Test connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            print("Running in offline mode - using mock database")
            self.client = None
            self.db = None
    
    def check_connection(self) -> bool:
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
            return False
        except:
            return False
    
    def save_conversation(self, session_id: str, message: str, response: str, intent: str = None, slots: Dict = None):
        """Save conversation to database"""
        try:
            if not self.db:
                print(f"Mock save conversation: {session_id} - {message[:50]}...")
                return "mock_id"
                
            conversation_data = {
                "session_id": session_id,
                "user_message": message,
                "agent_response": response,
                "intent": intent,
                "slots": slots or {},
                "timestamp": datetime.utcnow(),
                "created_at": datetime.utcnow()
            }
            
            result = self.db.conversations.insert_one(conversation_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return None
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a session"""
        try:
            if not self.db:
                return []  # Return empty for mock mode
                
            conversations = list(
                self.db.conversations
                .find({"session_id": session_id})
                .sort("timestamp", -1)
                .limit(limit)
            )
            
            # Convert ObjectId to string for JSON serialization
            for conv in conversations:
                conv["_id"] = str(conv["_id"])
            
            return conversations[::-1]  # Return in chronological order
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def save_appointment(self, appointment_data: Dict) -> str:
        """Save appointment to database"""
        try:
            if not self.db:
                print(f"Mock save appointment: {appointment_data.get('title', 'Appointment')}")
                return "mock_appointment_id"
                
            appointment_data["created_at"] = datetime.utcnow()
            result = self.db.appointments.insert_one(appointment_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return None
    
    def get_appointments(self, limit: int = 50) -> List[Dict]:
        """Get all appointments"""
        try:
            if not self.db:
                # Return mock appointments
                return [
                    {
                        "_id": "mock_1",
                        "title": "Sample Appointment",
                        "date": "2024-01-15",
                        "time": "10:00",
                        "duration": 60,
                        "status": "confirmed",
                        "created_at": datetime.utcnow()
                    }
                ]
                
            appointments = list(
                self.db.appointments
                .find()
                .sort("created_at", -1)
                .limit(limit)
            )
            
            # Convert ObjectId to string for JSON serialization
            for appointment in appointments:
                appointment["_id"] = str(appointment["_id"])
            
            return appointments
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []
    
    def get_appointment_by_id(self, appointment_id: str) -> Optional[Dict]:
        """Get appointment by ID"""
        try:
            appointment = self.db.appointments.find_one({"_id": ObjectId(appointment_id)})
            if appointment:
                appointment["_id"] = str(appointment["_id"])
            return appointment
        except Exception as e:
            print(f"Error getting appointment: {e}")
            return None
    
    def update_appointment_status(self, appointment_id: str, status: str) -> bool:
        """Update appointment status"""
        try:
            result = self.db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": {"status": status, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating appointment status: {e}")
            return False
    
    def save_user_session(self, session_id: str, user_data: Dict) -> str:
        """Save user session data"""
        try:
            session_data = {
                "session_id": session_id,
                "user_data": user_data,
                "created_at": datetime.utcnow(),
                "last_activity": datetime.utcnow()
            }
            
            # Upsert session data
            result = self.db.user_sessions.replace_one(
                {"session_id": session_id},
                session_data,
                upsert=True
            )
            
            return session_id
        except Exception as e:
            print(f"Error saving user session: {e}")
            return None
    
    def get_user_session(self, session_id: str) -> Optional[Dict]:
        """Get user session data"""
        try:
            session = self.db.user_sessions.find_one({"session_id": session_id})
            if session:
                session["_id"] = str(session["_id"])
            return session
        except Exception as e:
            print(f"Error getting user session: {e}")
            return None
    
    def get_conversations(self):
        """Get all conversation history"""
        try:
            if not self.db:
                # Return mock conversations
                return [
                    {
                        "id": "conv_001",
                        "session_id": "session_123",
                        "messages": [
                            {"role": "user", "content": "Hello, I want to book an appointment", "timestamp": "2025-06-27T10:00:00Z"},
                            {"role": "assistant", "content": "Hello! I'm TailorTalk, your AI assistant for booking appointments. How can I help you today?", "timestamp": "2025-06-27T10:00:01Z"}
                        ],
                        "created_at": "2025-06-27T10:00:00Z"
                    },
                    {
                        "id": "conv_002",
                        "session_id": "session_124",
                        "messages": [
                            {"role": "user", "content": "I want to schedule a meeting for tomorrow at 2 PM", "timestamp": "2025-06-27T11:00:00Z"},
                            {"role": "assistant", "content": "I'd be happy to help you schedule a meeting for tomorrow at 2 PM. Let me check availability for you.", "timestamp": "2025-06-27T11:00:01Z"}
                        ],
                        "created_at": "2025-06-27T11:00:00Z"
                    }
                ]
            
            conversations = list(self.db.conversations.find({}).sort("created_at", -1))
            for conv in conversations:
                conv["_id"] = str(conv["_id"])
                conv["id"] = str(conv["_id"])
            return conversations
        except Exception as e:
            print(f"Error fetching conversations: {e}")
            return []

    def get_all_appointments(self):
        """Get all booked appointments with enhanced details"""
        try:
            if not self.db:
                # Return mock appointments with enhanced details
                return [
                    {
                        "id": "apt_001",
                        "title": "Team Meeting",
                        "date": "2025-06-28",
                        "time": "14:00",
                        "duration": 60,
                        "description": "Weekly team sync meeting",
                        "status": "confirmed",
                        "created_at": "2025-06-27T10:30:00Z"
                    },
                    {
                        "id": "apt_002",
                        "title": "Client Call",
                        "date": "2025-06-29",
                        "time": "10:00",
                        "duration": 30,
                        "description": "Project discussion with client",
                        "status": "confirmed",
                        "created_at": "2025-06-27T11:15:00Z"
                    },
                    {
                        "id": "apt_003",
                        "title": "Code Review",
                        "date": "2025-06-30",
                        "time": "15:00",
                        "duration": 45,
                        "description": "Review new feature implementation",
                        "status": "confirmed",
                        "created_at": "2025-06-27T12:00:00Z"
                    }
                ]
            
            appointments = list(self.db.appointments.find({}).sort("created_at", -1))
            for apt in appointments:
                apt["_id"] = str(apt["_id"])
                apt["id"] = str(apt["_id"])
            return appointments
        except Exception as e:
            print(f"Error fetching appointments: {e}")
            return []

    def cancel_appointment(self, appointment_id: str):
        """Cancel a specific appointment"""
        try:
            if not self.db:
                # In mock mode, just return success
                print(f"Mock: Cancelling appointment {appointment_id}")
                return True
            
            result = self.db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": {"status": "cancelled", "cancelled_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error cancelling appointment: {e}")
            return False

    def reschedule_appointment(self, appointment_id: str, new_datetime: str):
        """Reschedule an existing appointment"""
        try:
            if not self.db:
                # In mock mode, just return success
                print(f"Mock: Rescheduling appointment {appointment_id} to {new_datetime}")
                return True
            
            # Parse the new datetime
            new_dt = datetime.fromisoformat(new_datetime.replace('Z', '+00:00'))
            
            result = self.db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {
                    "$set": {
                        "date": new_dt.strftime("%Y-%m-%d"),
                        "time": new_dt.strftime("%H:%M"),
                        "rescheduled_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error rescheduling appointment: {e}")
            return False

    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()

