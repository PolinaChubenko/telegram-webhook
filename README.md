https://github.com/PolinaChubenko/telegram-webhook/actions/workflows/main/badge.svg
# telegram bot on heroku
important modules
```
pip install flask
pip install requests
pip install python-dotenv
pip install psycopg2-binary

for weather-bot 
pip install googletrans==3.1.0a0
pip install country-converter==0.7.3 
```

## To run the telegram bot
Install all requirements manually or via this command

```
pip install -r requirements.txt
```

### on local hosting
Install ngrok and run this command
```
./ngrok http 5000
```
Copy suck a link https://************.ngrok.io
and do not close this terminal window. In any commandline type
with your <BOT_TOKEN> and <COPIED_LINK>
```
curl --location --request POST 'https://api.telegram.org/bot<BOT_TOKEN>/setWebhook' --header 'Content-Type: application/json' --data-raw '{"url": "https://************.ngrok.io"}'
```
To run the bot do following commands
```
export FLASK_APP=main.py
export FLASK_ENV=development [optional]
flask run
```
Keep in mind that you need to configure the connection with postgreSQL database
as in this repo it is done only for heroku postgres as an attached database.

### on heroku
Create an app and connect it to your GitHub repository. Then create heroku
postgres database
```
sudo apt-get install postgresql
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:info
```
Then you will see that everything is OKEY and database was created.
To connect database write
```
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
```
(DATABASE_URL on heroku will be attached automatically).

To run the bot you just need to deploy your branch in heroku ui.

To open database locally and see the table use this commands
```
heroku pg:psql
\dt
select * from chats_bd;
```
To quit this mode type ```\q```

There we go, job well done.

