import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1",
    api_key=os.getenv("NEBIUS_API_KEY"),
)

try:
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {"role": "user", "content": "Confirm connection to Nebius Token Factory."}
        ],
    )
    print("STATUS: Connected to Nebius Token Factory (NVIDIA Nemotron)")
except Exception as e:
    print("ERROR:", e)