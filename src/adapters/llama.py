from dataclasses import asdict
import json
import os
from groq import Groq
from dotenv import load_dotenv

from src.model.message import ChatMessage

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def invoke_llama(messages: ChatMessage, temperature: float) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[asdict(message) for message in messages],
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    return json.loads(response.choices[0].message.content)
