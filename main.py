import sqlite3
import telebot
import xlsxwriter
import os
from telebot import types

#C:/Users/glebm/OneDrive/Рабочий стол/programming/pythonProject/photo/
#C:/Users/Глеб/Desktop/Учёба/Прога/PythonProject/photo/

events = {}
event_name = ''

private_club_info = f"""<b>Закрытый Бизнес-клуб </b>💠\n
Это комьюнити сильнейших студентов-предпринимателей и топ-менеджеров крупных компаний.\n
Ценность Закрытого клуба:
• обмен связями и ресурсами
• совместное создание бизнес-проектов
• закрытые встречи с лидирующими на рынке предпринимателями и инвесторами
• сильное комьюнити, настроенное на взаимный рост и нетворкинг\n
Уже сейчас в клубе наши резиденты проводят встречи и запускают совместные бизнес-проекты.\n
Закрытый Бизнес-клуб входит в Объединение Бизнес-клубов России (ОБКР https://обкр.рф), благодаря чему ценность клуба возрастает в несколько раз, а резиденты имеют возможность коммуницировать с резидентами других Закрытых клубов, входящих в Объединение.\n
Закрытый клуб – надежная бизнес-сеть для поддержки и обмена опытом и перспектива для роста.\n
Для вступления необходимо соответствовать минимум одному критерию:
 • наличие собственного бизнеса с оборотом более 6 миллионов в год
 • чистая прибыль одного и более бизнесов от 1 миллиона в год
 • должность топ-менеджера компании\n
Оставь заявку и стань частью закрытого бизнес-комьюнити МГЮА: https://forms.gle/fsKJfsRDkZBPYDdEA \n
*Если вы сами не имеете собственного бизнеса или опыта в топ-менеджменте, но знакомы с потенциальным резидентом для Закрытого клуба, пригласите его к нам, и в случае успешного прохождения отбора, вы сможете посетить одну из наших закрытых встреч.\n
---&gt <a href="https://www.youtube.com/watch?v=hhBjY5_waFo"> Наш промо ролик </a> &lt---"""

public_club_info= f"""<b>⚡️ Бизнес-клуб МГЮА - Люди. Знания. Опыт.</b> \n
• один из лучших студенческих Бизнес-клубов России\n
• бизнес-сообщество ведущего юридического вуза России – Университет имени О.Е. Кутафина (МГЮА) \n
• объединение прорывных студентов: стартаперов, предпринимателей и ТОПов в своей сфере \n
🎯Наша миссия - объединение студентов, достигших результатов в бизнес-среде, для кратного роста! \n
У нас вы будете:
 • проводить открытые и закрытые мероприятия с топами рынка
 • брать интервью у предпринимателей 
 • вести социальные сети на тему бизнеса
 • посещать бизнес-форумы партнеров и многое другое!\n
Бизнес-клуб объединяет способных студентов, заинтересованных в бизнесе, которые вдохновляют, поддерживают друг друга и горят своим делом. \n
Интересуешься бизнесом? Уже являешься предпринимателем или только собираешься выходить на рынок? 
Вступай в Бизнес-клуб! И обязательно подписывайся на наши группу/канал, чтобы не пропустить интересные новости --> <a href="https://vk.com/businessclub_msal"> VK </a> и <a href="https://t.me/business_clubMSAL"> TG </a>"""

user_agreement = f""" """

bot = telebot.TeleBot(token='6624656705:AAEzIo8t1mZAyhcpALT-hzjXQGVBxua5F-Q', skip_pending=True)

