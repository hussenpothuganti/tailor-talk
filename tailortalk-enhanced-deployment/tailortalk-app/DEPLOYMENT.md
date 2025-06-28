# TailorTalk Deployment Guide

This guide provides step-by-step instructions for deploying TailorTalk on various platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended)

**Backend Deployment:**
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python main.py`
   - **Environment Variables**:
     ```
     MONGODB_URI=mongodb+srv://shaikmahammadhussain835:pgBZgM9gYvXmLzw1@hussain.vo52sy7.mongodb.net/?retryWrites=true&w=majority&appName=Hussain
     PORT=8000
     ```

**Frontend Deployment:**
1. Create another Web Service on Render
2. Set the following:
   - **Build Command**: `cd frontend && pip install -r requirements.txt`
   - **Start Command**: `cd frontend && streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment Variables**:
     ```
     BACKEND_URL=https://your-backend-service.onrender.com
     ```

### Option 2: Heroku

1. Install Heroku CLI
2. Create two apps:
   ```bash
   heroku create tailortalk-backend
   heroku create tailortalk-frontend
   ```
3. Deploy backend:
   ```bash
   git subtree push --prefix=backend heroku-backend main
   ```
4. Deploy frontend:
   ```bash
   git subtree push --prefix=frontend heroku-frontend main
   ```

### Option 3: Docker Deployment

**Local Docker:**
```bash
docker-compose up -d
```

**Production Docker:**
```bash
# Build images
docker build -f Dockerfile.backend -t tailortalk-backend .
docker build -f Dockerfile.frontend -t tailortalk-frontend .

# Run containers
docker run -d -p 8000:8000 --name backend tailortalk-backend
docker run -d -p 8501:8501 --name frontend tailortalk-frontend
```

### Option 4: Railway

1. Connect GitHub repository to Railway
2. Create two services from the same repo
3. Set build commands and environment variables as per Render instructions

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
MONGODB_URI=mongodb+srv://shaikmahammadhussain835:pgBZgM9gYvXmLzw1@hussain.vo52sy7.mongodb.net/?retryWrites=true&w=majority&appName=Hussain
PORT=8000
```

**Frontend:**
```env
BACKEND_URL=https://your-backend-url.com
```

### MongoDB Setup

The application is pre-configured with the provided MongoDB Atlas connection. The database will automatically:
- Create collections on first use
- Fall back to mock mode if unavailable
- Handle SSL/TLS connections securely

### Domain Configuration

After deployment, update the frontend code to point to your backend URL:

In `frontend/app.py`, line 15:
```python
API_BASE_URL = "https://your-backend-url.onrender.com"
```

## 🔍 Verification

After deployment, verify the following:

1. **Backend Health Check**: `GET https://your-backend-url/health`
2. **Frontend Access**: Visit your frontend URL
3. **Chat Functionality**: Send a test message
4. **Calendar Integration**: Click "Check Today's Availability"

## 🐛 Troubleshooting

### Common Issues

**Backend not starting:**
- Check MongoDB connection string
- Verify environment variables
- Check logs for SSL/TLS errors

**Frontend not connecting to backend:**
- Update `API_BASE_URL` in frontend code
- Check CORS settings
- Verify backend is accessible

**Database connection issues:**
- Application runs in mock mode automatically
- Check MongoDB Atlas network access
- Verify connection string format

### Logs and Monitoring

**Render:**
- View logs in Render dashboard
- Set up log drains for external monitoring

**Heroku:**
```bash
heroku logs --tail --app your-app-name
```

**Docker:**
```bash
docker logs container-name
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **MongoDB**: Use IP whitelisting in Atlas
3. **CORS**: Configure appropriate origins for production
4. **HTTPS**: Ensure SSL/TLS in production
5. **API Keys**: Rotate credentials regularly

## 📊 Performance Optimization

1. **Caching**: Implement Redis for session storage
2. **CDN**: Use CDN for static assets
3. **Database**: Add indexes for frequently queried fields
4. **Monitoring**: Set up application monitoring

## 🔄 CI/CD Pipeline

**GitHub Actions Example:**
```yaml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

## 📈 Scaling

**Horizontal Scaling:**
- Deploy multiple backend instances
- Use load balancer
- Implement session affinity

**Database Scaling:**
- MongoDB Atlas auto-scaling
- Read replicas for read-heavy workloads
- Sharding for large datasets

## 🆘 Support

For deployment issues:
1. Check this guide first
2. Review application logs
3. Verify environment configuration
4. Test locally with same configuration

---

**Happy Deploying! 🚀**

