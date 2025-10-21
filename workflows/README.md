# 🔄 n8n Workflow Examples

Ready-to-use n8n workflows powered by local AI (Ollama).

## 📋 Available Workflows

### 1. Email Auto-Responder
**File:** `email-automation.json`

Automatically responds to emails using AI.

**Features:**
- Monitors Gmail inbox
- Filters new emails (ignores replies)
- Generates contextual responses with Ollama
- Sends automated replies

**Use Cases:**
- Customer support automation
- Auto-reply to common inquiries
- Email triage

**Setup:**
1. Import workflow to n8n
2. Configure Gmail OAuth credentials
3. Activate workflow
4. AI will respond to new emails automatically

---

### 2. Daily Content Generator
**File:** `content-generation.json`

Creates social media content automatically every day.

**Features:**
- Runs daily at 9 AM
- Generates engaging posts for LinkedIn/Twitter
- Creates image prompts for visuals
- Saves to Airtable content calendar
- Sends notifications to Telegram

**Use Cases:**
- Social media management
- Content marketing automation
- Personal branding

**Setup:**
1. Import workflow
2. Configure Telegram bot
3. Set up Airtable base
4. Customize topics and tone
5. Adjust schedule as needed

---

### 3. Document Summarizer
**File:** `document-summarizer.json`

Summarizes documents via webhook API.

**Features:**
- Webhook endpoint for document URLs
- Extracts text from PDF/DOCX
- Generates concise summaries
- Creates relevant questions
- Returns JSON response
- Optional Telegram notifications

**Use Cases:**
- Research paper analysis
- Meeting notes summarization
- Report digestion
- API integration

**API Usage:**
```bash
curl -X POST https://n8n.yourdomain.com/webhook/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "document_url": "https://example.com/document.pdf"
  }'
```

**Response:**
```json
{
  "summary": "Main points...",
  "questions": ["Q1?", "Q2?", ...],
  "original_length": 5000,
  "processing_time": "15 seconds"
}
```

---

### 4. Custom Chatbot API
**File:** `chatbot-api.json`

Build your own ChatGPT-like API with conversation history.

**Features:**
- RESTful chat API endpoint
- Session-based conversation history
- PostgreSQL storage
- Context-aware responses
- JSON API responses

**Use Cases:**
- Custom chatbots for websites
- Internal AI assistants
- App integrations
- Customer support bots

**API Usage:**
```bash
curl -X POST https://n8n.yourdomain.com/webhook/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "message": "What is machine learning?"
  }'
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "session_id": "user-123",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## 🚀 Getting Started

### Prerequisites

1. **n8n running** (via docker-compose)
2. **Ollama with models** downloaded
3. **Credentials configured** in n8n:
   - Gmail OAuth (for email workflows)
   - Telegram Bot (for notifications)
   - Airtable API (for content calendar)
   - PostgreSQL (for chatbot)

### Installation Steps

1. **Access n8n:**
   ```
   https://n8n.yourdomain.com
   or
   http://localhost:5678
   ```

2. **Import Workflow:**
   - Click "+" → "Import from File"
   - Select workflow JSON file
   - Click "Import"

3. **Configure Credentials:**
   - Click on nodes with credential icons
   - Add/select appropriate credentials
   - Test connections

4. **Customize Settings:**
   - Update webhook URLs
   - Adjust AI prompts
   - Set schedules
   - Configure notifications

5. **Activate Workflow:**
   - Toggle "Active" switch in top right
   - Workflow now runs automatically

---

## ⚙️ Configuration

### Ollama Connection

All workflows use Ollama API:

**Credentials Setup:**
1. n8n Settings → Credentials
2. Add "Ollama API" credential
3. URL: `http://ollama:11434` (if using docker-compose)
4. Or: `http://localhost:11434` (if n8n runs outside Docker)

### Model Selection

Change models in Ollama nodes:
- `llama2` - Good for general tasks
- `mistral` - Better for creative content
- `codellama` - Best for code generation

### Temperature Settings

Adjust creativity:
- `0.1-0.3` - Factual, consistent
- `0.5-0.7` - Balanced
- `0.8-1.0` - Creative, varied

---

## 🔧 Customization Guide

### Modify AI Prompts

Edit prompt in Ollama nodes:

```
You are a [role]. [Instructions]

Context: {{$json["field"]}}

[Additional instructions]
```

**Tips:**
- Be specific about desired output
- Include examples if needed
- Use system messages for personality
- Add constraints (length, format, tone)

### Add Error Handling

Insert "IF" node after Ollama:

```yaml
Conditions:
  - response is not empty
  - response length > 10
Then: Continue to next node
Else: Send error notification
```

### Schedule Adjustments

