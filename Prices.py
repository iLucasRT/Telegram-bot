from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def ethereumprice(crypto):
    try:
        if crypto == 'pvu':
            crypto = 'plant-vs-undead-token'
        elif crypto == 'cake':
            crypto = 'pancakeswap-token'
        #crypto = str(crypto[7::])
        rawprice = cg.get_price(ids=crypto, vs_currencies='usd')
        rawprice = str(rawprice[crypto])
        rawprice = rawprice [7::]
        rawprice = rawprice.replace('}', ' ',)
        rawprice = float(rawprice)
        price = "El precio del " + crypto.capitalize() + " es de " + str(rawprice) + " USD"
        return price
    except KeyError:
        return 'Error de moneda'