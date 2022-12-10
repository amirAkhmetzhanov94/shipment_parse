import requests
import json
import os

from dotenv import load_dotenv

import telebot


def send_request():
    url = os.environ.get("API_LINK")
    headers = {
        "Authorization": os.environ.get("AUTHORIZATION_TOKEN")
    }
    response = requests.get(url, headers=headers)
    return response


def normalize(response):
    return json.loads(response.content)

def init_telebot():
    TOKEN = os.environ["BOT_TOKEN"]
    bot = telebot.TeleBot(TOKEN)
    return bot

def main():
    load_dotenv()
    status_codes = {
        0: "Ожидаем",
        1: "Получили",
        2: "На упаковке",
        3: "Отправили",
        4: "Готовы к выдаче",
        5: "На доставке",
        6: "Доставлены"
    }
    response = send_request()
    data = normalize(response)[0]["status"]
    human_order_status = status_codes.get(data, "Нет такого статус-кода")
    telegram_bot = init_telebot()
    telegram_bot.send_message(
        chat_id=os.environ.get("CHAT_ID"),
        text=f"Код: {data}\nЧеловеческое представление: {human_order_status}"
    )
    return human_order_status


if __name__ == "__main__":
    main()