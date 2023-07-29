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
                age int
                )""")
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📲 Зарегестрироваться')
    btn2 = types.KeyboardButton('👀 Просмотреть пользователей')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я тестовый бот для бизнес-клуба МГЮА', reply_markup=markup)
 

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == '📲 Зарегестрироваться':
        bot.send_message(message.chat.id, 'Отлично, регистрация займёт не больше 5 минут!')
        bot.send_message(message.chat.id, 'Введите ваше имя')
        bot.register_next_step_handler(message, fill_user_name)

    elif message.text == '👀 Просмотреть пользователей':
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ''
        for el in users:
            info += f'{el[1]} {el[2]}, {el[3]}, {el[4]}\n'
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, info)
        
    else:
        bot.send_message(message.chat.id, 'На такую комманду я не запрограммирован..')


def fill_user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите вашу фамилию')
    bot.register_next_step_handler(message, fill_user_surname, name)

def fill_user_surname(message, name):
    surname = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш официальное название вашего ВУЗа, института или колледжа с использованием аббревиатуры')
    bot.register_next_step_handler(message, fill_user_institute, name, surname)

def fill_user_institute(message, name, surname):
    institute = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш возраст')
    bot.register_next_step_handler(message, registration, name, surname, institute)

def registration(message, name, surname, institute):
    age = int(message.text.strip())

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, surname, institute, age) VALUES ("%s", "%s", "%s", "%s")' % (name, surname, institute, age))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('👀 Просмотреть пользователей')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Отлично, мы тебя зарегестрировали!', reply_markup=markup)


bot.polling(none_stop=True)
