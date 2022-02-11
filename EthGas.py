from urllib.request import Request, urlopen

def gaschecker(request):
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
    if request == '🐌 Low':
        return '🐌 Low price: ' +str(gassafelow) + ' gwei'
    elif request == '⏳ Normal':
        return '⏳ Normal price: ' + str(gasaverage) + ' gwei'
    elif request == '🚀 Fast':
        return '🚀 Fast price: ' + str(gasfast) + ' gwei'
    elif request == '⚡ Instant':
        return '⚡ Instant price: ' + str(gasfastest) + ' gwei'
    else:
        return '💲 Precios:' + '\n' + '\n' + '🐌 Low ' + str(gassafelow) + ' gwei' + '\n' + '\n' + '⏳ Normal ' + str(
            gasaverage) + ' gwei' + '\n' + '\n' + '🚀 Fast ' + str(gasfast) + ' gwei' + '\n' + '\n' + '⚡ Instant ' + str(gasfastest) + ' gwei'