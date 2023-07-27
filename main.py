import telebot
from telebot import types

bot = telebot.TeleBot('6556691353:AAET9cz_wPIog5m2n25D8nnQXy-h9GXCIlk', skip_pending=True)


@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/hello')
    markup.add(btn1)
    btn2 = types.KeyboardButton('/help')
    markup.add(btn2)
    btn3 = types.KeyboardButton('/admin_message_info')
    markup.add(btn3)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Это тестовый бот для бизнес-клуба МГЮА', reply_markup=markup)
 

@bot.message_handler(commands=['admin_message_info'])
def send_admin_info(message):
    bot.send_message(message.chat.id, message)

@bot.message_handler(commands=['help'])
def send_admin_info(message):
    bot.send_message(message.chat.id, 'Упс, пока что здесь ничего нет...')

bot.polling(none_stop=True)