btn1 = types.KeyboardButton('📲 Зарегистрироваться')
btn2 = types.KeyboardButton('📋 Мои данные')
btn3 = types.KeyboardButton('👀 Ивенты')
btn4 = types.KeyboardButton('➕ Добавить ивент')
btn5 = types.KeyboardButton('👉 Выбрать ивент')
btn6 = types.KeyboardButton('🔒 Закрытый клуб')
btn7 = types.KeyboardButton('👀 Все пользователи')
btn8 = types.KeyboardButton('📄 Файл')
btn9 = types.KeyboardButton('1. ФИО')
btn10 = types.KeyboardButton('2. Вуз')
btn11 = types.KeyboardButton('3. Курс')
btn12 = types.KeyboardButton('4. Институт (факультет)')
btn13 = types.KeyboardButton('⬅️ Назад')
btn14 = types.KeyboardButton('✏️ Изменить данные')
btn15 = types.KeyboardButton('📃 О клубе')
btn16 = types.KeyboardButton('🅾️ Изменить текст')
btn17 = types.KeyboardButton('🅾️ Изменить фото')
btn18 = types.KeyboardButton('✅ Да')
btn19 = types.KeyboardButton('📤 Отправить рассылку')
btn20 = types.KeyboardButton('⬅️ В меню')
btn21 = types.KeyboardButton('👨‍👨‍👦 Участники')
btn22 = types.KeyboardButton('✍️ Изменить')
btn23 = types.KeyboardButton('❌ Удалить')
btn24 = types.KeyboardButton('✅ Согласен')
btn25 = types.KeyboardButton('❌ Не согласен')



@bot.message_handler(commands=['start', 'hello', 'menu'])
def start_message(message):
    create_table(message, 'users')
    markup = main_menu_markup(message.from_user.id)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я бот бизнес-клуба МГЮА', reply_markup=markup)


@bot.message_handler(commands=['become_admin'])
def become_admin(message):
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, enter_admin_password)


@bot.message_handler(commands=['info'])
def get_public_club_info(message):
    club_info = public_club_info
    inline_markup = types.InlineKeyboardMarkup()
    inline_btn1 = types.InlineKeyboardButton(text='Группа ВК', url = 'https://vk.com/businessclub_msal')
    inline_btn2 = types.InlineKeyboardButton(text='Группа ТГ', url = 'https://t.me/business_clubMSAL')
    inline_markup.add(inline_btn1, inline_btn2)
    bot.send_message(message.chat.id, club_info, reply_markup = inline_markup, parse_mode='html')


@bot.message_handler(commands=['private_info'])
def get_private_club_info(message):
    club_info = private_club_info
    inline_markup = types.InlineKeyboardMarkup()
    inline_btn1 = types.InlineKeyboardButton(text='Наше промо', url = 'https://www.youtube.com/watch?v=hhBjY5_waFo')
    inline_markup.add(inline_btn1)
    bot.send_message(message.chat.id, club_info, reply_markup = inline_markup, parse_mode='html')


def enter_admin_password(message):
    if message.text == 'admin_password':
        change_user_data(message, 'admin_rights', True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn2, btn7, btn4, btn5)
        bot.send_message(message.chat.id, f'Отличо, {message.from_user.first_name}! Теперь ты администратор!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Пароль неверный')


