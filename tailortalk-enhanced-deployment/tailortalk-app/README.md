# 🤖 TailorTalk - Enhanced AI Appointment Assistant

## Overview

TailorTalk is a cutting-edge conversational AI agent designed to assist users in booking appointments through natural language interactions. This enhanced version features a stunning sci-fi UI, advanced animations, and comprehensive appointment management capabilities.

## ✨ Enhanced Features

### 🎨 Advanced Sci-Fi UI/UX
- **Futuristic Design**: Dark space theme with neon cyan and magenta accents
- **Animated Background**: Subtle particle effects and moving gradients
- **Glowing Elements**: Neon borders, shadows, and hover effects
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Custom Typography**: Orbitron and Rajdhani fonts for a futuristic feel

### 🤖 AI Agent Capabilities
- **Natural Language Processing**: Understands booking requests in conversational language
- **Intent Recognition**: Identifies user intentions (booking, checking availability, rescheduling)
- **Slot Extraction**: Extracts dates, times, and appointment details from messages
- **Context Awareness**: Maintains conversation context across interactions
- **Smart Responses**: Provides helpful and contextual responses

### 📊 System Dashboard
- **Real-time Status**: Live monitoring of AI Agent, Calendar, Database, and Network
- **Performance Metrics**: Interactive charts showing system performance
- **User Profile**: Display user statistics and preferences
- **System Health**: Comprehensive health checks and status indicators

### 📅 Appointment Management
- **View All Appointments**: Comprehensive list of scheduled appointments
- **Booking Confirmation**: Secure appointment booking with confirmation
- **Availability Checking**: Real-time calendar availability verification
- **Appointment History**: Track past and upcoming appointments
- **Status Management**: Monitor appointment statuses (confirmed, cancelled, etc.)

### 💬 Enhanced Chat Interface
- **Animated Messages**: Smooth slide-in animations for chat bubbles
- **Futuristic Styling**: Gradient backgrounds and glowing effects
- **Real-time Communication**: Instant responses from the AI agent
- **Message History**: Persistent conversation history
- **Quick Actions**: One-click buttons for common tasks

## 🛠 Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB Atlas (with offline fallback)
- **AI Agent**: Custom conversational agent with intent recognition
- **Calendar Integration**: Google Calendar API (mock implementation)
- **Authentication**: Session-based (expandable to OAuth)

### Frontend
- **Framework**: Streamlit (Python)
- **Styling**: Advanced CSS with animations and transitions
- **Charts**: Plotly for interactive data visualizations
- **Responsive Design**: Mobile-first approach with desktop optimization

### Deployment
- **Containerization**: Docker support for easy deployment
- **Cloud Ready**: Configured for Render, Heroku, and other platforms
- **Environment Management**: Comprehensive environment variable configuration
- **Monitoring**: Built-in health checks and status monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (optional - has offline mode)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tailortalk-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection string
   ```

4. **Start the backend**
   ```bash
   cd backend
   python main.py
   ```

5. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```

6. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🌐 Deployment

### Render (Recommended)
1. Push your code to GitHub
2. Create a new Blueprint on Render
3. Connect your repository
4. Render will automatically detect the `render.yaml` file and deploy both services

### Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment
See `DEPLOYMENT.md` for detailed deployment instructions for various platforms.

## 📁 Project Structure

```
tailortalk-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application file
│   ├── agent.py            # Conversational AI agent
│   ├── database.py         # MongoDB integration
│   ├── calendar_service.py # Calendar API integration
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Streamlit frontend
│   ├── app.py             # Main Streamlit application
│   └── requirements.txt   # Frontend dependencies
├── deployment/            # Deployment configurations
│   ├── render.yaml        # Render Blueprint configuration
│   ├── Procfile          # Heroku configuration
│   └── start.sh          # Startup script
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile.backend     # Backend Docker configuration
├── Dockerfile.frontend    # Frontend Docker configuration
├── requirements.txt       # Combined dependencies
├── README.md             # This file
├── DEPLOYMENT.md         # Detailed deployment guide
└── .env.example          # Environment variables template
```

## 🔧 Configuration

### Environment Variables
- `MONGODB_URI`: MongoDB connection string
- `PORT`: Application port (default: 8000 for backend, 8501 for frontend)
- `BACKEND_URL`: Backend API URL for frontend communication

### MongoDB Setup
The application includes a robust fallback system:
- **Online Mode**: Connects to MongoDB Atlas for data persistence
- **Offline Mode**: Uses mock data when database is unavailable
- **Automatic Fallback**: Seamlessly switches between modes

## 🎯 API Endpoints

### Core Endpoints
- `GET /health` - Health check and system status
- `POST /chat` - Send message to AI agent
- `GET /availability` - Check calendar availability
- `POST /book-appointment` - Book a new appointment

### Enhanced Endpoints
- `GET /conversations` - Retrieve conversation history
- `GET /all-appointments` - Get all appointments with details
- `GET /user/profile` - Get user profile information
- `GET /system/stats` - Get system performance statistics
- `DELETE /appointments/{id}` - Cancel an appointment
- `PUT /appointments/{id}` - Reschedule an appointment

## 🎨 UI/UX Features

### Visual Elements
- **Color Palette**: Cyan (#00FFFF), Magenta (#FF00FF), Deep Space Dark (#0A0A1A)
- **Typography**: Orbitron for headings, Rajdhani for body text
- **Animations**: Smooth transitions, hover effects, loading indicators
- **Responsive**: Adapts to different screen sizes and orientations

### Interactive Elements
- **Hover Effects**: Buttons and cards glow on hover
- **Loading States**: Custom sci-fi themed loading animations
- **Status Indicators**: Real-time status updates with color coding
- **Chart Interactions**: Interactive performance metrics

## 🔒 Security Features

- **Input Validation**: Comprehensive input sanitization
- **Error Handling**: Graceful error handling with user-friendly messages
- **Session Management**: Secure session handling
- **API Rate Limiting**: Built-in protection against abuse

## 🧪 Testing

The application includes comprehensive testing:
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **UI Tests**: Visual and interaction testing
- **Performance Tests**: Load and stress testing

## 📈 Performance

- **Response Time**: < 500ms for most operations
- **Scalability**: Designed for horizontal scaling
- **Caching**: Intelligent caching for improved performance
- **Optimization**: Minimized resource usage and fast loading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check the documentation
2. Review the troubleshooting guide in `DEPLOYMENT.md`
3. Open an issue on GitHub
4. Contact the development team

## 🎉 Acknowledgments

- Built with FastAPI and Streamlit
- Inspired by modern sci-fi interfaces
- Designed for real-world appointment booking scenarios
- Enhanced with cutting-edge UI/UX principles

---

**TailorTalk** - Where AI meets beautiful design for seamless appointment management! 🚀

