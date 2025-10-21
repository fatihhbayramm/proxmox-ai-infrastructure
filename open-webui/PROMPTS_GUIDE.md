# 📝 System Prompts Guide

How to use and customize system prompts in Open WebUI.

## 🎯 What are System Prompts?

System prompts define the AI's personality, behavior, and expertise. They set the context for how the AI should respond to users.

## 📦 Available Prompts

We've included 12 ready-to-use prompts in `prompts.json`:

1. **Professional Assistant** - General purpose, accurate responses
2. **Creative Writer** - Storytelling and content creation
3. **Code Expert** - Programming with best practices
4. **Teacher** - Patient explanations with examples
5. **Data Analyst** - Data-driven insights
6. **Marketing Consultant** - Strategic marketing advice
7. **Technical Writer** - Clear documentation
8. **Brainstorm Partner** - Creative ideation
9. **Code Reviewer** - Constructive code reviews
10. **Business Advisor** - Strategic business guidance
11. **Research Assistant** - Thorough research
12. **Productivity Coach** - Task and time management

## 🚀 How to Add Prompts

### Method 1: Via Web UI (Recommended)

1. **Access Open WebUI**
   ```
   http://localhost:3000
   or
   https://ai.yourdomain.com
   ```

2. **Navigate to Prompts**
   - Click your profile icon (top right)
   - Select **Workspace** → **Prompts**
   - Or go to Settings → Prompts

3. **Add New Prompt**
   - Click **"+"** button
   - Fill in:
     - **Name**: Professional Assistant
     - **Description**: Clear, accurate responses
     - **Prompt**: (paste content from prompts.json)
     - **Tags**: professional, general
   - Click **Save**

4. **Repeat for Each Prompt**
   - Copy content from `prompts.json`
   - Create separate prompt for each

### Method 2: Import via API

```bash
# Set your API key
API_KEY="your-api-key"
BASE_URL="http://localhost:3000"

# Read prompts.json and import
curl -X POST "$BASE_URL/api/v1/prompts/import" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @prompts.json
```

### Method 3: Database Import (Advanced)

```bash
# Copy prompts.json into container
docker cp prompts.json open-webui:/tmp/

# Execute import script
docker exec open-webui python -c "
import json
from app.models.prompts import Prompts

with open('/tmp/prompts.json') as f:
    data = json.load(f)
    for prompt in data['prompts']:
        Prompts.create(**prompt)
"
```

## 🎨 Using Prompts in Chat

### Set Default Prompt

1. **Go to Chat Interface**
2. **Click Settings Icon** (in chat)
3. **System Prompt** dropdown
4. **Select your preferred prompt**
5. **Set as default** (optional)

### Change Per Conversation

1. **Start new chat**
2. **Click prompt selector** (top of chat)
3. **Choose different prompt**
4. **Chat behavior changes immediately**

### Quick Switch

Use keyboard shortcut:
- Press `/` in chat
- Type prompt name
- Press Enter

## ✏️ Customizing Prompts

### Edit Existing Prompt

1. **Workspace → Prompts**
2. **Click prompt to edit**
3. **Modify content**
4. **Save changes**

### Create Custom Prompt

**Example: Turkish Language Tutor**
```
You are a friendly Turkish language tutor. Help users learn Turkish through:
- Simple explanations in English
- Turkish phrases with pronunciation
- Common conversation examples
- Cultural context when relevant
- Encouragement and patience

Always provide both Turkish and English in your responses.
```

**Example: SQL Helper**
```
You are a database expert specializing in SQL. When users ask questions:
- Write optimized SQL queries
- Explain query logic step-by-step
- Suggest indexes for performance
- Point out potential issues
- Use proper formatting with comments

Always consider: readability, performance, and security (SQL injection).
```

## 🔧 Advanced Customization

### Add Variables

Use placeholders in prompts:
```
You are a {role} with expertise in {domain}. 
Help users by {action}.
```

Then replace when using:
- role: "marketing consultant"
- domain: "digital advertising"
- action: "creating campaign strategies"

### Context-Aware Prompts

Include file context:
```
You are analyzing the uploaded document. 
Context: {document_content}

User question: {user_question}

Provide accurate answers based only on the document content.
```

### Multi-Language Support

```
You are a multilingual assistant. 
- Respond in the user's language
- If unclear, ask for clarification
- Maintain consistent personality across languages
```

## 📊 Prompt Best Practices

### 1. Be Specific

❌ **Bad:**
```
You are helpful.
```

