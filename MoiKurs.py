#!/usr/bin/python3

import requests
from value import bot


def moikurs(message):
    myheaders = {}
    myheaders['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    source = requests.get("https://siteapi.vtb.ru/api/currencyrates/table?category=3&type=1", headers=myheaders)
    html = source.text
    x=True
    try:
        kursP = float(html[(html.find('до 10000,00')-35):(html.find('до 10000,00')-30)])
        raznica = abs(kursP - 65.72)
        if kursP > 65.72:
            bot.send_message(message.chat.id, str(kursP) + '(+' + str(round(raznica, 2)) + ')')
            bot.send_message(message.chat.id, 'Крестьяне зарабатывают деньги, милорд:\t' + str(round(raznica, 2) * 1111))
        elif kursP == 65.72:
            bot.send_message(message.chat.id, kursP)
        else:
            bot.send_message(message.chat.id, str(kursP) + '(-' + str(round(raznica, 2)) + ')')
            bot.send_message(message.chat.id, 'Казна пустеет, милорд: ' + str(round(raznica, 2) * 1111))
        x=False
    except:
        x=x
    return x
