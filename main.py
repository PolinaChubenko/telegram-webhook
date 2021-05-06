import json
from flask import Flask, request
import os
from os.path import join, dirname
import requests

from src import urls
from dotenv import load_dotenv
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
connection = psycopg2.connect(DATABASE_URL, sslmode='require')


def add_table():
    try:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE chats (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, mode TEXT)""")
        cursor.close()
    except psycopg2.Error:
        pass


def add_value(chat_id):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO albums VALUES(NULL, ?, '')", chat_id)
        connection.commit()
    except psycopg2.Error:
        connection.rollback()


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def send_message(chat_id, text, parse_mode=None, reply_markup=None):
    method = "sendMessage"
    token = get_from_env("BOT_TOKEN")
    url = urls.TELEGRAM_BOT_URL + f"{token}/{method}"
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "reply_markup": reply_markup}
    requests.post(url, data=data)


@app.route("/", methods=["POST"])
def processing():
    chat_id = request.json["message"]["chat"]["id"]
    add_value(chat_id)
    send_message(chat_id, "Hello, sweetheart!")
    return {"ok": True}


if __name__ == '__main__':
    app.run()
