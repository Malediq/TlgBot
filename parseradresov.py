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
    'Хабаровск': 'khabarovsk'
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
    city = cities[data[0]]
    adr = data[1].lstrip() + ' ' + data[0]
    km = re.findall(r'\d{1,3}', data[2])
    km = km[0]
    url = 'https://www.farpost.ru/'
    if re.search(r'посуточно', message):
        urlp = url + city + '/realty/rent-apartment/?flatType%5B%5D=1&flatType%5B%5D=2&flatType%5B%5D=3&flatType%5B%5D=4'
    else:
        url = url + city + '/realty/rent_flats/'
        if re.search(r'животное|с животными|собака|кошка', message):
            urlp = url + '?animalsAllowed=1'
            if re.search(r'квартира', message):
                urlp += '&flatType%5B%5D=1&flatType%5B%5D=2&flatType%5B%5D=3&flatType%5B%5D=4'
        else:
            urlp = url
            if re.search(r'квартира', message):
                urlp += '?flatType%5B%5D=1&flatType%5B%5D=2&flatType%5B%5D=3&flatType%5B%5D=4'
    return urlp, km, adr



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


def get_infa(adr, km):
    #get list in format: distance, address, rooms, price, link
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
                infa = f"{dist:.2f} км, {adres}, {kom}, {cena.get_text()}\n{ssyl}\n"
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
    #get rent flats html
    global list
    bot.send_message(message.chat.id, 'Ожидайте милорд, ищу для Вас подходящие квартиры')
    starturl = get_start_url(message.text)
    url = starturl[0]
    adr = starturl[2]
    km = starturl[1]
    get_page(url)
    get_infa(adr, km)
    print(starturl)
    n = kolvo_pr(filepath)
    url += '&page='
    for i in range(2, n):
        bot.send_message(message.chat.id, 'Я не умер')
        urlp = url + str(i)
        get_page(urlp)
        get_infa(adr, km)
    list = sorted(list)
    bot.send_message(message.chat.id, 'Квартиры найдены и отсортированы, милорд')
    for i in list:
        bot.send_message(message.chat.id, i)
