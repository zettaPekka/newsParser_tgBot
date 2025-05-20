from openai import AsyncOpenAI
from typing import Optional
from dotenv import load_dotenv
from mistralai import Mistral

import os


load_dotenv()

client_open_router = AsyncOpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=os.getenv('AI_API_KEY'),
)

client_mistral = Mistral(api_key=os.getenv('AI_API_KEY'))


async def regenerate_open_router(text: str) -> Optional[str]:
    try:
        res = await client_open_router.chat.completions.create(
            model='microsoft/phi-4-reasoning-plus:free',
            messages=[
                {
                    'role': 'user',
                    'content': f'Немного перефразируй этот текст заменяя некоторые слова на синонимы (чтобы смысл не менялся) или перестановкой. Если в тексте более 4 абзацев немного сократи его. Важно не сокращать информацию и не добавлять своей, а так же без других тегов. Обязательно, первый абзац сделай жирным обернуы в html теге b а все остальное курсивным обернуы в html теге i, вот сам текст: {text}' 
                }
            ]
        )
        print(res.choices[0].message.content)
        return res.choices[0].message.content
    except:
        return False


async def regenerate(text: str) -> Optional[str]:
    try:
        chat_response = await client_mistral.chat.complete_async(
            model = 'mistral-large-latest',
            messages = [
                {
                    'role': 'user',
                    'content': f'Перефразируй текст заменяя некоторые слова на синонимы (чтобы смысл не менялся) или перестановкой. Если в тексте более 4 абзацев немного сократи его. Важно не сокращать информацию и не добавлять своей, а так же без других тегов. Обязательно, первый абзац сделай жирным обернув в html теге <b> а все остальное курсивным обернув в html теге <i>, вот сам текст: {text}' 
                },
            ],
            max_tokens=1500
        )
        return chat_response.choices[0].message.content
    except:
        return False