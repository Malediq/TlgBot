#!/usr/bin/python3

import telebot
from ipcalc import mask2cc, perevod10cc
#Enter your bot id
bot = telebot.TeleBot('')
#Path to Napominalka file
filename = '/home/events.pkl'
#Path to Parseradresov and chromium driver
selenpath = '/home/index_selen.html'
chromepath='/home/chromedriver'
#Timedelta between hostserver and client
td=7
#Help
text_help = 'Введите напоминание в формате:\n' \
            '<Время и Дата> <Событие>\n' \
            'Дата: (d)d.(/)(m)m\n' \
            '      (d)d.( /)(m)m.( /)yyyy\n' \
            '      Д(д)ень недели\n' \
            '      пн|вт|ср|чт|пт|сб|вс\n' \
            'Пример: 03 12/2020, 3.12,\n ' \
            '        Пн (ближайший следующий)\n' \
            '        завтра, понедельник\n' \
            'Время: (h)h:( -)(m)m\n' \
            'Пример времени: 12 40, 3:11\n' \
            'Мои события вывод: ' \
            'yyyy-mm-dd hh:mm <Событие>\n'

text_maski = 'BM  Netmask             |Wildcard\n'

for i in range(0, 33):
    maski = mask2cc(i)
    if i==0:
        text_maski += str(i) + '   - ' + perevod10cc(maski[0]) + '                 |' + perevod10cc(maski[1]) + '\n'
    elif i>0 and i<9:
        text_maski += str(i) + '   - ' + perevod10cc(maski[0]) + '             |' + perevod10cc(maski[1]) + '\n'
    elif i==9:
        text_maski += str(i) + '   - ' + perevod10cc(maski[0]) + '         |' + perevod10cc(maski[1]) + '\n'
    elif i>9 and i<17:
        text_maski += str(i) + ' - ' + perevod10cc(maski[0]) + '         |' + perevod10cc(maski[1]) + '\n'
    elif i>16 and i<25:
        text_maski += str(i) + ' - ' + perevod10cc(maski[0]) + '     |' + perevod10cc(maski[1]) + '\n'
    elif i>24 and i<33:
        text_maski += str(i) + ' - ' + perevod10cc(maski[0]) + ' |' + perevod10cc(maski[1]) + '\n'
