# ⚡ Workflows Quick Start

Get started with n8n workflows in 5 minutes!

## 🎯 Choose Your First Workflow

### 🚀 Easiest to Start With

**Document Summarizer** - No external services needed!

1. Import `document-summarizer.json`
2. Activate workflow
3. Test immediately:
```bash
curl -X POST http://localhost:5678/webhook/summarize \
  -H "Content-Type: application/json" \
  -d '{"document_url": "https://example.com/doc.pdf"}'
```

### 📧 Most Practical

**Email Auto-Responder** - Automate your inbox!

**Requires:** Gmail account

1. Import `email-automation.json`
2. Connect Gmail (OAuth)
3. Activate
4. Emails auto-responded!

### 🎨 Most Creative

**Content Generator** - Daily social media posts!

**Requires:** Telegram bot (optional)

1. Import `content-generation.json`
2. Customize topics
3. Set schedule
4. Get daily content!

### 💬 Most Powerful

**Chatbot API** - Build your own ChatGPT!

**Requires:** PostgreSQL database

1. Create database:
```sql
CREATE TABLE chat_sessions (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(255),
  user_message TEXT,
  ai_response TEXT,
  created_at TIMESTAMP,
  conversation_history TEXT
);
```
2. Import `chatbot-api.json`
3. Configure DB connection
4. Your ChatGPT API is ready!

---

## 📥 Import Workflow (3 Steps)

### Step 1: Open n8n
```
http://localhost:5678
or
https://n8n.yourdomain.com
```

### Step 2: Import
- Click "+" button (top right)
- Select "Import from File"
- Choose workflow JSON file
- Click "Import"

### Step 3: Activate
- Configure any credentials (if needed)
- Toggle "Active" switch
- Done! ✅

---

## ⚙️ Quick Configuration

### Set Ollama URL

All workflows need Ollama connection:

**If using Docker Compose:**
```
URL: http://ollama:11434
```

**If n8n outside Docker:**
```
URL: http://localhost:11434
```

**Configure:**
1. n8n → Settings → Credentials
2. Add "Ollama API"
3. Enter URL
4. Save

### Test Ollama Connection

```bash
# From terminal
curl http://localhost:11434/api/tags

# Should return list of models
```

---

## 🎨 Customize in 1 Minute

### Change AI Model

In Ollama node:
```
Model: llama2  → Change to: mistral
```

**Available models:**
- `llama2` - Balanced
- `mistral` - Creative
- `codellama` - Code tasks

### Adjust Creativity

```
Temperature: 0.7

Low (0.1-0.3)  = Factual, consistent
Medium (0.5-0.7) = Balanced  
High (0.8-1.0)  = Creative, varied
```

### Modify Prompt

Click Ollama node → Edit prompt:
```
You are a [helpful/professional/creative] assistant.

Task: [describe what you want]

Context: {{$json["your_field"]}}

Output: [specify format]
```

---

## 🧪 Test Workflow

### Method 1: Manual Test
1. Click "Execute Workflow" button
2. Check each node output
3. Verify results

### Method 2: Webhook Test
```bash
curl -X POST http://localhost:5678/webhook/your-path \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Method 3: Check Logs
```bash
# View n8n logs
docker logs n8n -f

# View Ollama logs
docker logs ollama -f
```

---

## 🐛 Common Issues & Quick Fixes

### ❌ "Ollama connection failed"

**Fix:**
```bash
# Check Ollama is running
docker ps | grep ollama

# Check URL in n8n credentials
# Should be: http://ollama:11434
```

### ❌ "Model not found"

**Fix:**
```bash
# Download model
docker exec ollama ollama pull llama2

# List available models
docker exec ollama ollama list
```

### ❌ "Webhook not found"

**Fix:**
- Check workflow is activated (toggle ON)
- Verify webhook path in URL
- Check n8n logs for errors

### ❌ "Out of memory"

**Fix:**
- Use smaller model (7B instead of 13B)
- Use quantized model (llama2:7b-q4_0)
- Reduce context length
- Restart Ollama

---

## 📚 Learn More

**Want to customize further?**
→ See [README.md](README.md) for detailed guide

**Need help?**
→ Check [../docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

**Want to build your own?**
→ Read [n8n documentation](https://docs.n8n.io/)

---

## 🎯 Next Steps

- [ ] Import first workflow
- [ ] Test with sample data
- [ ] Customize prompts
- [ ] Add notifications
- [ ] Build your own workflow
- [ ] Share your creation!

---

## 💡 Pro Tips

1. **Start simple** - Use provided workflows first
2. **Test often** - Check each node individually
3. **Save versions** - Export before major changes
4. **Monitor logs** - Watch for errors
5. **Ask community** - n8n Discord is helpful

---

**Time to build something amazing! 🚀**