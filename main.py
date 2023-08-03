import sqlite3
import telebot
from telebot import types

event = ''

bot = telebot.TeleBot('6556691353:AAET9cz_wPIog5m2n25D8nnQXy-h9GXCIlk', skip_pending=True)

@bot.message_handler(commands=['become_admin'])
def become_admin(message):
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, enter_admin_password)

def enter_admin_password(message):
    if message.text == 'admin_password':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('➕ Добвать мероприятие')
        btn2 = types.KeyboardButton('✏️ Изменить мероприятие')
        btn3 = types.KeyboardButton('❌ Удалить мероприятие')
        btn4 = types.KeyboardButton('👀 Просмотреть пользователей')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, f'Отличо, {message.from_user.first_name}! Теперь ты администратор!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Пароль неверный')


@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id int auto_increment primary key,
                FIO varchar(50),
                institute varchar(50),
                faculty varchar(50),
                course int,
                user_id int
                )""")
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📲 Зарегестрироваться')
    markup.add(btn1)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я тестовый бот для бизнес-клуба МГЮА', reply_markup=markup)
 

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == '📲 Зарегестрироваться':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Отлично, регистрация займёт не больше 5 минут!', reply_markup=markup)
        bot.send_message(message.chat.id, 'Введите ваше ФИО (полностью)')
        bot.register_next_step_handler(message, fill_user_FIO)

    elif message.text == '👀 Просмотреть пользователей':
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ''
        for el in users:
            if el[3] == '':
                info += f'{el[1]}, {el[2]}, {el[4]}-й курс\n'
            else:
                info += f'{el[1]}, {el[2]}, {el[3]}, {el[4]}-й курс\n'
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, info)

    elif message.text == '📋 Просмотреть мои данные':
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ''
        for el in users:
            if el[5] == message.from_user.id:
                if el[3] == '':
                    info += f'{el[1]}, {el[2]}, {el[4]}-й курс\n'
                else:
                    info += f'{el[1]}, {el[2]}, {el[3]}, {el[4]}-й курс\n'
                break
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, info)

    elif message.text == '👀 Просмотреть доступные мероприятия':
        if event == '':
            bot.send_message(message.chat.id, 'Пока что доступных мероприятий нет\nЯ напишу тебе, как только они появятся!')
        else:
            pass

    else:
        bot.send_message(message.chat.id, 'На такую комманду я пока не запрограммирован..')


def fill_user_FIO(message):
    FIO = message.text
    bot.send_message(message.chat.id, 'Введите официальное название вашего ВУЗа, например "МГЮА"')
    bot.register_next_step_handler(message, fill_user_institute, FIO)

def fill_user_institute(message, FIO):
    institute = message.text
    if institute.upper() == 'МГЮА':
        bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"')
        bot.register_next_step_handler(message, fill_user_faculty, FIO, institute)
    else:
        bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
        bot.register_next_step_handler(message, registration, FIO, institute)

def fill_user_faculty(message, FIO, institute):
    faculty = message.text
    bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
    bot.register_next_step_handler(message, registration, FIO, institute, faculty)

def registration(message, FIO, institute, faculty=''):
    course_num = int(message.text)

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (FIO, institute, faculty, course, user_id) VALUES ("%s", "%s", "%s", "%s", "%s")' % (FIO, institute, faculty, course_num, message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📋 Просмотреть мои данные')
    btn2 = types.KeyboardButton('👀 Просмотреть доступные мероприятия')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Отлично, мы тебя зарегестрировали!', reply_markup=markup)


bot.polling(none_stop=True)
