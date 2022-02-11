from urllib.request import Request, urlopen
from telegram import Update, ForceReply
from telegram.ext import Updater
from twisted.internet import task, reactor


def gaschecker():
    url = 'https://ethgasstation.info/api/ethgasAPI.json?api-key=90c88f7a523e00a269d7cb7be1641b8de1992b44cfd26bbd92f67dd390f6'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    webpage = webpage[1:65]
    webpage = webpage.split(sep=":")
    webpage = "".join(webpage)
    webpage = webpage.split(sep=',')
    webpage = "".join(webpage)
    webpage = webpage.split(sep='"')
    gasfast = (float(webpage[2]) // 10)
    gasfastest= (float(webpage[4]) // 10)
    gasaverage = (float(webpage[6]) // 10)
    gassafelow = (float(webpage[8]) // 10)
    return float(gassafelow)

def alerta(update: Update, patron):
    print('entré en alerta bro')
    gasnow = gaschecker()
    if gasnow < float(patron):
        update.message.reply_text('Alerta! El precio del gas es de ' + str(gasnow))
    else:
        return None

def caller(update: Update, num):
    tiempo = 1.5
    l = task.LoopingCall(alerta)
    l.start(tiempo)
    alerta(update, num)
    print('estoy acá')
    if update.message.text == '🔕 Desactivar alerta':
        print('entré al if pa')
