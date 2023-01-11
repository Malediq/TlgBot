#!/usr/bin/python3

import datetime
from datetime import datetime, timedelta
from value import bot, filename, td
from Napominalka import save_obj, load_obj

def check_events(messageid):
    global td
    now = str(datetime.now())
    ndatetimestr = now[0:16]
    now = datetime.strptime(ndatetimestr, '%Y-%m-%d %H:%M')
    now = now + timedelta(hours=td)
    nowh = now + timedelta(hours=1)
    nowd = now + timedelta(days=1)
    list = []
    list = load_obj()
    for date in list:
        try:
            datstr = date[0:16]
            dat = datetime.strptime(datstr, '%Y-%m-%d %H:%M')
            if dat == nowd:
                bot.send_message(messageid, "Завтра в " + date[11:16] + " " + date[17:])
            elif dat == nowh:
                bot.send_message(messageid, "Через час " + date[17:])
            elif dat == now:
                bot.send_message(messageid, date[17:])
                list.remove(date)
                save_obj(list)
            elif dat < now:
                list.remove(date)
                save_obj(list)
        except:
            list.remove(date)
            save_obj(list)

check_events(560103290)
