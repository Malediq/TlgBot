#!/usr/bin/python3

import requests
from value import bot, kp, dollarsumm


def moikurs(message):
    listd = {
        'до 100,00': 0,
        'до 500,00': 100,
        'до 1000,00': 500,
        'до 10000,00': 1000,
        'до 50000,00': 10000,
        'до 100000,00': 50000,
        'до 500000,00': 100000,
        'до 1000000,00': 500000,
        'от 1000000,00': 1000000}
    for i, j in listd.items():
        if dollarsumm > j:
            usl = i
    myheaders = {}
    myheaders['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    source = requests.get("https://siteapi.vtb.ru/api/currencyrates/table?category=3&type=1", headers=myheaders)
    html = source.text
    x=True
    try:
        kursP = float(html[(html.find(usl)-35):(html.find(usl)-30)])
        raznica = abs(kursP - kp)
        if kursP > kp:
            bot.send_message(message.chat.id, str(kursP) + '(+' + str(round(raznica, 2)) + ')')
            bot.send_message(message.chat.id, 'Прибыль составит:\t' + str(round(raznica, 2) * dollarsumm))
        elif kursP == kp:
            bot.send_message(message.chat.id, kursP)
        else:
            bot.send_message(message.chat.id, str(kursP) + '(-' + str(round(raznica, 2)) + ')')
            bot.send_message(message.chat.id, 'Убыток составит: ' + str(round(raznica, 2) * dollarsumm))
        x=False
    except:
        x=x
    return x
