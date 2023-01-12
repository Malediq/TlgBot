#!/usr/bin/python3

import re
import lxml
from value import bot, selenpath as filepath, chromepath
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from math import ceil



cities = {
    'Хабаровск': 'khabarovsk',
    'Владивосток': 'vladivostok'
}

list = []
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.headless = True


def document_initialised(driver):
    return driver.execute_script("return initialised")

def htmlw(file, filepath):
    #write file
    f = open(filepath, 'w', encoding="utf-8")
    f.write(file)
    f.close()

def htmlr(filepath):
    #read file
    f = open(filepath, 'r', encoding="utf-8")
    src = f.read()
    f.close()
    return src

def check_dist(adr1, adr2):
    #get distance between address 1 and address 2
    geolocator = Nominatim(user_agent="Tester")
    location = geolocator.geocode(adr1)
    location2 = geolocator.geocode(adr2)
    koor1 = (location.latitude, location.longitude)
    koor2 = (location2.latitude, location2.longitude)
    distancekm = geodesic(koor1, koor2).kilometers
    return distancekm

def get_start_url(message):
    #get start page url, find in message distance limit and address
    data = re.split(r'[,]', message)

    adr = data[1].lstrip() + ' ' + data[0]

    km = re.findall(r'\d{1,3}', data[2])
    km = km[0]

    if re.search(r'по цене', message):
        price = True
    else:
        price = False

    frp = 'https://www.farpost.ru/'
    city = cities[data[0]]
    #Предложение
    agency2 = 'agentType%5B%5D=agencyFee&'  # агенство с комиссией
    agency1 = 'agentType%5B%5D=agencyNoFee&'  # агенство без комиссии
    personal = 'agentType%5B%5D=privatePerson&' #от собственника
    #Условия
    pets = '' #можно ли с животными
    #Вид квартиры
    flat = 'flatType%5B%5D=1&flatType%5B%5D=2&flatType%5B%5D=3&flatType%5B%5D=4&' #квартира
    gostinka = '' #гостинка
    room = ''  # комната
    #Цена квартиры
    pricemax = ''
    pricemin = ''
    # посуточно или на долгий срок
    if re.search(r'посуточно', message):
        rent = 'rent-apartment/?'
    else:
        rent = 'rent_flats/?'
        flat += 'flatType%5B%5D=5&flatType%5B%5D=6&'
    if re.search(r'без квартир', message):
        flat = ''
        room = 'flatType%5B%5D=room&'
        gostinka = 'flatType%5B%5D=gostinka&'
    if re.search(r'комната', message):
        room = 'flatType%5B%5D=room&'
    if re.search(r'гостинка', message):
        gostinka = 'flatType%5B%5D=gostinka&'
    if re.search(r'от собственника|собственник', message):
        agency2 = ''
        agency1 = ''
    if re.search(r'оптимально', message):
        agency2 = ''
    if re.search(r'животное|с животными|собака|кошка', message):
        pets = 'animalsAllowed=1&'
    if re.search(r'\d[-]\d', message):
        myprice = re.findall(r'\d*[-]\d*', message)
        mmp = re.split(r'[-]', myprice[0])
        pricemax = 'price_max=' + mmp[1] + '&'
        pricemin = 'price_min=' + mmp[0] + '&'
    url = frp + city + '/realty/' + rent + agency2 + agency1 + personal + pets + flat + gostinka + room + pricemax + pricemin
    return url, km, adr, price



def get_page(urlp):
    #get html page
    global chromepath
    ps=''
    driver = webdriver.Chrome(
        executable_path=chromepath,
        options=options
    )
    try:
        driver.get(url=urlp)
        #driver.save_screenshot('primer.png')
        ps = driver.page_source
        WebDriverWait(driver, timeout=10).until(document_initialised)
    except: None
    finally:
        driver.close()
        driver.quit()
    htmlw(ps, filepath)


def get_infa(adr, km, price):
    #get list in format: distance, price, address, rooms, link (default)
    #get list in format: price, distance, address, rooms, link (if price = True)
    global list
    src = htmlr(filepath)
    soup = BeautifulSoup(src, "lxml")
    information = soup.find_all("div", class_='descriptionCell bull-item-content__cell bull-item-content__description-cell js-description-block')
    for inf in information:
        adresk = inf.find("div", class_='bull-item-content__subject-container').find("a")
        ssyl = 'https://www.farpost.ru' + adresk.get("href")
        adresk = re.split(r'[,] ', adresk.get_text())
        kom = adresk[0]
        if re.search(r'кор[.]', adresk[1]):
            adresk = re.split(r'кор[.]', adresk[1])
            adres = 'Хабаровск ' + adresk[0]
        else: adres = 'Хабаровск ' + adresk[1]
        cena = inf.find("div", class_='price-block__final-price finalPrice').find("span")
        try:
            dist = check_dist(adr, adres)
            if dist <= int(km):
                if price == True:
                    infa = f"{cena.get_text()}, {dist:.2f} км, {adres}, {kom}\n{ssyl}\n"
                else:
                    infa = f"{dist:.2f} км, {cena.get_text()}, {adres}, {kom}\n{ssyl}\n"
                list.append(infa)
        except: None



def kolvo_pr(filepath):
    #get number of pages
    src = htmlr(filepath)
    soup = BeautifulSoup(src, "lxml")
    kolvoo = soup.find("div", class_='bzr-viewdir-status__subscription').find("span").get("data-count")
    kolvo = ceil(int(kolvoo)/50) + 1
    return kolvo


def parseradr(message):
    #get rent flats or aparments in radius
    global list
    bot.send_message(message.chat.id, 'Ожидайте милорд, ищу для Вас подходящие квартиры')
    starturl = get_start_url(message.text)
    url = starturl[0]
    adr = starturl[2]
    km = starturl[1]
    price = starturl[3]
    get_page(url)
    get_infa(adr, km, price)
    n = kolvo_pr(filepath)
    url += 'page='
    for i in range(2, n):
        bot.send_message(message.chat.id, 'Я не умер')
        urlp = url + str(i)
        get_page(urlp)
        get_infa(adr, km)
    list = sorted(list)
    bot.send_message(message.chat.id, 'Квартиры найдены и отсортированы, милорд')
    for i in list:
        bot.send_message(message.chat.id, i)