Modify Schedule Trigger:
- **Hourly:** `0 * * * *`
- **Daily 9 AM:** `0 9 * * *`
- **Weekly Monday:** `0 9 * * 1`
- **Every 15 min:** `*/15 * * * *`

### Add Notifications

Insert Telegram/Slack/Email node:

```yaml
Message: Workflow completed!
Result: {{$json["result"]}}
Status: ✅ Success
```

---

## 💡 Workflow Ideas

### Additional Workflows You Can Build

1. **Code Review Bot**
   - GitHub PR trigger → Extract code → Ollama review → Comment

2. **Meeting Transcription**
   - Upload audio → Transcribe → Summarize → Send recap

3. **Customer Feedback Analysis**
   - Fetch reviews → Sentiment analysis → Categorize → Generate insights

4. **Blog Post Generator**
   - RSS feed trigger → Extract topics → Generate draft → Save to CMS

5. **Translation Service**
   - Webhook → Detect language → Translate with AI → Return JSON

6. **Data Extraction**
   - Upload invoice/receipt → Extract data → Save to spreadsheet

7. **News Digest**
   - Fetch news daily → Summarize → Compile newsletter → Send email

8. **Q&A Bot for Documentation**
   - Webhook with question → Search docs → Generate answer with context

9. **Social Media Monitor**
   - Monitor mentions → Sentiment analysis → Alert if negative → Auto-respond

10. **Code Generator**
    - Describe requirement → Generate code → Test → Return formatted code

---

## 🐛 Troubleshooting

### Workflow Not Triggering

**Check:**
- Workflow is activated (toggle ON)
- Trigger configuration is correct
- Credentials are valid
- Check execution logs

**Fix:**
```bash
# Check n8n logs
docker logs n8n -f

# Test webhook manually
curl -X POST https://n8n.yourdomain.com/webhook/test
```

### Ollama Connection Failed

**Check:**
- Ollama container is running
- Correct Ollama URL in credentials
- Models are downloaded

**Fix:**
```bash
# Check Ollama status
docker ps | grep ollama

# Test Ollama API
curl http://localhost:11434/api/tags

# Download missing model
docker exec ollama ollama pull llama2
```

### Slow Performance

**Optimize:**
- Use smaller models (7B instead of 13B)
- Reduce temperature
- Limit context length
- Process in batches
- Add caching nodes

### Execution Timeout

**Increase timeout:**

In docker-compose.yml:
```yaml
environment:
  - EXECUTIONS_TIMEOUT=3600  # 1 hour
  - EXECUTIONS_TIMEOUT_MAX=7200  # 2 hours
```

### Memory Issues

**Solutions:**
- Use quantized models (q4_0, q5_0)
- Process smaller chunks
- Add delays between requests
- Restart Ollama periodically

---

## 📊 Best Practices

### 1. Error Handling

Always add error handling:
```
Try → Main workflow
Catch → Error notification
Finally → Cleanup
```

### 2. Testing

Test workflows before production:
- Use test data
- Check all branches
- Verify error handling
- Monitor resource usage

### 3. Monitoring

Add logging nodes:
```yaml
- Log input data
- Log AI responses
- Log errors
- Track execution time
```

### 4. Security

Protect sensitive data:
- Use environment variables
- Encrypt credentials
- Validate webhook inputs
- Rate limit API endpoints
- Use authentication

### 5. Performance

Optimize for speed:
- Cache repeated queries
- Use smaller models when possible
- Batch process when feasible
- Set appropriate timeouts
- Monitor resource usage

### 6. Maintenance

Regular maintenance:
- Review logs weekly
- Update models monthly
- Test critical workflows
- Clean up old executions
- Backup workflow configurations

---

## 🔒 Security Considerations

### Webhook Security

**Add authentication to webhooks:**

1. **Basic Auth:**
```yaml
Webhook → IF node → Check header
If authorization matches → Continue
Else → Return 401
```

2. **API Key:**
```yaml
Webhook → Extract API key → Validate → Continue
```

3. **IP Whitelist:**
```yaml
Webhook → Check source IP → Allow/Deny
```

### Data Privacy

**Protect sensitive information:**
- Don't log personal data
- Encrypt data at rest
- Use secure connections (HTTPS)
- Comply with GDPR/privacy laws
- Anonymize data when possible

### Rate Limiting

**Prevent abuse:**
```yaml
Webhook → Count requests → 
If > limit → Return 429 (Too Many Requests)
Else → Continue
```

---

## 📚 Resources

### Official Documentation

- **n8n Docs:** https://docs.n8n.io/
- **Ollama API:** https://github.com/ollama/ollama/blob/main/docs/api.md
- **Workflow Examples:** https://n8n.io/workflows/

### Tutorials

- **n8n Quickstart:** https://docs.n8n.io/getting-started/
- **Webhook Guide:** https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
- **Error Handling:** https://docs.n8n.io/flow-logic/error-handling/

