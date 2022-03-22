from urllib.request import Request, urlopen
from telegram import Update


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
    try:
        print('entré en alerta bro')
        gasnow = gaschecker()
        if float(gasnow) < float(patron):
            print('en el if')
            update.message.reply_text('Alerta! El precio del gas es de ' + str(gasnow))
        else:
            return None
    except ValueError:
        print('al except')
        pass

def caller(update: Update, num):
    alerta(update, num)
    #rt = RepeatedTimer(5, alerta, update, num)

