import os
from openai import OpenAI
client = OpenAI(
    api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
    base_url="https://api.deepseek.com"
)
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a dog"},
        {"role": "user", "content": "who are you"},
    ],
    stream=False
)
print(response.id)