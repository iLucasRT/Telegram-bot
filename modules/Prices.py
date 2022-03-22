from pycoingecko import CoinGeckoAPI
import csv

cg = CoinGeckoAPI()

def ethereumprice(crypto, token_name):
    try:
        rawprice = cg.get_price(ids=crypto, vs_currencies='usd')
        rawprice = str(rawprice[crypto])
        rawprice = rawprice[7::]
        rawprice = rawprice.replace('}', ' ',)
        rawprice = float(rawprice)
        price = "El precio de " + token_name + " es de " + str(rawprice) + " USD"
        return price
    except KeyError:
        return 'Error de moneda'