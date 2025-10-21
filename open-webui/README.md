# 💬 Open WebUI Configuration

Complete guide for Open WebUI setup, customization, and optimization.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Customization](#customization)
- [User Management](#user-management)
- [Model Management](#model-management)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

Open WebUI is a self-hosted ChatGPT-like interface for Ollama. It provides:

- 💬 **Chat Interface** - Beautiful, responsive UI
- 📝 **Conversation History** - Save and organize chats
- 👥 **Multi-user Support** - Team collaboration
- 🎨 **Customization** - Themes, prompts, models
- 📊 **Usage Analytics** - Track usage patterns
- 🔐 **Authentication** - User management and access control

**Default Access:**
- URL: http://localhost:3000 or https://ai.yourdomain.com
- First user becomes admin automatically

---

## 🚀 Installation

### Quick Start (Already in docker-compose.yml)

```yaml
open-webui:
  image: ghcr.io/open-webui/open-webui:main
  container_name: open-webui
  restart: unless-stopped
  ports:
    - "3000:8080"
  environment:
    - OLLAMA_BASE_URL=http://ollama:11434
  volumes:
    - open-webui_data:/app/backend/data
```

### Verify Installation

```bash
# Check container status
docker ps | grep open-webui

# Check logs
docker logs open-webui

# Test access
curl http://localhost:3000/health
```

---

## ⚙️ Configuration

### Environment Variables

Add to `docker/.env`:

```env
# Basic Settings
OLLAMA_BASE_URL=http://ollama:11434
WEBUI_NAME=AI Assistant
DEFAULT_USER_ROLE=user

# Authentication
WEBUI_AUTH=true
ENABLE_SIGNUP=false  # Disable public signup
WEBUI_SECRET_KEY=your-secret-key-here

# Models
DEFAULT_MODELS=llama2,mistral
ENABLE_MODEL_FILTER=true

# Features
ENABLE_RAG=true
ENABLE_ADMIN_EXPORT=true
ENABLE_COMMUNITY_SHARING=false

# Performance
REQUEST_TIMEOUT=120
CHUNK_SIZE=8192
```

### Full Configuration in docker-compose.yml

```yaml
open-webui:
  image: ghcr.io/open-webui/open-webui:main
  container_name: open-webui
  restart: unless-stopped
  ports:
    - "3000:8080"
  environment:
    # Connection
    - OLLAMA_BASE_URL=http://ollama:11434
    
    # Branding
    - WEBUI_NAME=My AI Assistant
    - WEBUI_FAVICON_URL=/static/favicon.png
    
    # Security
    - WEBUI_AUTH=true
    - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
    - ENABLE_SIGNUP=${ENABLE_SIGNUP:-false}
    - DEFAULT_USER_ROLE=user
    
    # Models
    - DEFAULT_MODELS=llama2,mistral
    - ENABLE_MODEL_FILTER=true
    - MODEL_FILTER_LIST=llama2;mistral;codellama
    
    # Features
    - ENABLE_RAG=true
    - RAG_EMBEDDING_MODEL=llama2
    - ENABLE_WEB_SEARCH=false
    - ENABLE_IMAGE_GENERATION=false
    - ENABLE_ADMIN_EXPORT=true
    
    # Performance
    - REQUEST_TIMEOUT=120
    - CHUNK_SIZE=8192
    - NUM_PARALLEL_REQUESTS=1
    
    # Storage
    - DATA_DIR=/app/backend/data
    
    # Logs
    - LOG_LEVEL=INFO
    
  volumes:
    - open-webui_data:/app/backend/data
  depends_on:
    - ollama
  networks:
    - ai-network
```

---

## 🎨 Customization

### Change Interface Name

```env
WEBUI_NAME=My Company AI
```

### Custom Logo

1. Prepare your logo (PNG, 512x512 recommended)
2. Mount custom files:

```yaml
volumes:
  - ./open-webui/static:/app/backend/static
```

3. Place logo at `open-webui/static/logo.png`

### Custom Theme Colors

Create `open-webui/custom.css`:

```css
:root {
  --primary-color: #6366f1;
  --secondary-color: #8b5cf6;
  --background-color: #1f2937;
  --text-color: #f9fafb;
}
```

Mount in docker-compose:
```yaml
volumes:
  - ./open-webui/custom.css:/app/backend/static/custom.css
```

### Default System Prompts

Create custom prompts via UI:
1. Settings → Prompts
2. Click "+" to add new
3. Set as default

**Example Prompts:**

**Professional Assistant:**
```
You are a professional AI assistant. Provide clear, accurate, and helpful responses. 
Be concise but thorough. If you're unsure, say so.
```

**Creative Writer:**
```
You are a creative writing assistant. Help users craft engaging stories, 
articles, and content. Be imaginative and suggest improvements.
```

**Code Helper:**
```
You are an expert programmer. Provide clean, well-documented code with explanations. 
Include error handling and best practices.
```

---

## 👥 User Management

### Create Admin User

First user to register becomes admin automatically.

**Via UI:**
1. Go to http://localhost:3000
2. Click "Sign Up"
3. Fill in details
4. You're now admin!

### Add More Users

**Option 1: Enable Signup**
```env
ENABLE_SIGNUP=true
```

**Option 2: Admin Invites** (Recommended)
1. Admin → Users → Invite User
2. Share invitation link
3. User registers with link

**Option 3: Direct Creation**
1. Admin → Users → Add User
2. Fill in details
3. User receives credentials

### User Roles

**Admin:**
- Full system access
- User management
- System settings
- Model management

**User:**
- Chat with AI
- View own history
- Basic settings

**Pending:**
- Awaiting admin approval
- Limited access

### Manage Users

```bash
# View users via Docker
docker exec open-webui cat /app/backend/data/webui.db | grep users

# Backup user data
docker cp open-webui:/app/backend/data/webui.db ./backup/
```

---

## 🤖 Model Management

### Add Models

Models are automatically detected from Ollama:

```bash
# Download model in Ollama
docker exec ollama ollama pull llama2

# Refresh Open WebUI to see new model
# Settings → Models → Refresh
```

### Set Default Models

```env
DEFAULT_MODELS=llama2,mistral
```

### Model Filter

Only show specific models:

```env
ENABLE_MODEL_FILTER=true
MODEL_FILTER_LIST=llama2;mistral;codellama
```

### Model Settings

Per-model settings in UI:
1. Settings → Models
2. Click model name
3. Adjust:
   - Temperature
   - Top P
   - Top K
   - Max tokens
   - Stop sequences

**Recommended Settings:**

| Model | Temperature | Top P | Use Case |
|-------|-------------|-------|----------|
| llama2 | 0.7 | 0.9 | General chat |
| mistral | 0.8 | 0.95 | Creative tasks |
| codellama | 0.3 | 0.9 | Code generation |

---

## 🚀 Advanced Features

### RAG (Retrieval Augmented Generation)

Enable document chat:

```env
ENABLE_RAG=true
RAG_EMBEDDING_MODEL=llama2
RAG_CHUNK_SIZE=1500
RAG_CHUNK_OVERLAP=100
```

**Usage:**
1. Click 📎 in chat
2. Upload PDF/TXT/MD files
3. Ask questions about documents

### Web Search (Optional)

Requires external API:

```env
ENABLE_WEB_SEARCH=true
WEB_SEARCH_ENGINE=searxng  # or duckduckgo, google
SEARXNG_URL=http://searxng:8080
```

### Function Calling

Enable advanced AI capabilities:

```env
ENABLE_FUNCTION_CALLING=true
```

### Custom Functions

Create via UI:
1. Settings → Functions
2. Add custom Python functions
3. AI can call them during chat

**Example Function:**
```python
def calculate(expression: str) -> float:
    """Calculate mathematical expressions"""
    return eval(expression)
```

### Memory/Context

```env
MAX_CONTEXT_LENGTH=4096
CONVERSATION_HISTORY_SIZE=20
```

### Rate Limiting

```env
ENABLE_RATE_LIMITING=true
RATE_LIMIT_REQUESTS=60  # per minute
RATE_LIMIT_WINDOW=60    # seconds
```

---

## 🔧 Advanced Configuration

### Custom Backend URL

If Ollama is on different host:

```env
OLLAMA_BASE_URL=http://192.168.1.125:11434
# or
OLLAMA_BASE_URL=https://ollama.yourdomain.com
```

### Multiple Ollama Instances

Load balance across multiple Ollama servers:

```env
OLLAMA_BASE_URLS=http://ollama1:11434,http://ollama2:11434
```

### Database Configuration

Default: SQLite
Optional: PostgreSQL for better performance

```env
DATABASE_URL=postgresql://user:password@postgres:5432/openwebui
```

### Custom Storage Path

```yaml
volumes:
  - /mnt/data/openwebui:/app/backend/data
```

### Backup Configuration

```bash
# Create backup script
cat > backup-openwebui.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker cp open-webui:/app/backend/data ./backups/openwebui-$DATE
echo "Backup created: openwebui-$DATE"
EOF

chmod +x backup-openwebui.sh

# Add to crontab
0 2 * * * /path/to/backup-openwebui.sh
```

---

## 🐛 Troubleshooting

### Cannot Connect to Ollama

**Problem:** "Failed to connect to Ollama"

**Solutions:**
```bash
# Check Ollama is running
docker ps | grep ollama

# Check network
docker network inspect ai-network

# Test connection from Open WebUI
docker exec open-webui curl http://ollama:11434/api/tags

# Verify OLLAMA_BASE_URL
docker exec open-webui env | grep OLLAMA
```

### Models Not Showing

**Problem:** No models in dropdown

**Solutions:**
```bash
# Download models
docker exec ollama ollama pull llama2

# Restart Open WebUI
docker restart open-webui

# Check Ollama API
curl http://localhost:11434/api/tags
```

### Slow Responses

**Problem:** Chat responses are slow

**Solutions:**
1. Use smaller models (7B instead of 13B)
2. Increase timeout:
```env
REQUEST_TIMEOUT=300
```
3. Check GPU usage:
```bash
nvidia-smi
```
4. Reduce context:
```env
MAX_CONTEXT_LENGTH=2048
```

### Authentication Issues

**Problem:** Cannot login

**Solutions:**
```bash
# Reset admin password
docker exec open-webui python -c "
from app.models.users import Users
user = Users.get_user_by_email('admin@example.com')
user.update_password('newpassword')
"

# Or reset database (WARNING: loses data)
docker stop open-webui
docker volume rm open-webui_data
docker start open-webui
```

### Upload Errors

**Problem:** Cannot upload documents

**Solutions:**
```env
# Increase upload limit
MAX_UPLOAD_SIZE=100  # MB

# Enable RAG
ENABLE_RAG=true

# Check disk space
df -h
```

### Memory Issues

**Problem:** Container crashes / OOM

**Solutions:**
```yaml
# Limit memory
deploy:
  resources:
    limits:
      memory: 2G
```

---

## 📊 Usage Analytics

### View Statistics

Admin Dashboard shows:
- Total users
- Total chats
- Model usage
- Active users
- Response times

### Export Data

```bash
# Export all chats
# Admin → Settings → Export

# Or via Docker
docker cp open-webui:/app/backend/data/webui.db ./exports/
```

### Monitor Logs

```bash
# Real-time logs
docker logs -f open-webui

# Last 100 lines
docker logs --tail 100 open-webui

# Search logs
docker logs open-webui 2>&1 | grep ERROR
```

---

## 🔐 Security Best Practices

### 1. Disable Public Signup

```env
ENABLE_SIGNUP=false
```

### 2. Use Strong Secret Key

```bash
# Generate secure key
openssl rand -base64 32

# Add to .env
WEBUI_SECRET_KEY=your-generated-key
```

### 3. Enable Authentication

```env
WEBUI_AUTH=true
```

### 4. Use HTTPS

Access via Cloudflare Tunnel:
```
https://ai.yourdomain.com
```

### 5. Regular Backups

```bash
# Automated daily backups
0 2 * * * docker cp open-webui:/app/backend/data /backups/$(date +\%Y\%m\%d)
```

### 6. Update Regularly

```bash
# Update Open WebUI
docker pull ghcr.io/open-webui/open-webui:main
docker-compose up -d
```

---

## 🎯 Tips & Tricks

### Keyboard Shortcuts

- `Ctrl + Enter` - Send message
- `Ctrl + /` - Command palette
- `Ctrl + K` - New chat
- `Ctrl + Shift + L` - Toggle sidebar

### Better Prompts

**Instead of:**
```
Write about AI
```

**Try:**
```
Write a 500-word article about AI in healthcare, 
including 3 real-world examples and future implications.
```

### Use System Prompts

Create role-specific prompts:
- Code Reviewer
- Content Writer
- Language Teacher
- Data Analyst

### Organize Chats

- Use descriptive titles
- Tag conversations
- Archive old chats
- Export important ones

### Model Selection Tips

- **Quick questions:** llama2:7b
- **Creative writing:** mistral:7b
- **Code tasks:** codellama:7b
- **Long context:** llama2:13b (if enough VRAM)

---

## 📚 Resources

### Official Links
- **GitHub:** https://github.com/open-webui/open-webui
- **Documentation:** https://docs.openwebui.com
- **Discord:** https://discord.gg/open-webui

### Community
- **Reddit:** r/OpenWebUI
- **GitHub Discussions:** Feature requests and support

---

## 🆘 Getting Help

1. **Check logs:** `docker logs open-webui`
2. **Restart container:** `docker restart open-webui`
3. **Check documentation:** This file and official docs
4. **Ask community:** GitHub Discussions or Discord
5. **Open issue:** If you found a bug

---

**Enjoy your self-hosted AI chat interface! 💬🚀**