@bot.message_handler(content_types=['text'])
def func(message):
    global event_name
    if message.text == '📲 Зарегистрироваться':
        info_list = get_personal_info(message.from_user.id)
        if info_list:
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы!', reply_markup=markup)
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn24, btn25)
        bot.send_message(message.chat.id, 'Отлично, регистрация займёт не больше 5 минут!\n Но сперва подтвердите согласие на получение сообщений и обработку персональных данных:\n https://docs.google.com/document/d/1QfU-2YYUstVmTLHTee5JebKkd5jEB0eQnOj8SCPIh-I/edit#heading=h.6852be3h0van', reply_markup=markup)
        bot.register_next_step_handler(message, user_agreement)

    elif message.text == '👀 Все пользователи':
        info_list = get_all_info(message)
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
        markup = main_menu_markup(message.from_user.id)
        bot.send_message(message.chat.id, 'Возвращаемся', reply_markup=markup)

    elif message.text == '📃 О клубе':
        club_info = public_club_info
        inline_markup = types.InlineKeyboardMarkup()
        inline_btn1 = types.InlineKeyboardButton(text='Группа ВК', url = 'https://vk.com/businessclub_msal')
        inline_btn2 = types.InlineKeyboardButton(text='Группа ТГ', url = 'https://t.me/business_clubMSAL')
        inline_markup.add(inline_btn1, inline_btn2)
        bot.send_message(message.chat.id, club_info, reply_markup = inline_markup, parse_mode='html')

    elif message.text == '🔒 Закрытый клуб':
        club_info = private_club_info
        inline_markup = types.InlineKeyboardMarkup()
        inline_btn1 = types.InlineKeyboardButton(text='Наше промо', url = 'https://www.youtube.com/watch?v=hhBjY5_waFo')
        inline_markup.add(inline_btn1)
        bot.send_message(message.chat.id, club_info, reply_markup = inline_markup, parse_mode='html')

    elif message.text == '👀 Ивенты' or message.text == '👉 Выбрать ивент':
        if events == {}:
            bot.send_message(message.chat.id, 'Пока что доступных мероприятий нет\nЯ напишу тебе, как только они появятся!')
        else:
            markup = types.InlineKeyboardMarkup()
            i = 1
            events_info = 'Вот все доступные мероприятия:\n'
            for key in events:
                events_info += str(i) + '. ' + key + '\n'
                markup.add(types.InlineKeyboardButton(text= f'{i}', callback_data = key))
                i += 1
            bot.send_message(message.chat.id, events_info, reply_markup=markup)

    elif message.text == '✍️ Изменить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn13)
        bot.send_message(message.chat.id, 'Что меняем?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)
    
    elif message.text == '👨‍👨‍👦 Участники':
        try:
            info_list = get_event_info(message, event_name)
            info = ''
            for el in info_list:
                if el[4] == '':
                    info += f'{el[2]} {el[3]} {el[5]}-й курс\n'
                else:
                    info += f'{el[2]} {el[3]} {el[4]} {el[5]}-й курс\n'
            if info == '':
                markup = main_menu_markup(message.from_user.id)
                bot.send_message(message.chat.id, 'Пока что никто не зарегестрировался на это мероприятие', reply_markup=markup)
                return
            bot.send_message(message.chat.id, info)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(btn8, btn20)
            bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as error:
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, f'Что-то пошло не так\nApiTelegramException: {error}', reply_markup=markup)
        except BaseException as error:
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, f'Что-то пошло не так:\n{error}', reply_markup=markup)

    elif message.text == "📄 Файл":
        markup = main_menu_markup(message.from_user.id)
        try:
            create_xlsx_file(message, event_name)
            file = open('temp.xlsx', 'rb+')
            bot.send_document(message.chat.id, file, reply_markup=markup)
            file.close()
            os.remove('temp.xlsx')
        except telebot.apihelper.ApiTelegramException as error:
            bot.send_message(message.chat.id, f'Что-то пошло не так\nApiTelegramException: {error}', reply_markup=markup)
        except OSError as error:
            bot.send_message(message.chat.id, f'Что-то пошло не так\nOSError: {error}', reply_markup=markup)
        except BaseException as error:
            bot.send_message(message.chat.id, f'Что-то пошло не так:\n{error}', reply_markup=markup)

    elif message.text == '❌ Удалить':
        try:
            conn = sqlite3.connect('database.sql')
            cur = conn.cursor()
            cur.execute('DROP TABLE IF EXISTS %s' % (event_name))
            conn.commit()
            cur.close()
            conn.close()
            src = events[event_name][1]
            os.remove(src)
            del events[event_name]
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, f'Мероприятие \"{event_name}\" успешно удалено', reply_markup=markup)
            event_name = ''
        except sqlite3.Error as error:
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, f'Что-то пошло не так при работе с базой данных:\n{error}', reply_markup=markup)
        except BaseException as error:
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, f'Что-то пошло не так:\n{error}', reply_markup=markup)
        
    elif message.text == '➕ Добавить ивент':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите название нового ивента', reply_markup=markup)
        bot.register_next_step_handler(message, add_event_name)

    elif message.text == '📤 Отправить рассылку':
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton('Я буду', callback_data='register_on_event_callback'))
        info = get_all_info(message)
        for el in info:
            src = events[event_name][1]
            with open(src, 'rb') as photo:
                bot.send_photo(el[1], photo, caption=events[event_name][0], reply_markup=inline_markup)
        reply_markup = main_menu_markup(message.from_user.id)
        bot.send_message(message.chat.id, 'Рассылка отправлена!', reply_markup=reply_markup)

    else:
        bot.send_message(message.chat.id, 'На такую комманду я пока не запрограммирован..')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'register_on_event_callback':
        try:
            global event_name
            conn = sqlite3.connect('database.sql')
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE id = ?', (callback.message.chat.id, ))
            info = cur.fetchall()[0]
            cur.execute('INSERT INTO `%s` (id, chat_id, FIO, institute, faculty, course, admin_rights) VALUES (%s, %s, "%s", "%s", "%s", %s, %s)' % (event_name, info[0], info[1], info[2], info[3], info[4], info[5], info[6]))
            conn.commit()
            cur.close()
            conn.close()
            markup = main_menu_markup(callback.message.chat.id)
            bot.send_message(callback.message.chat.id, 'Отлично, вы записаны на это мероприятие!', reply_markup=markup)
        except sqlite3.IntegrityError:
            markup = main_menu_markup(callback.message.chat.id)
            bot.send_message(callback.message.chat.id, 'Вы уже зарегистрированы!', reply_markup=markup)
        except BaseException as error:
            markup = main_menu_markup(callback.message.chat.id)
            bot.send_message(callback.message.chat.id, f'Что-то пошло не так:\n{error}', reply_markup=markup)
        finally:
            bot.answer_callback_query(callback.id)
            return
    else:
        try:
            event_name = callback.data
            if (event_name in events) == False:
                if not events:
                    markup = main_menu_markup(callback.message.chat.id)
                    bot.send_message(callback.message.chat.id, 'На данный момент доступных мероприятий нет', reply_markup=markup)
                    bot.answer_callback_query(callback.id)
                    return
                else:
                    markup = types.InlineKeyboardMarkup()
                    i = 1
                    events_info = 'Это мероприятие было удалено. Вот актульный список:\n\n'
                    for key in events:
                        events_info += str(i) + '. ' + key + '\n'
                        markup.add(types.InlineKeyboardButton(text= f'{i}', callback_data = key))
                        i += 1
                    bot.send_message(callback.message.chat.id, events_info, reply_markup=markup)
                    bot.answer_callback_query(callback.id)
                    return
            inline_markup = types.InlineKeyboardMarkup()
            inline_markup.add(types.InlineKeyboardButton('Я буду', callback_data='register_on_event_callback'))
            src = events[event_name][1]
            with open(src, 'rb') as photo:
                bot.send_photo(callback.message.chat.id, photo, caption=event_name)
                bot.send_message(callback.message.chat.id, events[event_name][0])
            bot.answer_callback_query(callback.id)
            if is_admin(callback.message.chat.id):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(btn21, btn22, btn23, btn20, btn19)
                bot.send_message(callback.message.chat.id, 'Что дальше?', reply_markup=markup)
        except BaseException as error:
            markup = main_menu_markup(callback.message.chat.id)    
            bot.send_message(callback.message.chat.id, f'Что-то пошло не так:\n{error}', reply_markup=markup) 


