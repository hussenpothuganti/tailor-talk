import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
from database import Database
from calendar_service import CalendarService

class ConversationalAgent:
    def __init__(self, database: Database, calendar_service: CalendarService):
        self.db = database
        self.calendar_service = calendar_service
        self.conversation_states = {}
        
        # Intent patterns
        self.intent_patterns = {
            'greeting': [
                r'hello|hi|hey|good morning|good afternoon|good evening',
                r'start|begin|help'
            ],
            'book_appointment': [
                r'book|schedule|appointment|meeting|call',
                r'want to schedule|need to book|set up a meeting',
                r'available|free time|time slot'
            ],
            'check_availability': [
                r'available|free|when|what time|schedule',
                r'do you have|any time|free time'
            ],
            'confirm_booking': [
                r'yes|confirm|book it|that works|sounds good',
                r'perfect|great|ok|okay'
            ],
            'cancel_decline': [
                r'no|cancel|not now|maybe later',
                r'different time|another time'
            ]
        }
        
        # Slot extraction patterns
        self.slot_patterns = {
            'date': [
                r'tomorrow|today|next week|this week',
                r'monday|tuesday|wednesday|thursday|friday|saturday|sunday',
                r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
                r'\d{1,2}th|\d{1,2}st|\d{1,2}nd|\d{1,2}rd'
            ],
            'time': [
                r'\d{1,2}:\d{2}',
                r'\d{1,2}\s*(am|pm|AM|PM)',
                r'morning|afternoon|evening|noon'
            ],
            'duration': [
                r'\d+\s*hour|hour',
                r'\d+\s*minute|minute',
                r'30 min|1 hour|2 hour'
            ]
        }
    
    async def process_message(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """Process user message and return agent response"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create conversation state
        if session_id not in self.conversation_states:
            self.conversation_states[session_id] = {
                'state': 'initial',
                'slots': {},
                'context': []
            }
        
        state = self.conversation_states[session_id]
        
        # Extract intent and slots
        intent = self.extract_intent(message)
        slots = self.extract_slots(message)
        
        # Update slots
        state['slots'].update(slots)
        
        # Add to context
        state['context'].append({
            'user_message': message,
            'intent': intent,
            'slots': slots,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Generate response based on current state and intent
        response_data = await self.generate_response(state, intent, message, session_id)
        
        # Save conversation to database
        self.db.save_conversation(
            session_id=session_id,
            message=message,
            response=response_data['response'],
            intent=intent,
            slots=slots
        )
        
        return response_data
    
    def extract_intent(self, message: str) -> str:
        """Extract intent from user message"""
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'unknown'
    
    def extract_slots(self, message: str) -> Dict[str, Any]:
        """Extract slots (entities) from user message"""
        slots = {}
        message_lower = message.lower()
        
        # Extract date
        for pattern in self.slot_patterns['date']:
            match = re.search(pattern, message_lower)
            if match:
                date_text = match.group()
                parsed_date = self.parse_date(date_text)
                if parsed_date:
                    slots['date'] = parsed_date
                    break
        
        # Extract time
        for pattern in self.slot_patterns['time']:
            match = re.search(pattern, message_lower)
            if match:
                time_text = match.group()
                parsed_time = self.parse_time(time_text)
                if parsed_time:
                    slots['time'] = parsed_time
                    break
        
        # Extract duration
        for pattern in self.slot_patterns['duration']:
            match = re.search(pattern, message_lower)
            if match:
                duration_text = match.group()
                parsed_duration = self.parse_duration(duration_text)
                if parsed_duration:
                    slots['duration'] = parsed_duration
                    break
        
        return slots
    
    def parse_date(self, date_text: str) -> Optional[str]:
        """Parse date text to standard format"""
        today = datetime.now().date()
        
        if 'today' in date_text:
            return today.strftime('%Y-%m-%d')
        elif 'tomorrow' in date_text:
            return (today + timedelta(days=1)).strftime('%Y-%m-%d')
        elif 'next week' in date_text:
            return (today + timedelta(days=7)).strftime('%Y-%m-%d')
        elif any(day in date_text for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']):
            # Find next occurrence of the day
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for i, day in enumerate(days):
                if day in date_text:
                    days_ahead = (i - today.weekday()) % 7
                    if days_ahead == 0:
                        days_ahead = 7  # Next week if it's the same day
                    target_date = today + timedelta(days=days_ahead)
                    return target_date.strftime('%Y-%m-%d')
        
        return None
    
    def parse_time(self, time_text: str) -> Optional[str]:
        """Parse time text to standard format"""
        if ':' in time_text:
            return time_text
        elif 'morning' in time_text:
            return '09:00'
        elif 'afternoon' in time_text:
            return '14:00'
        elif 'evening' in time_text:
            return '17:00'
        elif 'noon' in time_text:
            return '12:00'
        
        return None
    
    def parse_duration(self, duration_text: str) -> Optional[int]:
        """Parse duration text to minutes"""
        if 'hour' in duration_text:
            if '2' in duration_text:
                return 120
            else:
                return 60
        elif '30' in duration_text:
            return 30
        
        return 60  # Default 1 hour
    
    async def generate_response(self, state: Dict, intent: str, message: str, session_id: str) -> Dict[str, Any]:
        """Generate appropriate response based on state and intent"""
        
        if intent == 'greeting':
            response = "Hello! I'm TailorTalk, your AI assistant for booking appointments. How can I help you today?"
            state['state'] = 'ready'
            
        elif intent == 'book_appointment':
            if 'date' in state['slots'] and 'time' in state['slots']:
                # We have both date and time, confirm booking
                date = state['slots']['date']
                time = state['slots']['time']
                duration = state['slots'].get('duration', 60)
                
                response = f"Perfect! I can book an appointment for {date} at {time} for {duration} minutes. Shall I confirm this booking?"
                state['state'] = 'confirming'
                
            elif 'date' in state['slots']:
                # We have date, ask for time
                date = state['slots']['date']
                available_slots = await self.calendar_service.get_availability(date)
                
                if available_slots:
                    slots_text = ', '.join(available_slots)
                    response = f"Great! For {date}, I have these time slots available: {slots_text}. Which time works best for you?"
                else:
                    response = f"I don't have any available slots for {date}. Would you like to try a different date?"
                
                state['state'] = 'collecting_time'
                
            else:
                # Ask for date
                next_slots = self.calendar_service.get_next_available_slots()
                if next_slots:
                    suggestions = next_slots[:3]
                    suggestion_text = ', '.join([slot['display'] for slot in suggestions])
                    response = f"I'd be happy to help you book an appointment! Here are some upcoming available slots: {suggestion_text}. Or let me know your preferred date and time."
                else:
                    response = "I'd be happy to help you book an appointment! What date and time would work best for you?"
                
                state['state'] = 'collecting_details'
        
        elif intent == 'check_availability':
            if 'date' in state['slots']:
                date = state['slots']['date']
                available_slots = await self.calendar_service.get_availability(date)
                
                if available_slots:
                    slots_text = ', '.join(available_slots)
                    response = f"For {date}, I have these time slots available: {slots_text}. Would you like to book one of these?"
                else:
                    response = f"I don't have any available slots for {date}. Would you like to check a different date?"
            else:
                response = "What date would you like to check availability for?"
            
            state['state'] = 'showing_availability'
        
        elif intent == 'confirm_booking' and state['state'] == 'confirming':
            # Book the appointment
            try:
                date = state['slots']['date']
                time = state['slots']['time']
                duration = state['slots'].get('duration', 60)
                title = "Appointment"
                
                booking_result = await self.calendar_service.book_appointment(
                    title=title,
                    date=date,
                    time=time,
                    duration=duration,
                    description="Booked via TailorTalk"
                )
                
                response = f"Excellent! Your appointment has been confirmed for {date} at {time}. You'll receive a confirmation shortly."
                state['state'] = 'completed'
                
            except Exception as e:
                response = f"I'm sorry, there was an issue booking your appointment. Please try again or contact support."
                state['state'] = 'error'
        
        elif intent == 'cancel_decline':
            response = "No problem! Let me know if you'd like to schedule for a different time or if there's anything else I can help you with."
            state['state'] = 'ready'
        
        else:
            # Default response for unknown intents
            if state['state'] == 'initial' or state['state'] == 'ready':
                response = "I can help you book appointments and check availability. Would you like to schedule a meeting or check available time slots?"
            else:
                response = "I'm not sure I understand. Could you please clarify what you'd like to do?"
        
        return {
            'response': response,
            'session_id': session_id,
            'intent': intent,
            'slots': state['slots'],
            'actions': self.get_suggested_actions(state, intent)
        }
    
    def get_suggested_actions(self, state: Dict, intent: str) -> List[str]:
        """Get suggested actions based on current state"""
        actions = []
        
        if state['state'] == 'collecting_details':
            actions = ['Check availability', 'Book appointment']
        elif state['state'] == 'collecting_time':
            actions = ['Select time slot', 'Check different date']
        elif state['state'] == 'confirming':
            actions = ['Confirm booking', 'Change details']
        elif state['state'] == 'completed':
            actions = ['Book another appointment', 'View appointments']
        else:
            actions = ['Book appointment', 'Check availability']
        
        return actions

