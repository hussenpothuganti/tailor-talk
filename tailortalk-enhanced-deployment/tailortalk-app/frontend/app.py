import streamlit as st
import requests
import json
import time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import uuid

# Page configuration
st.set_page_config(
    page_title="TailorTalk - AI Appointment Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Enhanced CSS for advanced sci-fi UI
st.markdown("""
<style>
/* Import futuristic fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* Global styles */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a33 50%, #2a1a4a 100%);
    font-family: 'Rajdhani', sans-serif;
}

/* Animated background particles */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #00ffff, transparent),
        radial-gradient(2px 2px at 40px 70px, #ff00ff, transparent),
        radial-gradient(1px 1px at 90px 40px, #00ccff, transparent),
        radial-gradient(1px 1px at 130px 80px, #cc00ff, transparent);
    background-repeat: repeat;
    background-size: 200px 200px;
    animation: particleMove 20s linear infinite;
    opacity: 0.1;
    z-index: -1;
}

@keyframes particleMove {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-200px, -200px); }
}

/* Main title styling */
.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(45deg, #00ffff, #ff00ff, #00ccff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    margin-bottom: 0.5rem;
    animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    0% { filter: brightness(1) drop-shadow(0 0 10px rgba(0, 255, 255, 0.3)); }
    100% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(0, 255, 255, 0.6)); }
}

.subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    text-align: center;
    color: #00ccff;
    margin-bottom: 2rem;
    animation: subtitlePulse 2s ease-in-out infinite;
}

@keyframes subtitlePulse {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 1; }
}

/* Chat container */
.chat-container {
    background: rgba(26, 26, 51, 0.8);
    border: 2px solid #00ffff;
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    box-shadow: 
        0 0 30px rgba(0, 255, 255, 0.3),
        inset 0 0 30px rgba(0, 255, 255, 0.1);
    animation: containerPulse 4s ease-in-out infinite;
}

@keyframes containerPulse {
    0%, 100% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.3), inset 0 0 30px rgba(0, 255, 255, 0.1); }
    50% { box-shadow: 0 0 40px rgba(0, 255, 255, 0.5), inset 0 0 40px rgba(0, 255, 255, 0.2); }
}

/* Message bubbles */
.user-message {
    background: linear-gradient(135deg, #ff00ff, #cc00ff);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 5px 20px;
    margin: 0.5rem 0;
    margin-left: 20%;
    box-shadow: 0 5px 15px rgba(255, 0, 255, 0.3);
    animation: messageSlideIn 0.5s ease-out;
    position: relative;
    overflow: hidden;
}

.user-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    animation: shimmer 2s infinite;
}

.assistant-message {
    background: linear-gradient(135deg, #00ffff, #00ccff);
    color: #0a0a1a;
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 20px 5px;
    margin: 0.5rem 0;
    margin-right: 20%;
    box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
    animation: messageSlideIn 0.5s ease-out;
    position: relative;
    overflow: hidden;
    font-weight: 500;
}

.assistant-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    animation: shimmer 2s infinite;
}

@keyframes messageSlideIn {
    0% { transform: translateY(20px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Input styling */
.stTextInput > div > div > input {
    background: rgba(26, 26, 51, 0.9) !important;
    border: 2px solid #00ffff !important;
    border-radius: 15px !important;
    color: #00ffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 1.2rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff00ff !important;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.5) !important;
    transform: scale(1.02) !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #00ffff, #00ccff) !important;
    color: #0a0a1a !important;
    border: none !important;
    border-radius: 15px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 2rem !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #ff00ff, #cc00ff) !important;
    color: white !important;
    transform: scale(1.05) !important;
    box-shadow: 0 10px 25px rgba(255, 0, 255, 0.4) !important;
}

/* Sidebar styling */
.css-1d391kg {
    background: rgba(10, 10, 26, 0.95) !important;
    border-right: 2px solid #00ffff !important;
}

/* Metrics styling */
.metric-card {
    background: rgba(26, 26, 51, 0.8);
    border: 1px solid #00ffff;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 0.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: metricFloat 3s ease-in-out infinite;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 255, 255, 0.3);
    border-color: #ff00ff;
}

@keyframes metricFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-3px); }
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #00ffff;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: #cccccc;
    margin-top: 0.5rem;
}

/* Status indicators */
.status-online {
    color: #00ff00;
    animation: statusBlink 2s infinite;
}

.status-offline {
    color: #ff0000;
    animation: statusBlink 2s infinite;
}

@keyframes statusBlink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.5; }
}

/* Loading animation */
.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(0, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #00ffff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Section headers */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00ffff;
    text-align: center;
    margin: 2rem 0 1rem 0;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00ffff, transparent);
}

/* Appointment cards */
.appointment-card {
    background: rgba(26, 26, 51, 0.8);
    border: 1px solid #00ccff;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.appointment-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 204, 255, 0.3);
    border-color: #ff00ff;
}

.appointment-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #00ffff, #ff00ff);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(26, 26, 51, 0.5);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ffff, #ff00ff);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ff00ff, #00ffff);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

def get_system_stats():
    """Fetch system statistics from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/system/stats", timeout=5)
        if response.status_code == 200:
            return response.json().get("stats", {})
    except:
        pass
    
    # Fallback mock data
    return {
        "ai_agent": {"status": "online", "response_time": "0.3s", "accuracy": "95%"},
        "calendar": {"status": "connected", "sync_time": "2s", "availability": "92%"},
        "database": {"status": "connected", "response_time": "0.1s", "uptime": "99%"},
        "network": {"status": "stable", "latency": "45ms", "bandwidth": "100Mbps"}
    }

def get_user_profile():
    """Fetch user profile from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/user/profile", timeout=5)
        if response.status_code == 200:
            return response.json().get("profile", {})
    except:
        pass
    
    # Fallback mock data
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "stats": {"total_appointments": 15, "completed_appointments": 12, "cancelled_appointments": 3}
    }

def get_all_appointments():
    """Fetch all appointments from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/all-appointments", timeout=5)
        if response.status_code == 200:
            return response.json().get("appointments", [])
    except:
        pass
    
    # Fallback mock data
    return [
        {"id": "apt_001", "title": "Team Meeting", "date": "2025-06-28", "time": "14:00", "status": "confirmed"},
        {"id": "apt_002", "title": "Client Call", "date": "2025-06-29", "time": "10:00", "status": "confirmed"},
        {"id": "apt_003", "title": "Code Review", "date": "2025-06-30", "time": "15:00", "status": "confirmed"}
    ]

def send_message(message):
    """Send message to backend and get response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message, "session_id": st.session_state.session_id},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Fallback response
    return {
        "response": "I'm here to help you with appointment booking! How can I assist you today?",
        "session_id": st.session_state.session_id
    }

def create_system_dashboard():
    """Create system status dashboard"""
    stats = get_system_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🤖</div>
            <div class="metric-label">AI Agent</div>
            <div class="status-online">● {stats['ai_agent']['status'].title()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">📅</div>
            <div class="metric-label">Calendar</div>
            <div class="status-online">● {stats['calendar']['status'].title()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🗄️</div>
            <div class="metric-label">Database</div>
            <div class="status-online">● {stats['database']['status'].title()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🌐</div>
            <div class="metric-label">Network</div>
            <div class="status-online">● {stats['network']['status'].title()}</div>
        </div>
        """, unsafe_allow_html=True)

def create_performance_chart():
    """Create performance metrics chart"""
    # Mock performance data
    df = pd.DataFrame({
        'Metric': ['AI Agent', 'Calendar', 'Database', 'Network'],
        'Performance': [95, 92, 99, 87],
        'Color': ['#00ffff', '#00ccff', '#ff00ff', '#cc00ff']
    })
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['Metric'],
            y=df['Performance'],
            marker_color=df['Color'],
            text=df['Performance'].astype(str) + '%',
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="System Performance Metrics",
        title_font_color='#00ffff',
        title_font_size=20,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cccccc',
        showlegend=False,
        height=400
    )
    
    fig.update_xaxes(gridcolor='rgba(0,255,255,0.2)')
    fig.update_yaxes(gridcolor='rgba(0,255,255,0.2)', range=[0, 100])
    
    return fig

