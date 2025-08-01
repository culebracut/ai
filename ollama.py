import requests
import json

# Configuration
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"  # Corrected endpoint
MODEL_NAME = "gemma3n:latest"  # Or your specific Gemma 3n model like "gemma3:4b"

def ask_gemma_via_ollama(question):
    """
    Sends a question to Gemma running on Ollama via its REST API and returns the response.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False  # Set to True for streaming responses
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        response_data = response.json()
        
        # Check the structure of the response to extract the content
        if "response" in response_data:
            return response_data["response"]
        elif "messages" in response_data and isinstance(response_data["messages"], list):
            # This might be for the /api/chat endpoint, but some generate responses can also have this format
            for message in response_data["messages"]:
                if message.get("role") == "assistant" and "content" in message:
                    return message["content"]
        
        return f"Unexpected response format: {response_data}"

    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {e}"
    except json.JSONDecodeError:
        return f"Error decoding JSON response from Ollama API: {response.text}"

if __name__ == "__main__":
    while True:
        user_question = input("You: ")
        if user_question.lower() in ["exit", "quit"]:
            break

        print("Gemma (Ollama): Thinking...")
        gemma_response = ask_gemma_via_ollama(user_question)
        print(f"Gemma (Ollama): {gemma_response}\n")
