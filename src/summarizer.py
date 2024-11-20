"""Ollama API
Raises:
    Exception: ConnectionError
    Exception: ConnectionRefusedError
    Exception: Exception
Returns:
    _type_: string
"""
import os
import time
import json
import requests

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
base_url = os.getenv("OLLAMA_API_URL")
class Message:
    """
    A class to represent a message.

    Attributes:
    role (str): The role of the message sender.
    content (str): The content of the message.
    """
    def __init__(self, role, content):
        """
        Initialize a Message instance.

        Parameters:
        role (str): The role of the message sender.
        content (str): The content of the message.
        """
        self.role = role
        self.content = content

class OllamaAPIRequest:
    """
    A class to represent an API request to Ollama.

    Attributes:
    model (str): The model to be used for the request.
    messages (list): A list of Message instances.
    stream (bool): Whether to stream the response.
    """
    def __init__(self, model, messages, stream):
        """
        Initialize an OllamaAPIRequest instance.

        Parameters:
        model (str): The model to be used for the request.
        messages (list): A list of Message instances.
        stream (bool): Whether to stream the response.
        """
        self.model = model
        self.messages = messages
        self.stream = stream

class OllamaAPIResponse:
    """
    A class to represent an API response from Ollama.

    Attributes:
    model (str): The model used for the response.
    created_at (str): The creation time of the response.
    message (Message): The message content of the response.
    done (bool): Whether the response is complete.
    context (str): The context of the response.
    total_duration (float): The total duration of the response.
    load_duration (float): The load duration of the response.
    prompt_eval_count (int): The prompt evaluation count.
    prompt_eval_duration (float): The prompt evaluation duration.
    eval_count (int): The evaluation count.
    eval_duration (float): The evaluation duration.
    done_reason (str): The reason the response is done.
    """
    def __init__(
        self, model, created_at, *args):
        """
        Initialize an OllamaAPIResponse instance.

        Parameters:
        model (str): The model used for the response.
        created_at (str): The creation time of the response.
        message (dict or Message): The message content of the response.
        done (bool): Whether the response is complete.
        context (str): The context of the response.
        total_duration (float): The total duration of the response.
        load_duration (float): The load duration of the response.
        prompt_eval_count (int): The prompt evaluation count.
        prompt_eval_duration (float): The prompt evaluation duration.
        eval_count (int): The evaluation count.
        eval_duration (float): The evaluation duration.
        done_reason (str): The reason the response is done.
        """
        self.keys = {
            "message" : None,
            "done" : None,
            "context" : None,
            "total_duration" : None,
            "load_duration" : None,
            "prompt_eval_count" : None,
            "prompt_eval_duration" : None,
            "eval_count" : None,
            "eval_duration" : None,
            "done_reason" : None}

        for arg in args:
            if arg in self.keys:
                self.keys[arg] = args[arg]

        self.model = model
        self.created_at = created_at

def summarize_text_with_ollama(text):
    """
    Summarize the given text using the Ollama API.

    Parameters:
    text (str): The text to be summarized.

    Returns:
    str: The summarized text.
    """
    connection = False
    while not connection:
        try:
            url = base_url
            if requests.get(url, timeout=10).status_code == 200:
                connection = True
        except ConnectionError:
            if ConnectionError is ConnectionRefusedError:
                print("CONNECTION REFUSED")
            else:
                print("Retrying to Connect")
        time.sleep(1)

    if not text.strip():
        return "No text provided for summarization."

    url = base_url + "/api/chat/"
    messages = [Message(role="user", content=f"{text}")]
    payload = OllamaAPIRequest(model=OLLAMA_MODEL, messages=messages, stream=False)

    try:
        response = requests.post(
            url,
            data=json.dumps(payload, default=lambda o: o.__dict__),
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        response.raise_for_status()
        response_dict = response.json()

        # Debugging: Print the response dictionary to understand its structure
        # print("Response Dictionary:", response_dict)

        # Extract the relevant part of the response
        response_data = response_dict.get('response', response_dict)

        # Ensure response_data is a dictionary
        if isinstance(response_data, str):
            response_data = json.loads(response_data)

        # Ensure all required fields are present
        required_fields = ['model', 'created_at', 'message', 'done']
        for field in required_fields:
            if field not in response_data:
                response_data[field] = None

        response = OllamaAPIResponse(**response_data)

        # Check if the message attribute is not None
        if response.keys["message"] and hasattr(response.keys["message"], 'content'):
            return response.keys["message"].content
        return "Structural error occured"
    except requests.exceptions.RequestException as e:
        print(f"Failed to summarize text {e}")
        return "Failed to summarize text: RequestException"
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        return "Failed to summerize text: JSONDecodeError"
