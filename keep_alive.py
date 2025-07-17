from flask import Flask, request
import telebot
import os

app = Flask(_name_)
TOKEN = "8090368961:AAHLbisTtk844DgZm1qv-finteOELWeaSF4"
bot = telebot.TeleBot(TOKEN)

@app.route('/', methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

def keep_alive():
    app.run(host='0.0.0.0', port=10000)