### Community

- **n8n Community:** https://community.n8n.io/
- **Discord:** https://discord.gg/n8n
- **GitHub:** https://github.com/n8n-io/n8n

### AI/LLM Resources

- **Prompt Engineering:** https://www.promptingguide.ai/
- **Model Comparison:** https://ollama.com/library
- **Fine-tuning Guide:** https://github.com/ollama/ollama/blob/main/docs/modelfile.md

---

## 🤝 Contributing Workflows

Have a useful workflow? Share it!

### Submission Guidelines

1. **Test thoroughly** - Ensure it works
2. **Document well** - Add comments in nodes
3. **Remove credentials** - Clean sensitive data
4. **Add README section** - Describe use case
5. **Submit PR** - Via GitHub

### Workflow Template

```markdown
### Workflow Name
**File:** `workflow-name.json`

Brief description.

**Features:**
- Feature 1
- Feature 2

**Use Cases:**
- Use case 1
- Use case 2

**Setup:**
1. Step 1
2. Step 2
```

---

## 🎓 Learning Path

### Beginner

1. Import and test provided workflows
2. Modify prompts to suit your needs
3. Add simple notifications
4. Understand node connections

### Intermediate

1. Create custom workflows from scratch
2. Add error handling and retries
3. Implement data transformations
4. Use multiple AI models

### Advanced

1. Build complex multi-step automations
2. Integrate with databases
3. Create reusable sub-workflows
4. Implement advanced error recovery
5. Build production-ready APIs

---

## 💬 Example Use Cases

### E-commerce

- **Order Processing:** Webhook → Extract order → Generate invoice → Send email
- **Product Descriptions:** Fetch product → Generate description → Update database
- **Customer Support:** Email trigger → Classify issue → Auto-respond or escalate

### Content Creation

- **Blog Automation:** Topic → Research → Write draft → Format → Publish
- **Video Scripts:** Idea → Outline → Script → Timestamps → Export
- **Newsletter:** Curate content → Summarize → Format → Schedule send

### Data Analysis

- **Report Generation:** Fetch data → Analyze trends → Generate insights → Create report
- **Survey Analysis:** Collect responses → Sentiment analysis → Visualize → Share
- **Log Analysis:** Monitor logs → Detect patterns → Alert on anomalies

### Development

- **Code Review:** PR opened → Extract code → Review → Comment suggestions
- **Documentation:** Code changes → Generate docs → Update wiki
- **Testing:** Deploy → Run tests → Generate report → Notify team

---

## 📈 Performance Metrics

### Typical Processing Times

| Workflow | Average Time | Model Used |
|----------|--------------|------------|
| Email Response | 5-10s | llama2 7B |
| Content Generation | 15-30s | mistral 7B |
| Document Summary | 20-60s | llama2 7B |
| Chatbot Response | 3-8s | llama2 7B |

**Factors affecting speed:**
- Model size (7B vs 13B)
- GPU availability
- Context length
- Temperature settings
- Concurrent requests

### Resource Usage

**Typical memory usage per model:**
- 7B model: ~4-5GB VRAM
- 13B model: ~7-8GB VRAM
- Quantized (q4_0): ~30% less

**Optimization tips:**
- Use quantized models for production
- Limit concurrent executions
- Set execution timeouts
- Monitor GPU temperature

---

## 🔄 Workflow Versions

### Version History

**v1.0 (Current)**
- Email automation
- Content generation
- Document summarization
- Chatbot API

**Coming Soon (v1.1)**
- Voice transcription workflow
- Image generation workflow
- Multi-language translation
- Slack integration examples

---

## 📞 Support

### Getting Help

1. **Check documentation** - Most issues covered here
2. **Review logs** - n8n execution logs show detailed errors
3. **Test components** - Test each node individually
4. **Community forum** - Ask in n8n community
5. **GitHub issues** - Report bugs or request features

### Useful Debug Commands

```bash
# Check n8n logs
docker logs n8n -f

# Check Ollama logs
docker logs ollama -f

# Test Ollama connection
curl http://localhost:11434/api/tags

# List n8n workflows via API
curl http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: your-api-key"

# Check workflow executions
curl http://localhost:5678/api/v1/executions \
  -H "X-N8N-API-KEY: your-api-key"
```

---

## 🎯 Next Steps

1. **Import a workflow** - Start with email automation
2. **Customize prompts** - Make it fit your use case
3. **Test thoroughly** - Ensure it works as expected
4. **Monitor performance** - Check logs and metrics
5. **Build your own** - Create custom workflows
6. **Share back** - Contribute successful workflows

---

**Happy Automating! 🚀**

For more help, check the [main documentation](../docs/) or open an issue on [GitHub](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues).