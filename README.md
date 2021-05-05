# telegram bot on heroku

```
pip install flask
pip install requests
pip install python-dotenv
```
additional: googletrans==3.1.0a0 and country-converter==0.7.3 

### for local hosting
```
./ngrok http 5000
```
copy https://************.ngrok.io

and do not close this terminal window

```
curl --location --request POST 'https://api.telegram.org/bot<BOT_TOKEN>/setWebhook' --header 'Content-Type: application/json' --data-raw '{"url": "https://************.ngrok.io"}'
```

starting the bot
```
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

### Deploying on Heroku
add Procfile, it is important for heroku
