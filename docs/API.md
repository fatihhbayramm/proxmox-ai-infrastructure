# 🔌 API Documentation

Complete API reference for interacting with your AI infrastructure.

## 📋 Table of Contents

- [Ollama API](#ollama-api)
- [Open WebUI API](#open-webui-api)
- [n8n API](#n8n-api)
- [Code Examples](#code-examples)

---

## Ollama API

Base URL: `http://localhost:11434` or `https://ollama.yourdomain.com`

### Generate Completion

**Endpoint:** `POST /api/generate`

Generate a response from a model.

**Request:**

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

**Response:**

```json
{
  "model": "llama2",
  "created_at": "2024-01-01T00:00:00.000000Z",
  "response": "The sky appears blue because...",
  "done": true
}
```

**Parameters:**

- `model` (required): Model name (e.g., "llama2", "mistral")
- `prompt` (required): The prompt to generate a response for
- `stream` (optional): Stream response (default: true)
- `system` (optional): System message
- `template` (optional): Override model template
- `context` (optional): Context from previous request
- `options` (optional): Model parameters

**Example with options:**

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Explain quantum computing",
  "stream": false,
  "options": {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 40
  }
}'
```

### Chat Completion

**Endpoint:** `POST /api/chat`

Send a chat message with conversation history.

**Request:**

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful AI assistant."
    },
    {
      "role": "user",
      "content": "What is machine learning?"
    }
  ],
  "stream": false
}'
```

**Response:**

```json
{
  "model": "llama2",
  "created_at": "2024-01-01T00:00:00.000000Z",
  "message": {
    "role": "assistant",
    "content": "Machine learning is..."
  },
  "done": true
}
```

### List Models

**Endpoint:** `GET /api/tags`

List all available models.

**Request:**

```bash
curl http://localhost:11434/api/tags
```

**Response:**

```json
{
  "models": [
    {
      "name": "llama2:latest",
      "modified_at": "2024-01-01T00:00:00.000000Z",
      "size": 3826793677
    },
    {
      "name": "mistral:latest",
      "modified_at": "2024-01-01T00:00:00.000000Z",
      "size": 4109850951
    }
  ]
}
```

### Pull Model

**Endpoint:** `POST /api/pull`

Download a model.

**Request:**

```bash
curl http://localhost:11434/api/pull -d '{
  "name": "llama2"
}'
```

### Delete Model

**Endpoint:** `DELETE /api/delete`

Delete a model.

**Request:**

```bash
curl -X DELETE http://localhost:11434/api/delete -d '{
  "name": "llama2"
}'
```

### Show Model Info

**Endpoint:** `POST /api/show`

Get detailed model information.

**Request:**

```bash
curl http://localhost:11434/api/show -d '{
  "name": "llama2"
}'
```

### Embeddings

**Endpoint:** `POST /api/embeddings`

Generate embeddings for text.

**Request:**

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "llama2",
  "prompt": "The quick brown fox"
}'
```

**Response:**

```json
{
  "embedding": [0.123, -0.456, 0.789, ...]
}
```

---

## Open WebUI API

Base URL: `http://localhost:3000` or `https://ai.yourdomain.com`

### Authentication

If authentication is enabled, obtain a token first:

**Endpoint:** `POST /api/v1/auths/signin`

**Request:**

```bash
curl -X POST http://localhost:3000/api/v1/auths/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password"
  }'
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

Use token in subsequent requests:

```bash
curl http://localhost:3000/api/v1/chats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### List Chats

**Endpoint:** `GET /api/v1/chats`

**Request:**

```bash
curl http://localhost:3000/api/v1/chats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Chat

**Endpoint:** `POST /api/v1/chats/new`

**Request:**

```bash
curl -X POST http://localhost:3000/api/v1/chats/new \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat": {
      "title": "New Conversation",
      "models": ["llama2"]
    }
  }'
```

---

## n8n API

Base URL: `http://localhost:5678` or `https://n8n.yourdomain.com`

### Authentication

Get API key from n8n Settings → API Keys

**Headers:**

```
X-N8N-API-KEY: your-api-key
```

### List Workflows

**Endpoint:** `GET /api/v1/workflows`

**Request:**

```bash
curl http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: your-api-key"
```

### Execute Workflow

**Endpoint:** `POST /api/v1/workflows/:id/execute`

**Request:**

```bash
curl -X POST http://localhost:5678/api/v1/workflows/1/execute \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "input": "Your input text"
    }
  }'
```

### Webhook Trigger

**Endpoint:** `POST /webhook/:path`

**Request:**

