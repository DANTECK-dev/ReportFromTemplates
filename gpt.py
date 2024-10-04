
import openai

YANDEX_GPT_API_KEY = 'your_yandex_gpt_api_key'
openai.api_key = YANDEX_GPT_API_KEY

def generate_content(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
