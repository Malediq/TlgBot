#!/usr/bin/python3
import re
import time
from value import bot, help, text_maski
from MoiKurs import moikurs
from Napominalka import add_event, my_events, rm_event
from telebot import types
from ipcalc import ipcalc
from parseradresov import parseradr

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("Мой курс")
    item2 = types.KeyboardButton("Мои события")
    item3 = types.KeyboardButton("Помощь")
    item4 = types.KeyboardButton("Маски")
    markup.add(item1, item2, item3, item4)
    bot.send_message(m.chat.id, text="Пиво течет во мне и я един с пивом", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Мой курс':
        x = True
        while x:
            start = time.monotonic()
            x = moikurs(message)
            elapsed = time.monotonic() - start
            if elapsed < 1:
                time.sleep(1 - elapsed)
    elif message.text == 'Помощь':
        help(message)
    elif message.text == 'Мои события':
        try:
            my_events(message)
        except:
            bot.send_message(message.chat.id, 'Событий не запланировано, милорд')
    elif message.text == 'Маски':
        bot.send_message(message.chat.id, text_maski)
    elif message.text[0:7] == 'Удалить' or message.text[0:7] == 'удалить':
        try:
            rm_event(message)
            bot.send_message(message.chat.id, 'Событие удалено, милорд')
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так, милорд')
    elif re.search(r'\d{1,2}[:-]\d{1,2}', message.text) and re.search(r'\d{1,2}[./]\d{1,2}|Сегодня|сегодня|завтра|Завтра|Понедельник|Вторник|Среда|Четверг|Пятница|Суббота|Воскресенье|понедельник|вторник|среда|четверг|пятница|суббота|воскресенье|пн|вт|ср|чт|пт|сб|вс|Пн|Вт|Ср|Чт|Пт|Сб|Вс', message.text):
        try:
            add_event(message)
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так, милорд')
    elif re.match(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}/\d{1,2}', message.text):
        text = ipcalc(message)
        bot.send_message(message.chat.id, text)
    elif message.text == 'Мой id':
        bot.send_message(message.chat.id, f'{message.chat.id}')
    elif re.search(r'улица', message.text) and re.search(r'\d{1,3} км', message.text):
        try:
            parseradr(message)
        except:
            bot.send_message(message.chat.id, 'Пожалуйста, повторите запрос, милорд')
    else:
        bot.send_message(message.chat.id, 'Как скажете, милорд')

bot.polling(none_stop=True, interval=0)