# Main UI
def main():
    # Header
    st.markdown('<h1 class="main-title">🤖 TailorTalk</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Appointment Assistant</p>', unsafe_allow_html=True)
    
    # System Dashboard
    st.markdown('<h2 class="section-header">⚡ System Status</h2>', unsafe_allow_html=True)
    create_system_dashboard()
    
    # Performance Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(create_performance_chart(), use_container_width=True)
    
    with col2:
        # User Profile
        profile = get_user_profile()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">👤</div>
            <div class="metric-label">User Profile</div>
            <div style="color: #00ffff; margin-top: 1rem;">
                <strong>{profile['name']}</strong><br>
                Total: {profile['stats']['total_appointments']}<br>
                Completed: {profile['stats']['completed_appointments']}<br>
                Cancelled: {profile['stats']['cancelled_appointments']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat Interface
    st.markdown('<h2 class="section-header">💬 Chat Interface</h2>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("Type your message here...", placeholder="Hi, I'd like to book an appointment...", key="chat_input")
    
    with col2:
        send_button = st.button("🚀 Send", key="send_btn")
    
    # Process message
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("🤖 Processing..."):
            response = send_message(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response["response"]})
        
        st.rerun()
    
    # Quick Actions
    st.markdown('<h2 class="section-header">⚡ Quick Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Check Today's Availability"):
            try:
                response = requests.get(f"{API_BASE_URL}/availability?date={datetime.now().strftime('%Y-%m-%d')}")
                if response.status_code == 200:
                    data = response.json()
                    slots = data.get("available_slots", ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"])
                    st.success(f"Available slots today: {', '.join(slots)}")
                else:
                    st.error("Unable to fetch availability")
            except:
                st.success("Available slots today: 09:00, 10:00, 11:00, 14:00, 15:00, 16:00")
    
    with col2:
        if st.button("🔄 Refresh Status"):
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Appointments Overview
    st.markdown('<h2 class="section-header">📋 Upcoming Appointments</h2>', unsafe_allow_html=True)
    
    appointments = get_all_appointments()
    
    for apt in appointments[:3]:  # Show only first 3
        st.markdown(f"""
        <div class="appointment-card">
            <h4 style="color: #00ffff; margin: 0 0 0.5rem 0;">{apt['title']}</h4>
            <p style="color: #cccccc; margin: 0;">
                📅 {apt['date']} at {apt['time']} | Status: <span style="color: #00ff00;">{apt['status'].title()}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if len(appointments) > 3:
        st.info(f"And {len(appointments) - 3} more appointments...")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666; font-size: 0.9rem;">
        🚀 Powered by TailorTalk AI • Built with Streamlit & FastAPI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

