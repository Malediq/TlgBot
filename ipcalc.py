#!/usr/bin/python3

import re

def perevod2cc(ip):
    list = re.split(r'[.]', ip)
    list2cc = ''
    for i in list:
        okt = bin(int(i))
        okt = okt[2:]
        while len(okt) != 8:
            okt = '0' + okt
        list2cc += okt
    return list2cc

def mask2cc(mask):
    strmask = ''
    obrmask = ''
    for i in range(0, mask):
        strmask += '1'
        obrmask += '0'
    while len(strmask) != 32:
        strmask += '0'
        obrmask += '1'
    return [strmask, obrmask]

def perevod10cc(ip):
    str10cc = str(int(ip[0:8], 2)) + '.' + str(int(ip[8:16], 2)) + '.' + str(int(ip[16:24], 2)) + '.' + str(int(ip[24:32], 2))
    return str10cc

def ipcalc(message):
    ipmask = re.split(r'/', message.text)
    ip = ipmask[0]
    mask = int(ipmask[1])
    list = perevod2cc(ip)
    iposn = list[0:mask]
    ipnet = iposn
    ipbr = iposn
    maski = mask2cc(mask)
    netmask = perevod10cc(maski[0])
    wildmask = perevod10cc(maski[1])
    hosts = 2**(32 - mask) - 2
    while len(ipnet) != 31:
        ipnet += '0'
        ipbr += '1'
    iphmin = ipnet + '1'
    iphmax = ipbr + '0'
    ipnet += '0'
    ipbr += '1'
    ipnet = perevod10cc(ipnet)
    ipbr = perevod10cc(ipbr)
    iphmin = perevod10cc(iphmin)
    iphmax = perevod10cc(iphmax)
    text =  'Network:    ' + ipnet + '\n'
    text += 'Broadcast: ' + ipbr + '\n'
    text += 'Hostmin:    ' + iphmin + '\n'
    text += 'Hostmax:   ' + iphmax + '\n'
    text += 'Hosts:         ' + str(hosts) + '\n'
    text += 'Netmask:    ' + netmask + '\n'
    text += 'Wildcard:    ' + wildmask + '\n'
    return text
