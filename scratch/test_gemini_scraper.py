import os
import sys
import pydantic
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GEMINI API KEY')
if not api_key:
    # Try parent directory .env
    if os.path.exists('../.env'):
        with open('../.env', 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.split('=', 1)
                    if k.strip() in ['GEMINI_API_KEY', 'GEMINI API KEY']:
                        api_key = v.strip()
                        break

if not api_key:
    print('No API key found')
    sys.exit(1)

genai.configure(api_key=api_key)

class RawCharacter(pydantic.BaseModel):
    name: str
    role: str
    mal_character_id: int | None
    mal_character_url: str | None

class CharacterList(pydantic.BaseModel):
    characters: list[RawCharacter]

model = genai.GenerativeModel('gemini-2.5-flash')
prompt = 'List the main and supporting characters of the anime/manga "Nisekoi". Provide approximate MAL IDs and URLs if you know them.'

try:
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type='application/json',
            response_schema=CharacterList
        )
    )
    print('Successful response!')
    print(response.text)
except Exception as e:
    print('Error:', e)
