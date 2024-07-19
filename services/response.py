import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_reply(tweet):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are to make a comment on {tweet}"},
            {"role": "user", "content": tweet}
        ]
    )
    return response.choices[0].message['content']