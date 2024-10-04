import openai
import telebot
import requests
import json


def f_promt(message):
    return {
        "modelUri": "gpt://b1ga5hb653meclc8roa5/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "10000"
        },
        "messages": [
            {
                "role": "user",
                "text": message
            }
        ]
    }


url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key AQVNxby_73o3iF_GmP3DLjo1E6al0iPiswGBd72O"
}


# Функция генерации структуры отчета с помощью GPT
def generate_report_structure(bot, user_data):
    prompt = {
        "modelUri": "gpt://b1ga5hb653meclc8roa5/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "10000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты ассистент-помочник для студентов, ты создаешь содержание/структуру того или иного отчета, "
                        "титульный лист и содержание не включается в итоговое сгенерированое содержание"
            },
            {
                "role": "user",
                "text": f"Составь структуру отчета по теме {user_data['theme']} для дисциплины {user_data['subject']}."
            }
        ]
    }
    response = requests.post(url, headers=headers, json=prompt)
    report_structure = json.loads(response.text)["result"]["alternatives"][0]["message"]["text"]
    print(report_structure)
    bot.send_message(user_data['chat_id'], f"Предлагаемая структура отчета:\n{report_structure}")
    bot.send_message(user_data['chat_id'], "Подходит ли эта структура? (Да/Нет)")
    bot.register_next_step_handler_by_chat_id(user_data['chat_id'], confirm_structure, bot, user_data, report_structure)


# Подтверждение структуры отчета
def confirm_structure(message, bot, user_data, report_structure):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Отлично! Начнем заполнять отчет.")
        # Далее бот будет запрашивать детали для каждого раздела структуры
    else:
        bot.send_message(message.chat.id, "Запрашиваю новую структуру...")
        generate_report_structure(bot, user_data)


def simple_request(message, bot, user_data):
    print(message)
    prompt = f_promt(message)
    response = requests.post(url, headers=headers, json=prompt)
    request = json.loads(response.text)["result"]["alternatives"][0]["message"]["text"]
    print(request)
    bot.send_message(user_data['chat_id'], request)
