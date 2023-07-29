import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('6556691353:AAET9cz_wPIog5m2n25D8nnQXy-h9GXCIlk', skip_pending=True)


@bot.message_handler(commands=['start', 'hello'])
def start_message(message):

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id int auto_increment primary key,
                name varchar(50),
                surname varchar(50),
                institute varchar(50),
                age INTEGER
                )""")
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('👋 Поздороваться')
    btn2 = types.KeyboardButton('📲 Зарегестрироваться')
    btn3 = types.KeyboardButton('👀 Просмотреть пользователей')
    markup.row(btn1, btn2)
    markup.row(btn3)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я тестовый бот для бизнес-клуба МГЮА', reply_markup=markup)
 

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == '👋 Поздороваться'):
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я тестовый бот для бизнес-клуба МГЮА')
    
    elif(message.text == '📲 Зарегестрироваться'):
        bot.send_message(message.chat.id, 'Ой-ой')
    
    elif message.text == "👀 Просмотреть пользователей":
        bot.send_message(message.chat.id, 'Упс, меня пока на это не запрограммировали')
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('👋 Поздороваться')
        btn2 = types.KeyboardButton('📲 Зарегестрироваться')
        btn3 = types.KeyboardButton('👀 Просмотреть пользователей')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")

bot.polling(none_stop=True)
