# Deployment Guide - Text2SQL Agent

## Quick Deploy to Streamlit Cloud (Recommended)

### Prerequisites

- GitHub account
- Private repository: `https://github.com/Joe-ElM/Project-Text2SQL-`
- OpenAI API key (optional - app has fallback)

### Steps

1. **Push code to GitHub**

   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select: `Joe-ElM/Project-Text2SQL-`

3. **Configure deployment**

   - **Main file path**: `app/app.py`
   - **Python version**: 3.9
   - **Requirements**: `requirements.txt` (auto-detected)

4. **Set environment variables**

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for build
   - App will be live at your Streamlit URL

### Features

- **Free hosting**
- **Automatic HTTPS**
- **Custom domain** (paid plans)
- **Sleeps after inactivity** (users can wake)
- **Private repo support**

---

## Alternative: Railway Deployment (Always-On)

### Cost: ~$5-7/month

### Features: Always-on, no sleep, faster than Streamlit Cloud

### Steps

1. **Connect to Railway**

   - Go to [railway.app](https://railway.app)
   - Connect GitHub account
   - Select repository

2. **Configure build**

   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app/app.py --server.port=$PORT`
   - **Port**: Auto-assigned

3. **Environment Variables**

   ```bash
   OPENAI_API_KEY=your_key_here
   PORT=8080
   ```

4. **Deploy**
   - Railway auto-deploys on push
   - Custom domain included

---

## Docker Deployment (Advanced)

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
docker build -t text2sql-agent .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key text2sql-agent
```

---

## Environment Configuration

### Required Variables

```bash
OPENAI_API_KEY=sk-...  # Your OpenAI API key (optional)
```

### Optional Variables

```bash
DB_TYPE=sqlite                           # Default database type
DB_DSN=sqlite:///data/sakila_master.db  # Default connection string
```

### For Production

```bash
OPENAI_API_KEY=sk-...
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## Post-Deployment Checklist

### Test Core Features

- [ ] App loads without errors
- [ ] Sidebar controls work (API key, model selection, database)
- [ ] Can upload SQLite database file
- [ ] Can submit natural language queries
- [ ] SQL queries display properly formatted
- [ ] Chat history persists during session
- [ ] Model switching works (GPT-4o ↔ GPT-4o-mini)

### Test Database Connections

- [ ] SQLite file upload works
- [ ] PostgreSQL connection string works
- [ ] PostgreSQL schema selection works
- [ ] MySQL connection string works
- [ ] Connection status indicators work

### Performance Tests

- [ ] App responds within 5-10 seconds for queries
- [ ] Memory usage stable during extended use
- [ ] No memory leaks in long sessions
- [ ] UI remains responsive during processing

---

## Troubleshooting

### Common Issues

**Build Fails on Streamlit Cloud**

- Check requirements.txt has correct versions
- Ensure all imports are available
- Verify Python 3.9 compatibility

**App Shows "Module Not Found"**

- Add `sys.path.append()` in app.py (already included)
- Check file structure matches expected paths

**OpenAI API Errors**

- Verify API key is set correctly
- Check API key has sufficient credits
- Test with user-provided API key option

**Database Connection Issues**

- Verify connection string format
- Check network access for remote databases
- Ensure database credentials are correct

### Debug Commands

```bash
# Local testing
streamlit run app/app.py --logger.level debug

# Check dependencies
pip list | grep -E "(streamlit|langchain|openai)"

# Test database connections
python -c "from sqlalchemy import create_engine; engine = create_engine('sqlite:///data/sakila_master.db'); print(engine.table_names())"
```

---

## Monitoring & Analytics

### Streamlit Cloud Analytics

- Page views and user sessions
- Error logs and performance metrics
- Geographic user distribution

### Custom Monitoring (Optional)

```python
# Add to app.py for usage tracking
import logging
logging.basicConfig(level=logging.INFO)

# Log user queries (anonymized)
logging.info(f"Query processed: length={len(user_query)}, model={selected_model}")
```

---

## Updates & Maintenance

### Automatic Deployment

- **Streamlit Cloud**: Auto-deploys on git push to main branch
- **Railway**: Auto-deploys on git push with zero downtime
- **Manual**: Push changes, deployment happens automatically

### Update Process

1. Test changes locally: `streamlit run app/app.py`
2. Commit and push: `git add . && git commit -m "Update: description" && git push`
3. Monitor deployment logs for errors
4. Test live application after deployment

### Maintenance Schedule

- **Weekly**: Check error logs and performance
- **Monthly**: Update dependencies if needed
- **Quarterly**: Review and optimize prompts based on usage

---

## Success Metrics

### Key Performance Indicators

- **Response Time**: < 10 seconds per query
- **Success Rate**: > 95% successful SQL generation
- **User Engagement**: Average session > 5 minutes
- **Error Rate**: < 5% of total queries

### Usage Analytics

- Track most common query types
- Monitor database types used
- Analyze model preference (GPT-4o vs GPT-4o-mini)
- Measure user retention and return visits

---

**Deployment Status**: Ready for production deployment
**Target URL**: https://github.com/Joe-ElM/Project-Text2SQL-
**Recommended Platform**: Streamlit Cloud (free) or Railway (always-on)