def create_xlsx_file(message, event_name):
    info_list = get_event_info(message, event_name)
    try:
        workbook = xlsxwriter.Workbook('temp.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 5)
        bold = workbook.add_format({"bold": True})
        worksheet.write(0, 0, 'ФИО', bold)
        worksheet.write(0, 1, 'Вуз', bold)
        worksheet.write(0, 2, 'Институт', bold)
        worksheet.write(0, 3, 'Курс', bold)
        i = 1
        for el in info_list:
            worksheet.write(i, 0, el[2])
            worksheet.write(i, 1, el[3])
            worksheet.write(i, 2, el[4])
            worksheet.write(i, 3, el[5])
            i += 1
        workbook.close()
    except BaseException as error:
        markup = main_menu_markup(message.from_user.id)    
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{error}', reply_markup=markup)


def is_admin(id):
    info_list = get_personal_info(id)
    if info_list and info_list[0][6] == True:
        return True
    else:
        return False
        

def create_table(message, table_name):
    try:
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `{table_name}` (
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
    except sqlite3.Error as error:
        bot.send_message(message.chat.id, f'{error}\nЧто-то пошло не так при работе с базой данных')
        

def add_event_name(message):
    global event_name
    if type(message.text) != str:
        bot.send_message(message.chat.id, 'Пожалуйста, введи название в виде текста')
        bot.register_next_step_handler(message, add_event_name)
        return
    event_name = message.text
    events[event_name] = ['', '']
    create_table(message, event_name)
    bot.send_message(message.chat.id, 'Отлично! Теперь напиши описание мероприятия')
    bot.register_next_step_handler(message, add_event_description, event_name)


def add_event_description(message, event_name):
    if type(message.text) != str:
        bot.send_message(message.chat.id, 'Пожалуйста, введи описание в виде текста')
        bot.register_next_step_handler(message, add_event_description)
        return
    event_description = message.text
    events[event_name][0] = event_description
    bot.send_message(message.chat.id, 'Отлично! Теперь добавь постер')
    bot.register_next_step_handler(message, add_event_photo, event_name)


def add_event_photo(message, event_name):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        events[event_name][1] = src
        bot.send_message(message.chat.id, f'Фото добавлено. Вот полное описание:')
        with open(src, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=event_name)
            bot.send_message(message.chat.id, events[event_name][0])

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn18)
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)
    except telebot.apihelper.ApiTelegramException as error:
        bot.send_message(message.chat.id, f'{error}\nОписание ивента слишком большое ({len(events[event_name][0])}), опишите мероприятие покороче:')
        bot.register_next_step_handler(message, add_event_description, event_name)
    except Exception as error:
        bot.reply_to(message, f'{error}\nПожалуйста, скиньте постер в виде файла')
        bot.register_next_step_handler(message, add_event_photo, event_name)
    

