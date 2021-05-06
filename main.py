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
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# cursor.execute("""CREATE TABLE albums
#                   (title text, artist text, release_date text,
#                    publisher text, media_type text)
#                """)

print('PostgreSQL database version:')
print(cur.execute('SELECT version()'))

cur.execute("""CREATE TABLE IF NOT EXIST albums (title text, artist text, release_date text, publisher text, media_type text)""")
cur.execute("""INSERT INTO albums VALUES ('Glow', 'Andy Hunter', '7/24/2012', 'Xplore Records', 'MP3')""")
conn.commit()

app = Flask(__name__)


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
    if request.method == "POST":
        chat_id = request.json["message"]["chat"]["id"]
        send_message(chat_id, "Hello, sweetheart!")
        return {"ok": True}
    return {"ok": True}


if __name__ == '__main__':
    app.run()
