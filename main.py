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
# connection = psycopg2.connect(DATABASE_URL, sslmode='require')
# cursor = connection.cursor()
# creation = """CREATE TABLE chats_db (id SERIAL PRIMARY KEY, chat_id INTEGER, mode TEXT)"""
# cursor.execute(creation)


def create_db():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute('DROP DATABASE IF EXISTS chats_db')
        creation = """CREATE TABLE chats_db (id SERIAL PRIMARY KEY, chat_id INTEGER, mode TEXT)"""
        cursor.execute(creation)
        cursor.close()
    except (Exception, psycopg2.DatabaseError):
        pass
    finally:
        if connection is not None:
            connection.close()


app = Flask(__name__)
create_db()


def db_add_value(chat_id):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("""SELECT COUNT(*) FROM chats_db WHERE chat_id = %s""", (chat_id,))
        exists = cursor.fetchone()
        # print(exists)
        if exists == (0,):
            cursor.execute("""INSERT INTO chats_db(chat_id, mode) VALUES(%s, %s)""", (chat_id, ''))
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        # print(error)
    finally:
        if connection is not None:

            connection.close()


def bd_change_value(chat_id, mode):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("""UPDATE chats_db SET mode = %s WHERE chat_id = %s""", (mode, chat_id))
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        # print(error)
    finally:
        if connection is not None:
            connection.close()


def db_get_value(chat_id):
    connection = None
    response = ''
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("""SELECT mode FROM chats_db WHERE chat_id = %s""", (chat_id,))
        mode = cursor.fetchone()
        response = mode[0]
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        # print(error)
    finally:
        if connection is not None:
            connection.close()
        return response


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


def is_command(r):
    try:
        if r.json["message"]["entities"][0]["type"] == "bot_command":
            return True
    except KeyError:
        return False
    return False


def parse_command(chat_id, command):
    text = command.split()
    command = text[0]
    text = ' '.join(text[1:])
    if command == "/start":
        send_message(chat_id, "I know command start")
    elif command == "/help":
        send_message(chat_id, "I know command help")
    elif command == "/today" or command == "/tomorrow":
        bd_change_value(chat_id, command[1:])
        if text != "":
            send_message(chat_id, "I changed mode for working with " + text)


@app.route("/", methods=["POST"])
def processing():
    chat_id = request.json["message"]["chat"]["id"]
    db_add_value(chat_id)
    if is_command(request):
        text = request.json["message"]["text"]
        parse_command(chat_id, text)
    else:
        m = db_get_value(chat_id)
        send_message(chat_id, "Hello, sweetheart! You mode is " + m)
    return {"ok": True}


if __name__ == '__main__':
    app.run()