def change_event(message, event_name):
    try:    
        if message.text == '✅ Да':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(btn19, btn20)
            bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup)

        elif message.text == '🅾️ Изменить текст':
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Ввидите описание заново', reply_markup=markup)
            bot.register_next_step_handler(message, change_event_description, event_name)

        elif message.text == '🅾️ Изменить фото':
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Пришлите фото заново', reply_markup=markup)
            bot.register_next_step_handler(message, change_event_photo, event_name)
    except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn18)
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)

        

def change_event_description(message, event_name):
    try:
        event_description = message.text
        events[event_name][0] = event_description
        src = events[event_name][1]
        with open(src, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=event_name)
            bot.send_message(message.chat.id, events[event_name][0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn18)
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)
    except:
        bot.send_message(message.chat.id, 'Ввидите описание заново, в виде текста')
        bot.register_next_step_handler(message, change_event_description, event_name)


def change_event_photo(message, event_name):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = events[event_name][1]
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.send_message(message.chat.id, f'Фото добавлено. Вот полное описание:')
        with open(src, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=event_name)
            bot.send_message(message.chat.id, events[event_name][0])
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn16, btn17, btn18)
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
        bot.register_next_step_handler(message, change_event, event_name)
    except AttributeError:
        bot.reply_to(message, 'Пожалуйста, скиньте постер в виде файла')
        bot.register_next_step_handler(message, change_event_photo, event_name)
    except BaseException as error:
        bot.send_message(message.chat.id, f'Возникла ошибка в ходе работы бота:\n{error}, func \"start_message\". Пожалуйста, перешилите это сообщение @hlebbezdrozhevoy')
        bot.register_next_step_handler(message, change_event_photo, event_name)


