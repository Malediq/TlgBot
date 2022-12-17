#!/usr/bin/python3

import pickle
import re
from value import bot, filename
from datetime import datetime, timedelta


def save_obj(obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=0)
        f.close()


def load_obj():
    with open(filename, 'rb') as f:
        z = pickle.load(f)
        f.close()
        return z

def day_week(dwstring):
    now = datetime.now()
    now += timedelta(hours=7)
    dayn = now.weekday()
    if dwstring == 'завтра' or dwstring == 'Завтра':
        needd = dayn+1
    elif dwstring == 'пн' or dwstring == 'Пн' or dwstring == 'понедельник' or dwstring == 'Понедельник':
        needd = 0
    elif dwstring == 'вт' or dwstring == 'Вт' or dwstring == 'вторник' or dwstring == 'Вторник':
        needd = 1
    elif dwstring == 'ср' or dwstring == 'Ср' or dwstring == 'среда' or dwstring == 'Среда':
        needd = 2
    elif dwstring == 'чт' or dwstring == 'Чт' or dwstring == 'четверг' or dwstring == 'Четверг':
        needd = 3
    elif dwstring == 'пт' or dwstring == 'Пт' or dwstring == 'пятница' or dwstring == 'пятница':
        needd = 4
    elif dwstring == 'сб' or dwstring == 'Сб' or dwstring == 'суббота' or dwstring == 'Суббота':
        needd = 5
    elif dwstring == 'вс' or dwstring == 'Вс' or dwstring == 'воскресенье' or dwstring == 'Воскресенье':
        needd = 6
    if dayn >= needd:
        needd += 7
    td = needd - dayn
    now += timedelta(days=td)
    return str(now)

def add_event(message):
    # 11 11 11 11 1111 Event
    # 11 11 завтра Event
    # 11 11 пн(вт,ср,чт,пт,сб,вс) Event
    # 012345678901234567
    # 2022-10-24 18:35:25.365862
    resultd = re.findall(r'\d{1,2}[./]\d{1,2}[./]\d{4}|\d{1,2}[./]\d{1,2}|завтра|Завтра|Понедельник|Вторник|Среда|Четверг|Пятница|Суббота|Воскресенье|понедельник|вторник|среда|четверг|пятница|суббота|воскресенье|пн|вт|ср|чт|пт|сб|вс|Пн|Вт|Ср|Чт|Пт|Сб|Вс', message.text)
    if re.match(r'завтра|Завтра|Понедельник|Вторник|Среда|Четверг|Пятница|Суббота|Воскресенье|понедельник|вторник|среда|четверг|пятница|суббота|воскресенье|пн|вт|ср|чт|пт|сб|вс|Пн|Вт|Ср|Чт|Пт|Сб|Вс', resultd[0]):
        mydate = day_week(resultd[0])
        myyear = mydate[0:4]
        mymounth = mydate[5:7]
        myday = mydate[8:10]
    elif re.match(r'\d{1,2}[./]\d{1,2}[./]\d{4}', resultd[0]):
        mydate = re.split(r'[ ./-]', resultd[0])
        myyear = mydate[2]
        mymounth = mydate[1]
        myday = mydate[0]
    elif re.match(r'\d{1,2}[./]\d{1,2}', resultd[0]):
        mydate = re.split(r'[.]', resultd[0])
        myyear = str(datetime.now())[0:4]
        mymounth = mydate[1]
        if int(mymounth) < 10 and len(mymounth) < 2:
            mymounth = '0' + mymounth
        myday = mydate[0]
        if int(myday) < 10 and len(myday) < 2:
            myday = '0' + myday
    else: None
    # ищем время myminute, myhour
    resultt = re.findall(r'\d{1,2}[:-]\d{1,2}', message.text)
    mytime = re.split(r'[:-]', resultt[0])
    myhour = mytime[0]
    if int(myhour) < 10 and len(myhour) < 2:
        myhour = '0' + myhour
    myminute = mytime[1]
    if int(myminute) < 10 and len(myminute) < 2:
        myminute = '0' + myminute
    resdel = re.split(resultd[0], message.text)
    resdel = ' '.join(resdel)
    resdel = re.split(r'\d{1,2}[:-]\d{1,2}', resdel)
    delo = resdel[1]
    list = []
    try:
        list = load_obj()
    except: None
    try:
        list.append(myyear + "-" + mymounth + "-" + myday + " " + myhour + ":" + myminute + "   " + delo.lstrip())
        list = sorted(list)
        save_obj(list)
    except: None

def rm_event(message):
    # Удалить 1,2,3,4,5-10
    # 01234567890123456789
    list = []
    list = load_obj()
    result = re.findall(r'\d+', message.text)
    diap = re.findall(r'\d+-\d+', message.text)
    r1 = []
    r2 = []
    for i in diap:
        r1.append(re.split(r'-', i))
    for i in r1:
        for j in range(int(i[0]), int(i[1]) + 1):
            k = str(j)
            result.append(k)
    result = set(result)
    for i in result:
        k = int(i)-1
        r2.append(k)
    r2.sort(reverse=True)
    for c in r2:
        list.pop(c)
    save_obj(list)

def my_events(message):
    list = []
    list = load_obj()
    i=0
    txt=''
    for text in list:
        i+=1
        txt += (str(i) + ". " + text + "\n")
    bot.send_message(message.chat.id, txt)
