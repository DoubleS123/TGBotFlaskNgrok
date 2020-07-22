import logging
import time
import flask
import telebot

API_TOKEN = '1258021007:AAEj2HmlkLK1ez7oOOKt8y6zuM-czzWnuHo'
WEBHOOK_HOST = 'cb126c112161.ngrok.io'
WEBHOOK_PORT = 5000
WEBHOOK_LISTEN = '0.0.0.0' 


WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)
soup_menu = {
    '/Борщ'       : 'Красная классика',
    '/Грибной'        : 'Собраны бабкиной рукой',
    '/Овощной': 'В основном капуста',
    '/Рассольник'    : 'То, что ты не любил в детском саду'}

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid,
                 ("Добро пожаловать в наше кафе.\n"
                  "Остался только суп."))
    soup(message)

@bot.message_handler(commands =['Борщ','Грибной','Овощной','Рассольник'])
def mes1 (message):
    cid = message.chat.id
    bot.send_message(cid, ('Отличный выбор! \n'
                           'Спасибо за заказ!'))

def soup(message):
    cid = message.chat.id
    help_text = "Пожалуйста, сделайте свой выбор: \n"
    for key in soup_menu:  
        help_text +=  key + ": "
        help_text += soup_menu[key] + "\n"
    bot.send_message(cid, help_text)  

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    cid = message.chat.id
    bot.send_message(cid, 'Такого блюда нет! Не умеешь читать меню - сиди голодный!')


bot.remove_webhook()

time.sleep(0.1)


bot.set_webhook(url='https://cb126c112161.ngrok.io' + WEBHOOK_URL_PATH)

app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        debug=False)