def main_menu_markup(id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info_list = get_personal_info(id)
    if info_list and info_list[0][6] == True:
        markup.add(btn2, btn7, btn4, btn5)
    elif info_list:
        markup.add(btn2, btn3, btn15, btn6)
    else:
        markup.add(btn1, btn15, btn6)
    return markup
    

def get_event_info(message, name):
    try:
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM `%s`' % (name))
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except sqlite3.Error as error:
        markup = main_menu_markup(message.chat.id)
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{error}\nПожалуйста, перешилите это сообщение @hlebbezdrozhevoy', reply_markup=markup)
    except BaseException as error:
        bot.send_message(message.chat.id, f'Возникла ошибка в ходе работы бота:\n{error}, func \"get_event_info\"\nПожалуйста, перешилите это сообщение @hlebbezdrozhevoy')


def get_all_info(message):
    try:
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except sqlite3.Error as error:
        markup = main_menu_markup(message.chat.id)
        bot.send_message(message.chat.id, 'Что-то пошло не так\n{error}', reply_markup=markup)
    except BaseException as error:
        bot.send_message(message.chat.id, f'Возникла ошибка в ходе работы бота:\n{error}, func \"get_all_info\"\nПожалуйста, перешилите это сообщение @hlebbezdrozhevoy')


def get_personal_info(user_id):
    try:
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except sqlite3.Error as error:
        markup = main_menu_markup(user_id)
        bot.send_message(user_id, 'Что-то пошло не так\n{error}', reply_markup=markup)
    except BaseException as error:
        bot.send_message(user_id, f'Возникла ошибка в ходе работы бота:\n{error}, func \"get_personal_info\"\nПожалуйста, перешилите это сообщение @hlebbezdrozhevoy')


def change_user_data_from_input(message, field):
    try:
        if type(message.text) != str:
            bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте снова')
            bot.register_next_step_handler(message, change_user_data_from_input, field)
            return
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

        markup = main_menu_markup(message.from_user.id)
        bot.send_message(message.chat.id, 'Отлично, ваши данные были изменены', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте снова')
        bot.register_next_step_handler(message, change_user_data_from_input, field)
        return



def change_user_data(message, field, data):
    try:
        if field == 'institute' or field == 'faculty':
            data = data.upper()
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        request = sql_request_to_change_data(field)
        cur.execute(request, (data, message.from_user.id))
        conn.commit()
        cur.close()
        conn.close()
    except sqlite3.Error as error:
        markup = main_menu_markup(message.chat.id)
        bot.send_message(message.chat.id, 'Что-то пошло не так\n{error}', reply_markup=markup)
    except BaseException as error:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте снова')
        bot.register_next_step_handler(message, change_user_data, field, data)
        return


def user_agreement(message):
    try:
        if message.text == "✅ Согласен":
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Введите ваше ФИО, полностью', reply_markup=markup)
            bot.register_next_step_handler(message, fill_user_FIO)
        elif message.text == "❌ Не согласен":
            markup = main_menu_markup(message.from_user.id)
            bot.send_message(message.chat.id, 'Что ж, это довольно честно', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Нажите на кнопку "✅ Согласен" или "❌ Не согласен"')
            bot.register_next_step_handler(message, user_agreement)
    except:
        bot.send_message(message.chat.id, 'Нажите на кнопку "✅ Согласен" или "❌ Не согласен"')
        bot.register_next_step_handler(message, user_agreement)


def fill_user_FIO(message):
    try:
        if type(message.text) != str:
            bot.send_message(message.chat.id, 'Введите ваше ФИО, полностью, в виде текста')
            bot.register_next_step_handler(message, fill_user_FIO)
            return
        FIO = message.text
        bot.send_message(message.chat.id, 'Введите официальное название вашего вуза, например "МГЮА"')
        bot.register_next_step_handler(message, fill_user_institute, FIO)
    except:
        bot.send_message(message.chat.id, 'Введите ваше ФИО, полностью, в виде текста')
        bot.register_next_step_handler(message, fill_user_FIO)


def fill_user_institute(message, FIO):
    try:
        institute = message.text
        if institute.upper() == 'МГЮА':
            bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"')
            bot.register_next_step_handler(message, fill_user_faculty, FIO, institute.upper())
        else:
            bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
            bot.register_next_step_handler(message, registration, FIO, institute)
    except:
        bot.send_message(message.chat.id, 'Введите официальное название вашего вуза в виде текста, например "МГЮА"')
        bot.register_next_step_handler(message, fill_user_institute, FIO)


def fill_user_faculty(message, FIO, institute):
    try:    
        faculty = message.text.upper()
        bot.send_message(message.chat.id, 'Введите номер курса, на котором вы обучаетесь в данный момент')
        bot.register_next_step_handler(message, registration, FIO, institute, faculty)
    except:
        bot.send_message(message.chat.id, 'Укажите на каком институте вы обучаетесь в виде аббревиатуры, например "ИБП"')
        bot.register_next_step_handler(message, fill_user_institute, FIO)


def registration(message, FIO, institute, faculty=''):
    try: 
        course_num = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Пожалуйста, введите целое число')
        bot.register_next_step_handler(message, registration, FIO, institute, faculty)
        return
    institute = institute.upper()
    faculty = faculty.upper()
    try:        
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute('INSERT INTO users (id, chat_id, FIO, institute, faculty, course, admin_rights) VALUES (%s, %s, "%s", "%s", "%s", %s, %s)' % (message.from_user.id, message.chat.id, FIO, institute, faculty, course_num, False))
        conn.commit()
        cur.close()
        conn.close()
    except sqlite3.IntegrityError:
        markup = main_menu_markup(message.from_user.id)
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы!', reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn2, btn3, btn15, btn6)
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
