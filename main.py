import sqlite3
import telebot
from telebot import types

events = {}
event_name = ''

bot = telebot.TeleBot('6556691353:AAET9cz_wPIog5m2n25D8nnQXy-h9GXCIlk', skip_pending=True)

btn1 = types.KeyboardButton('📲 Зарегистрироваться')
btn2 = types.KeyboardButton('📋 Мои данные')
btn3 = types.KeyboardButton('👀 Мероприятия')
btn4 = types.KeyboardButton('➕ Добавить ивент')
btn5 = types.KeyboardButton('✏️ Изменить ивент')
btn6 = types.KeyboardButton('❌ Удалить ивент')
btn7 = types.KeyboardButton('👀 Все пользователи')
btn9 = types.KeyboardButton('1. ФИО')
btn10 = types.KeyboardButton('2. Вуз')
btn11 = types.KeyboardButton('3. Курс')
btn12 = types.KeyboardButton('4. Институт (факультет)')
btn13 = types.KeyboardButton('⬅️ Назад')
btn14 = types.KeyboardButton('✏️ Изменить данные')
btn15 = types.KeyboardButton('📃 О клубе')
btn16 = types.KeyboardButton('🅾️ Нет, изменить текст') 
btn17 = types.KeyboardButton('🅾️ Нет, изменить фото')
btn18 = types.KeyboardButton('✅ Да, всё верно')
btn19 = types.KeyboardButton('📤 Отправить рассылку')
btn20 = types.KeyboardButton('⬅️ В меню')



@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    create_table(message, 'users')
    markup = main_menu_markup(message)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я тестовый бот для бизнес-клуба МГЮА', reply_markup=markup)
 

@bot.message_handler(commands=['become_admin'])
def become_admin(message):
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, enter_admin_password)

def enter_admin_password(message):
    if message.text == 'admin_password':
        change_user_data(message, 'admin_rights', True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn2, btn7, btn15, btn4, btn5, btn6)
        bot.send_message(message.chat.id, f'Отличо, {message.from_user.first_name}! Теперь ты администратор!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Пароль неверный')


@bot.message_handler(content_types=['text'])
def func(message):
    
    if message.text == '📲 Зарегистрироваться':
        info_list = get_personal_info(message.from_user.id)
        if info_list:
            markup = markup = main_menu_markup(message)
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы!', reply_markup=markup)
            return
        
        markup = types.ReplyKeyboardRemove()
        
        bot.send_message(message.chat.id, 'Отлично, регистрация займёт не больше 5 минут!', reply_markup=markup)
        bot.send_message(message.chat.id, 'Введите ваше ФИО (полностью)')
        bot.register_next_step_handler(message, fill_user_FIO)

    elif message.text == '👀 Все пользователи':
        info_list = get_all_info()
        info = ''
        for el in info_list:
            if el[4] == '':
                info += f'{el[2]} {el[3]} {el[5]}-й курс\n'
            else:
                info += f'{el[2]} {el[3]} {el[4]} {el[5]}-й курс\n'
        bot.send_message(message.chat.id, info)

    elif message.text == '📋 Мои данные':
        info_list = get_personal_info(message.from_user.id)
        if info_list[0][4] == '':
            info = f'{info_list[0][2]}\n{info_list[0][3]} {info_list[0][5]}-й курс'
        else:
            info = f'{info_list[0][2]}\n{info_list[0][3]} {info_list[0][4]} {info_list[0][5]}-й курс'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn13, btn14)
        bot.send_message(message.chat.id, info, reply_markup=markup)

    elif  message.text == '✏️ Изменить данные':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        info_list = get_personal_info(message.from_user.id)
        if info_list[0][4] == '':
            markup.add(btn9, btn10, btn11, btn13)
        else:
            markup.add(btn9, btn10, btn11, btn12, btn13)
        bot.send_message(message.chat.id, 'Что именно вы хотите изменить?', reply_markup=markup)

    elif  message.text == '1. ФИО':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите ваше ФИО (полностью)', reply_markup=markup)
        bot.register_next_step_handler(message, change_user_data_from_input, 'FIO')

    elif  message.text == '2. Вуз':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите официальное название вашего вуза, например "МГЮА"', reply_markup=markup)
        bot.register_next_step_handler(message, change_user_data_from_input, 'institute')

    elif  message.text == '3. Курс':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент', reply_markup=markup)
        bot.register_next_step_handler(message, change_user_data_from_input, 'course')

    elif  message.text == '4. Институт (факультет)':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"', reply_markup=markup)
        bot.register_next_step_handler(message, change_user_data_from_input, 'faculty')


    elif  message.text == '⬅️ Назад' or message.text == '⬅️ В меню':
        markup = main_menu_markup(message)
        bot.send_message(message.chat.id, 'Возвращаемся', reply_markup=markup)

    elif message.text == '📃 О клубе':
        club_info = 'Здесь будет полезная информация о бизнес-клубе МГЮА\nНо пока тут только напоминание, что надо выпрямить спину'
        inline_markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Наша группа', url = 'https://vk.com/businessclub_msal')
        inline_markup.add(btn)
        bot.send_message(message.chat.id, club_info, reply_markup = inline_markup)

    elif message.text == '👀 Мероприятия':
        if events == {}:
            bot.send_message(message.chat.id, 'Пока что доступных мероприятий нет\nЯ напишу тебе, как только они появятся!')
        else:
            pass

    elif message.text == '➕ Добавить ивент':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите название нового ивента', reply_markup=markup)
        bot.register_next_step_handler(message, add_event_name)

    elif message.text == '📤 Отправить рассылку':
        info = get_all_info()
        for el in info:
            bot.send_message(el[1], 'Тестируется рассылка, не обращайте внимания')
            src = events[event_name][1]
            with open(src, 'rb') as photo:
                bot.send_photo(el[1], photo, caption=events[event_name][0])
        markup = main_menu_markup(message)
        bot.send_message(message.chat.id, 'Рассылка отправлена!', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'На такую комманду я пока не запрограммирован..')


