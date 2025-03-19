from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from AI.jsonFileManager import JsonFileManager


load_dotenv()

asistant = AsyncOpenAI(
    api_key=os.getenv("AI_TOKEN"),
    base_url="https://api.proxyapi.ru/openai/v1",
)

manager = JsonFileManager()