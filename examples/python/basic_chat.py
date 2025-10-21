#!/usr/bin/env python3
"""
Basic Chat Example with Ollama
Simple question-answer interaction
"""

import requests
import json
from typing import Dict, Any

class OllamaChat:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> Dict[str, Any]:
        """
        Generate a response using the generate endpoint
        
        Args:
            model: Model name (e.g., 'llama2', 'mistral')
            prompt: The prompt to send
            stream: Whether to stream the response
            
        Returns:
            Dictionary containing the response
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        response = requests.post(self.generate_url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def chat(self, model: str, messages: list, stream: bool = False) -> Dict[str, Any]:
        """
        Send a chat message with conversation history
        
        Args:
            model: Model name
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response
            
        Returns:
            Dictionary containing the response
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        response = requests.post(self.chat_url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def stream_generate(self, model: str, prompt: str):
        """
        Stream a response line by line
        
        Args:
            model: Model name
            prompt: The prompt to send
            
        Yields:
            Response chunks as they arrive
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }
        
        response = requests.post(self.generate_url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]
                if data.get("done"):
                    break


def main():
    # Initialize chat client
    chat = OllamaChat()
    
    # Example 1: Simple question
    print("=" * 50)
    print("Example 1: Simple Question")
    print("=" * 50)
    
    result = chat.generate(
        model="llama2",
        prompt="What is the capital of France?"
    )
    print(f"Question: What is the capital of France?")
    print(f"Answer: {result['response']}")
    print()
    
    # Example 2: Streaming response
    print("=" * 50)
    print("Example 2: Streaming Response")
    print("=" * 50)
    
    print("Question: Explain quantum computing in simple terms.")
    print("Answer: ", end="", flush=True)
    
    for chunk in chat.stream_generate(
        model="llama2",
        prompt="Explain quantum computing in simple terms."
    ):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Example 3: Chat with history
    print("=" * 50)
    print("Example 3: Conversation with History")
    print("=" * 50)
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "What is machine learning?"
        }
    ]
    
    result = chat.chat(model="llama2", messages=messages)
    print(f"User: What is machine learning?")
    print(f"Assistant: {result['message']['content']}")
    
    # Continue conversation
    messages.append(result["message"])
    messages.append({
        "role": "user",
        "content": "Can you give me an example?"
    })
    
    result = chat.chat(model="llama2", messages=messages)
    print(f"\nUser: Can you give me an example?")
    print(f"Assistant: {result['message']['content']}")
    print()
    
    # Example 4: Different models
    print("=" * 50)
    print("Example 4: Comparing Models")
    print("=" * 50)
    
    prompt = "Write a haiku about AI"
    
    for model in ["llama2", "mistral"]:
        try:
            result = chat.generate(model=model, prompt=prompt)
            print(f"\n{model.upper()}:")
            print(result['response'])
        except Exception as e:
            print(f"\n{model.upper()}: Model not available ({e})")


if __name__ == "__main__":
    main()