from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
import os
import json
from typing import List, Dict, Any, Optional
import pickle

class CalendarService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.service = None
        self.credentials = None
        self.setup_service()
    
    def setup_service(self):
        """Set up Google Calendar service with authentication"""
        try:
            # For now, we'll create a mock service since we don't have OAuth setup
            # In production, this would handle proper OAuth flow
            print("Calendar service initialized (mock mode)")
            self.service = "mock_service"
        except Exception as e:
            print(f"Error setting up calendar service: {e}")
            self.service = None
    
    def check_connection(self) -> bool:
        """Check if calendar service is connected"""
        return self.service is not None
    
    async def get_availability(self, date: str) -> List[str]:
        """Get available time slots for a specific date"""
        try:
            # Mock implementation - in production this would query actual calendar
            available_slots = [
                "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"
            ]
            
            # Filter out past times if date is today
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.now().date()
            
            if target_date == today:
                current_hour = datetime.now().hour
                available_slots = [slot for slot in available_slots 
                                 if int(slot.split(":")[0]) > current_hour]
            
            return available_slots
        except Exception as e:
            print(f"Error getting availability: {e}")
            return []
    
    async def book_appointment(self, title: str, date: str, time: str, 
                             duration: int = 60, description: str = None) -> Dict[str, Any]:
        """Book an appointment on Google Calendar"""
        try:
            # Mock implementation - in production this would create actual calendar event
            event_id = f"mock_event_{datetime.now().timestamp()}"
            
            # Parse date and time
            start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_datetime = start_datetime + timedelta(minutes=duration)
            
            event_data = {
                "event_id": event_id,
                "title": title,
                "start": start_datetime.isoformat(),
                "end": end_datetime.isoformat(),
                "description": description or "",
                "status": "confirmed"
            }
            
            print(f"Mock appointment booked: {title} on {date} at {time}")
            return event_data
            
        except Exception as e:
            print(f"Error booking appointment: {e}")
            raise e
    
    async def get_events(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get calendar events within date range"""
        try:
            # Mock implementation
            mock_events = [
                {
                    "id": "mock_event_1",
                    "title": "Team Meeting",
                    "start": "2024-01-15T10:00:00",
                    "end": "2024-01-15T11:00:00",
                    "description": "Weekly team sync"
                },
                {
                    "id": "mock_event_2", 
                    "title": "Client Call",
                    "start": "2024-01-15T14:00:00",
                    "end": "2024-01-15T15:00:00",
                    "description": "Project discussion"
                }
            ]
            
            return mock_events
        except Exception as e:
            print(f"Error getting events: {e}")
            return []
    
    async def cancel_appointment(self, event_id: str) -> bool:
        """Cancel an appointment"""
        try:
            # Mock implementation
            print(f"Mock appointment cancelled: {event_id}")
            return True
        except Exception as e:
            print(f"Error cancelling appointment: {e}")
            return False
    
    def get_next_available_slots(self, days_ahead: int = 7) -> List[Dict[str, str]]:
        """Get next available time slots for the upcoming days"""
        try:
            slots = []
            today = datetime.now().date()
            
            for i in range(1, days_ahead + 1):
                target_date = today + timedelta(days=i)
                # Skip weekends for business appointments
                if target_date.weekday() < 5:  # Monday = 0, Friday = 4
                    date_str = target_date.strftime("%Y-%m-%d")
                    available_times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
                    
                    for time_slot in available_times:
                        slots.append({
                            "date": date_str,
                            "time": time_slot,
                            "display": f"{target_date.strftime('%A, %B %d')} at {time_slot}"
                        })
            
            return slots[:10]  # Return first 10 available slots
        except Exception as e:
            print(f"Error getting next available slots: {e}")
            return []