✅ **Good:**
```
You are a helpful coding assistant specializing in Python. 
Provide clean, documented code with explanations. 
Include error handling and follow PEP 8 style guide.
```

### 2. Set Boundaries

```
You are a medical information assistant. 

IMPORTANT: 
- Provide general health information only
- Always recommend consulting healthcare professionals
- Never diagnose or prescribe
- Cite sources when possible
```

### 3. Define Output Format

```
When explaining code:
1. Brief overview
2. Code with inline comments
3. Example usage
4. Common pitfalls

Use markdown formatting with proper code blocks.
```

### 4. Add Examples

```
You are a creative headline writer.

Example input: "New AI tool helps developers"
Example output: "Revolutionary AI Tool Cuts Development Time by 50%"

Follow this style: attention-grabbing, benefit-focused, specific numbers.
```

### 5. Include Constraints

```
You are a children's story writer.

Constraints:
- Age-appropriate language (6-8 years)
- Stories under 500 words
- Positive messages
- No violence or scary content
- Include moral lessons
```

## 🎯 Prompt Templates

### General Purpose
```
You are a [role] with [expertise]. 
Your goal is to [objective].

When responding:
- [guideline 1]
- [guideline 2]
- [guideline 3]

Always [requirement].
```

### Task-Specific
```
You are helping with [specific task].

Input format: [expected input]
Output format: [desired output]

Requirements:
1. [requirement 1]
2. [requirement 2]

Example:
Input: [example input]
Output: [example output]
```

### Domain Expert
```
You are a [field] expert with [years] years of experience.
Specializations: [list specialties]

Approach:
- [methodology 1]
- [methodology 2]

Communication style: [style description]
```

## 🧪 Testing Prompts

### Test Checklist

- [ ] Does it respond appropriately to the target use case?
- [ ] Does it handle edge cases well?
- [ ] Is the tone/style consistent?
- [ ] Does it follow specified constraints?
- [ ] Is output format as expected?

### A/B Testing

Create variations and compare:

**Version A: Formal**
```
You are a professional business consultant...
```

**Version B: Casual**
```
You're a friendly business advisor...
```

Test with same questions, compare results.

## 📚 Prompt Library Ideas

### Development
- Frontend Developer
- Backend Engineer
- DevOps Specialist
- QA Tester
- Database Administrator

### Content
- Blog Writer
- Social Media Manager
- Email Copywriter
- SEO Specialist
- Video Script Writer

### Business
- Financial Advisor
- Project Manager
- Sales Coach
- Customer Support
- HR Consultant

### Education
- Math Tutor
- Language Teacher
- Science Explainer
- History Professor
- Study Coach

### Creative
- Poet
- Story Writer
- Game Designer
- Music Composer (theory)
- Art Critic

## 🔄 Sharing Prompts

### Export Your Prompts

```bash
# Via API
curl "$BASE_URL/api/v1/prompts" \
  -H "Authorization: Bearer $API_KEY" \
  > my-prompts.json
```

### Share with Team

1. Export prompts to JSON
2. Share file with team
3. Team imports using same method
4. Everyone has same prompts!

## 💡 Tips & Tricks

### 1. Start Simple
Begin with basic prompt, iterate based on responses.

### 2. Use Examples
Show the AI what you want with examples.

### 3. Set Expectations
Clearly define what you want and don't want.

### 4. Test Thoroughly
Try various inputs, edge cases, and scenarios.

### 5. Version Control
Keep track of prompt versions, note what works.

### 6. User Feedback
Ask users which prompts work best, adjust accordingly.

## 🐛 Troubleshooting

### Prompt Not Working

**Problem:** AI doesn't follow prompt instructions

**Solutions:**
- Make instructions more explicit
- Add examples
- Break complex instructions into steps
- Test with simpler version first

### Inconsistent Responses

**Problem:** AI behavior varies

**Solutions:**
- Reduce temperature (Settings → Models)
- Add more specific constraints
- Include consistency requirements in prompt
- Use more examples

### Too Verbose/Brief

**Problem:** Response length not right

**Solutions:**
Add length guidance:
```
Provide concise responses (2-3 paragraphs max).
```
or
```
Provide detailed explanations with examples.
```

## 📞 Getting Help

- **Documentation:** This guide
- **Community:** Share prompts in discussions
- **Examples:** See `prompts.json` for inspiration

---

**Ready to create amazing AI assistants! 🚀**

Start with our pre-made prompts, then customize to fit your needs.