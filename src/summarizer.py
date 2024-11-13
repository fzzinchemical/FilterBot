import requests
import json
import time
import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

class OllamaAPIRequest:
    def __init__(self, model, messages, stream):
        self.model = model
        self.messages = messages
        self.stream = stream

class OllamaAPIResponse:
    def __init__(self, model, created_at, message=None, done=None, context=None, total_duration=None, load_duration=None, prompt_eval_count=None, prompt_eval_duration=None, eval_count=None, eval_duration=None, done_reason=None):
        self.model = model
        self.created_at = created_at
        self.message = message if isinstance(message, Message) else Message(**message) if message else None
        self.done = done
        self.context = context
        self.total_duration = total_duration
        self.load_duration = load_duration
        self.prompt_eval_count = prompt_eval_count
        self.prompt_eval_duration = prompt_eval_duration
        self.eval_count = eval_count
        self.eval_duration = eval_duration
        self.done_reason = done_reason

def summarize_text_with_ollama(text):
    connection = False
    while not connection:
        try:
            url = "http://ollama:11434"
            if requests.get(url).status_code == 200:
                connection = True
        except:
            connection = False
        time.sleep(1)

    if not text.strip():
        return "No text provided for summarization."

    url = "http://ollama:11434/api/chat"
    messages = [Message(role="user", content=f"{text}")]
    payload = OllamaAPIRequest(model=OLLAMA_MODEL, messages=messages, stream=False)

    try:
        response = requests.post(
            url,
            data=json.dumps(payload, default=lambda o: o.__dict__),
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        response_dict = response.json()
        
        # Debugging: Print the response dictionary to understand its structure
        # print("Response Dictionary:", response_dict)
        
        # Extract the relevant part of the response
        response_data = response_dict.get('response', response_dict)
        
        # Ensure response_data is a dictionary
        if isinstance(response_data, str) and response_data.strip() == "":
            response_data = {}
        elif isinstance(response_data, str):
            response_data = json.loads(response_data)
        
        # Ensure all required fields are present
        required_fields = ['model', 'created_at', 'message', 'done']
        for field in required_fields:
            if field not in response_data:
                response_data[field] = None
        
        response = OllamaAPIResponse(**response_data)

        # Check if the message attribute is not None
        if response.message and hasattr(response.message, 'content'):
            return response.message.content
        else:
            raise Exception("Response message is missing or invalid.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to summarize text: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to decode JSON response: {e}")

# Example usage
if __name__ == "__main__":
    text = "Your text here"
    summary = summarize_text_with_ollama(text)
    print(summary)