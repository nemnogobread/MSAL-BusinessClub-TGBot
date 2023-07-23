import telebot

bot = telebot.TeleBot('6556691353:AAG54E4sdBBD79j3pX2x_WDSfrKspp5hepM')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!')


bot.polling(none_stop=True)