```bash
curl -X POST http://localhost:5678/webhook/ai-process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Process this with AI"
  }'
```

---

## Code Examples

### Python

**Install dependencies:**

```bash
pip install requests
```

**Basic chat:**

```python
import requests
import json

def chat_with_ollama(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}"

# Usage
result = chat_with_ollama("What is Python?")
print(result)
```

**Streaming response:**

```python
import requests
import json

def stream_chat(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    
    response = requests.post(url, json=payload, stream=True)
    
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "response" in data:
                print(data["response"], end="", flush=True)
            if data.get("done"):
                print()  # New line at end
                break

# Usage
stream_chat("Write a short story about AI")
```

**With conversation history:**

```python
import requests

def chat_conversation(messages, model="llama2"):
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    return response.json()["message"]["content"]

# Usage
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is AI?"},
]

reply = chat_conversation(conversation)
print(reply)

# Continue conversation
conversation.append({"role": "assistant", "content": reply})
conversation.append({"role": "user", "content": "Can you explain more?"})

reply2 = chat_conversation(conversation)
print(reply2)
```

### JavaScript/Node.js

**Install dependencies:**

```bash
npm install axios
```

**Basic chat:**

```javascript
const axios = require('axios');

async function chatWithOllama(prompt, model = 'llama2') {
  const url = 'http://localhost:11434/api/generate';
  
  const payload = {
    model: model,
    prompt: prompt,
    stream: false
  };
  
  try {
    const response = await axios.post(url, payload);
    return response.data.response;
  } catch (error) {
    console.error('Error:', error.message);
    return null;
  }
}

// Usage
chatWithOllama('What is JavaScript?').then(result => {
  console.log(result);
});
```

**Streaming response:**

```javascript
const axios = require('axios');

async function streamChat(prompt, model = 'llama2') {
  const url = 'http://localhost:11434/api/generate';
  
  const payload = {
    model: model,
    prompt: prompt,
    stream: true
  };
  
  const response = await axios.post(url, payload, {
    responseType: 'stream'
  });
  
  response.data.on('data', chunk => {
    const data = JSON.parse(chunk.toString());
    if (data.response) {
      process.stdout.write(data.response);
    }
    if (data.done) {
      console.log('\n');
    }
  });
}

// Usage
streamChat('Explain async/await in JavaScript');
```

### cURL Examples

**Simple question:**

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "What is 2+2?",
  "stream": false
}'
```

**With system message:**

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {
      "role": "system",
      "content": "You are a math tutor. Keep answers concise."
    },
    {
      "role": "user",
      "content": "Explain calculus"
    }
  ],
  "stream": false
}'
```

**Adjust temperature:**

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Write a creative story",
  "stream": false,
  "options": {
    "temperature": 1.2,
    "top_p": 0.9
  }
}'
```

**Generate embeddings:**

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "llama2",
  "prompt": "Represent this text"
}'
```

---

## Model Parameters

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| temperature | float | 0.8 | Creativity (0-2). Higher = more creative |
| top_p | float | 0.9 | Nucleus sampling threshold |
| top_k | int | 40 | Top-k sampling parameter |
| num_predict | int | -1 | Max tokens to generate (-1 = unlimited) |
| repeat_penalty | float | 1.1 | Penalty for repetition |
| seed | int | 0 | Random seed for reproducibility |

### Example with all parameters

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Write a poem",
  "stream": false,
  "options": {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 50,
    "num_predict": 200,
    "repeat_penalty": 1.2,
    "seed": 42
  }
}'
```

---

## Error Handling

### Common HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (model doesn't exist)
- `500`: Internal Server Error

### Example error response

```json
{
  "error": "model not found"
}
```

### Python error handling

```python
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection Error: Is Ollama running?")
except requests.exceptions.Timeout:
    print("Timeout: Request took too long")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Rate Limiting

Currently, there are no rate limits on local installation. However, consider implementing rate limiting for production use or public access.

---

## Best Practices

1. **Use streaming for long responses** - Better UX
2. **Implement timeouts** - Prevent hanging requests
3. **Handle errors gracefully** - Network issues happen
4. **Cache responses** - Save compute for repeated queries
5. **Monitor performance** - Track response times
6. **Use appropriate models** - Smaller models for simple tasks

---

## Additional Resources

- **Ollama Documentation**: <https://github.com/ollama/ollama/blob/main/docs/api.md>
- **Open WebUI API**: Check `/api/docs` endpoint
- **n8n API Documentation**: <https://docs.n8n.io/api/>

---

## Support

For API-related questions:

- GitHub Issues: <https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues>
- Documentation: Check `/docs` folder