def create_table(message, table_name):
    try:
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                    id int auto_increment primary key,
                    chat_id int,
                    FIO varchar(50),
                    institute varchar(50),
                    faculty varchar(50),
                    course int,
                    admin_rights bool
                    )""")
        conn.commit()
        cur.close()
        conn.close()
    except sqlite3.Error:
        bot.send_message(message.chat.id, 'Что-то пошло не так при работе с базой данных')


def add_event_name(message):
    global event_name
    event_name = message.text
    events[event_name] = ['', '']
    create_table(message, event_name)
    bot.send_message(message.chat.id, 'Отлично! Теперь напиши описание мероприятия')
    bot.register_next_step_handler(message, add_event_description, event_name)


def add_event_description(message, event_name):
    event_description = message.text
    events[event_name][0] = event_description
    bot.send_message(message.chat.id, 'Отлично! Теперь добавь постер')
    bot.register_next_step_handler(message, add_event_picture, event_name)


def add_event_picture(message, event_name):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'C:/Users/Глеб/Desktop/Учёба/Прога/PythonProject/photo/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        events[event_name][1] = src
        bot.send_message(message.chat.id, f'Фото добавлено. Вот полное описание:')
        with open(src, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=events[event_name][0])

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn18)
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)
    except Exception as error:
        bot.reply_to(message, error)
    

def change_event(message, event_name):
    if message.text == '✅ Да, всё верно':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn19, btn20)
        bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup)

    elif message.text == '🅾️ Нет, изменить текст':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ввидите описание заново', reply_markup=markup)
        bot.register_next_step_handler(message, change_event_description, event_name)

    elif message.text == '🅾️ Нет, изменить фото':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Пришлите фото заново', reply_markup=markup)
        bot.register_next_step_handler(message, change_event_photo, event_name)
        

def change_event_description(message, event_name):
    event_description = message.text
    events[event_name][0] = event_description
    src = events[event_name][1]
    with open(src, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=events[event_name][0])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn16, btn17, btn18)
    bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
    bot.register_next_step_handler(message, change_event, event_name)


def change_event_photo(message, event_name):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = events[event_name][1]
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.send_message(message.chat.id, f'Фото добавлено. Вот полное описание:')
        with open(src, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=events[event_name][0])
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn18)
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)
    except Exception as error:
        bot.reply_to(message, error)




def main_menu_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info_list = get_personal_info(message.from_user.id)
    if info_list and info_list[0][6] == True:
        markup.add(btn2, btn7, btn15, btn4, btn5, btn6)
    elif info_list:
        markup.add(btn2, btn3, btn15)
    else:
        markup.add(btn1, btn15)
    return markup
    

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


def change_user_data_from_input(message, field):
    data = message.text
    if field == 'course':
        try: 
            data = int(data)
        except ValueError:
            bot.send_message(message.chat.id, 'Пожалуйста, введите целое число')
            bot.register_next_step_handler(message, change_user_data_from_input, 'course')
            return
            
    change_user_data(message, field, data)
    info = get_personal_info(message.from_user.id)

    if field == 'institute' and data.upper() == 'МГЮА':
        bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"')
        bot.register_next_step_handler(message, change_user_data_from_input, 'faculty')
        return
    elif field == 'institute' and info[0][3] != 'МГЮА' and info[0][4] != '':
        change_user_data(message, 'faculty', '')

    markup = main_menu_markup(message)
    bot.send_message(message.chat.id, 'Отлично, ваши данные были изменены', reply_markup=markup)


def change_user_data(message, field, data):
    if field == 'institute' or field == 'faculty':
        data = data.upper()
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    request = sql_request_to_change_data(field)
    cur.execute(request, (data, message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()


def fill_user_FIO(message):
    FIO = message.text
    bot.send_message(message.chat.id, 'Введите официальное название вашего вуза, например "МГЮА"')
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
    institute = institute.upper()
    faculty = faculty.upper()
    try:        
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('INSERT INTO users (id, chat_id, FIO, institute, faculty, course, admin_rights) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (message.from_user.id, message.chat.id, FIO, institute, faculty, course_num, False))
        conn.commit()
        cur.close()
        conn.close()
    except sqlite3.IntegrityError:
        markup = main_menu_markup(message)
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы!', reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn2, btn3, btn15)
    bot.send_message(message.chat.id, 'Отлично, мы тебя зарегистрировали!', reply_markup=markup)


def sql_request_to_change_data(field):
    if field == 'FIO':
        return 'UPDATE users SET FIO = ? WHERE id = ?'
    elif field == 'institute':
        return 'UPDATE users SET institute = ? WHERE id = ?'
    elif field == 'faculty':
        return 'UPDATE users SET faculty = ? WHERE id = ?'
    elif field == 'course':
        return 'UPDATE users SET course = ? WHERE id = ?'
    elif field == 'admin_rights':
        return 'UPDATE users SET admin_rights = ? WHERE id = ?'

if __name__ == '__main__':
    bot.polling(none_stop=True)
