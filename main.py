import json
from flask import Flask, request
import os
from os.path import join, dirname
import requests

from src import urls
from dotenv import load_dotenv
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


def create_table():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute('DROP DATABASE IF EXISTS chats_db')
        creation = """CREATE TABLE chats_db (id SERIAL PRIMARY KEY, chat_id INTEGER, mode TEXT)"""
        cursor.execute(creation)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


app = Flask(__name__)
create_table()


def add_value(chat_id):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO chats_db(chat_id, mode) VALUES(%s, %s)", (chat_id, ''))
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.rollback()
            connection.close()


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
