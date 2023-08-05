import sqlite3
import telebot
from telebot import types

event = ''

bot = telebot.TeleBot('6556691353:AAET9cz_wPIog5m2n25D8nnQXy-h9GXCIlk', skip_pending=True)


@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id int auto_increment primary key,
                chat_id int,
                FIO varchar(50),
                institute varchar(50),
                faculty varchar(50),
                course int
                )""")
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📲 Зарегестрироваться')
    btn2 = types.KeyboardButton('📋 Просмотреть мои данные')
    btn3 = types.KeyboardButton('👀 Просмотреть доступные мероприятия')
    if get_personal_info(message.from_user.id):
        markup.add(btn2, btn3)
    else:
        markup.add(btn1)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я тестовый бот для бизнес-клуба МГЮА', reply_markup=markup)
 

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


@bot.message_handler(content_types=['text'])
def func(message):
    
    if message.text == '📲 Зарегестрироваться':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Отлично, регистрация займёт не больше 5 минут!', reply_markup=markup)
        bot.send_message(message.chat.id, 'Введите ваше ФИО (полностью)')
        bot.register_next_step_handler(message, fill_user_FIO)

    elif message.text == '👀 Просмотреть пользователей':
        info_list = get_all_info()
        info = ''
        for el in info_list:
            if el[4] == '':
                info += f'{el[2]}, {el[3]}, {el[5]}-й курс\n'
            else:
                info += f'{el[2]}, {el[3]}, {el[4]}, {el[5]}-й курс\n'
        bot.send_message(message.chat.id, info)

    elif message.text == '📋 Просмотреть мои данные':
        info_list = get_personal_info(message.from_user.id)
        if info_list[0][4] == '':
            info = f'ID: {info_list[0][0]}\nchat_ID: {info_list[0][1]}\n{info_list[0][2]}\n{info_list[0][3]}, {info_list[0][5]}-й курс'
        else:
            info = f'ID: {info_list[0][0]}\nchat_ID: {info_list[0][1]}\n{info_list[0][2]}\n{info_list[0][3]}, {info_list[0][4]}, {info_list[0][5]}-й курс'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('✏️ Изменить данные')
        markup.add(btn1)
        bot.send_message(message.chat.id, info, reply_markup=markup)

    elif  message.text == '✏️ Изменить данные':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('1. ФИО')
        btn2 = types.KeyboardButton('2. ВУЗ')
        btn3 = types.KeyboardButton('3. Курс')
        btn4 = types.KeyboardButton('4. Институт (факультет)')
        btn5 = types.KeyboardButton('⬅️ Назад')
        info_list = get_personal_info(message.from_user.id)
        if info_list[0][4] == '':
            markup.add(btn1, btn2, btn3, btn5)
        else:
            markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Что именно вы хотите изменить?', reply_markup=markup)

    elif  message.text == '1. ФИО':
        bot.send_message(message.chat.id, 'Введите ваше ФИО (полностью)')
        bot.register_next_step_handler(message, change_user_data, 'FIO')

    elif  message.text == '2. ВУЗ':
        bot.send_message(message.chat.id, 'Введите официальное название вашего ВУЗа, например "МГЮА"')
        bot.register_next_step_handler(message, change_user_data, 'institute')

    elif  message.text == '3. Институт (факультет)':
        bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"')
        bot.register_next_step_handler(message, change_user_data, 'faculty')

    elif  message.text == '4. Курс':
        bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
        bot.register_next_step_handler(message, change_user_data, 'course')

    elif  message.text == '⬅️ Назад':
        pass

    elif message.text == '👀 Просмотреть доступные мероприятия':
        if event == '':
            bot.send_message(message.chat.id, 'Пока что доступных мероприятий нет\nЯ напишу тебе, как только они появятся!')
        else:
            pass

    else:
        bot.send_message(message.chat.id, 'На такую комманду я пока не запрограммирован..')


def get_all_info():
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info


def get_personal_info(user_id):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
    info = cur.fetchall()
    cur.close()
    conn.close()
    return info


def change_user_data(message, field):
    data = message.text
    if field == 'course':
        try: 
            data = int(data)
        except ValueError:
            bot.send_message(message.chat.id, 'Пожалуйста, введите целое число')
            bot.register_next_step_handler(message, change_user_data, 'course')
            return
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    request = sql_request_to_change_data(field)
    cur.execute(request, (data, message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📲 Зарегестрироваться')
    btn2 = types.KeyboardButton('📋 Просмотреть мои данные')
    btn3 = types.KeyboardButton('👀 Просмотреть доступные мероприятия')
    if get_personal_info(message.from_user.id):
        markup.add(btn2, btn3)
    else:
        markup.add(btn1)
    bot.send_message(message.chat.id, 'Отлично, ваши данные были изменены', reply_markup=markup)


def fill_user_FIO(message):
    FIO = message.text
    bot.send_message(message.chat.id, 'Введите официальное название вашего ВУЗа, например "МГЮА"')
    bot.register_next_step_handler(message, fill_user_institute, FIO)


def fill_user_institute(message, FIO):
    institute = message.text
    if institute.upper() == 'МГЮА':
        bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"')
        bot.register_next_step_handler(message, fill_user_faculty, FIO, institute.upper())
    else:
        bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
        bot.register_next_step_handler(message, registration, FIO, institute)


def fill_user_faculty(message, FIO, institute):
    faculty = message.text.upper()
    bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
    bot.register_next_step_handler(message, registration, FIO, institute, faculty)


def registration(message, FIO, institute, faculty=''):
    try: 
        course_num = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите целое число')
        bot.register_next_step_handler(message, registration, FIO, institute, faculty)
        return
        
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (id, chat_id, FIO, institute, faculty, course) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % (message.from_user.id, message.chat.id, FIO, institute, faculty, course_num))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📋 Просмотреть мои данные')
    btn2 = types.KeyboardButton('👀 Просмотреть доступные мероприятия')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Отлично, мы тебя зарегестрировали!', reply_markup=markup)


def sql_request_to_change_data(field):
    if field == 'FIO':
        return 'UPDATE users SET FIO = ? WHERE id = ?'
    elif field == 'institute':
        return 'UPDATE users SET institute = ? WHERE id = ?'
    elif field == 'faculty':
        return 'UPDATE users SET faculty = ? WHERE id = ?'
    elif field == 'course':
        return 'UPDATE users SET course = ? WHERE id = ?'


bot.polling(none_stop=True)
