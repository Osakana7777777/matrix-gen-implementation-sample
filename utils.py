import os
import json
import asyncio
from openai import AsyncOpenAI, RateLimitError
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return AsyncOpenAI(api_key=api_key, base_url=base_url)

def save_to_jsonl(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')
    print(f"Data saved to {filename}")

async def generate_completion(client, messages, model=None, retries=3):
    if model is None:
        model = os.environ.get("OPENAI_MODEL_NAME", "gpt-4o")
    
    for attempt in range(retries):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except RateLimitError:
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit reached. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print("Rate limit reached. Max retries exceeded.")
                return None
        except Exception as e:
            print(f"Error generating completion: {e}")
            return None
