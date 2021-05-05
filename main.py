import json
from flask import Flask, request
import os
from os.path import join, dirname
import requests
from src import urls
from dotenv import load_dotenv
import telebot
import time

app = Flask(__name__)
bot = telebot.TeleBot('1782721424:AAFjjA7SQ1AzYmIYszj6Fv2W9Mqq-fRzM6Y')
bot.set_webhook(url="https://telegram-webhook-guide.herokuapp.com:443")


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


# def send_message(chat_id, text, parse_mode=None, reply_markup=None):
#     method = "sendMessage"
#     token = '1782721424:AAFjjA7SQ1AzYmIYszj6Fv2W9Mqq-fRzM6Y'
#     url = urls.TELEGRAM_BOT_URL + f"{token}/{method}"
#     data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "reply_markup": reply_markup}
#     requests.post(url, data=data)


@app.route("/", methods=["POST", "GET"])
def processing():
    if request.method == "POST":
        chat_id = request.json["message"]["chat"]["id"]
        bot.send_message(chat_id, "Hello, sweetheart!")
        return {"ok": True}
    return {"ok": True}


if __name__ == '__main__':
    app.run(host="https://telegram-webhook-guide.herokuapp.com", port=int(os.environ.get('PORT', '443')))
