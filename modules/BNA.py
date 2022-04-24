import json
from urllib.request import Request, urlopen
import requests


def dolar_blue():
    url = 'https://api.estadisticasbcra.com/usd'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzkxMDE4MDAsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.Znwt0xyLHGP8IgRkB-widW1XqzJjLBxmgdw0U4tb0p6Arhn5VArO29gJQezuvWjU2PE07QSY0l9F0cUlBa1r5w'}
    request = requests.get(url, headers=header)
    dolaroficial = request.json()
    largo = (len(dolaroficial)-1)
    dolaroficial = dolaroficial[largo]
    dolaroficial = str(dolaroficial['v'])
    if '.' in dolaroficial:
        dolaroficial = dolaroficial.replace('.', ',')
    return 'El valor del dólar blue es de $' + dolaroficial

def dolar_oficial(impuesto):
    url = 'https://api.estadisticasbcra.com/usd_of'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzkxMDE4MDAsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.Znwt0xyLHGP8IgRkB-widW1XqzJjLBxmgdw0U4tb0p6Arhn5VArO29gJQezuvWjU2PE07QSY0l9F0cUlBa1r5w'}
    request = requests.get(url, headers=header)
    dolaroficial = request.json()
    largo = (len(dolaroficial)-1)
    dolaroficial = dolaroficial[largo]
    dolaroficial = str(dolaroficial['v'])
    if impuesto == '💵 Dólar oficial con impuestos':
        dolaroficial = (float(dolaroficial)*1.65)
        dolaroficial = str(dolaroficial)
        return 'El valor del dólar solidario es de $' + dolaroficial[:6]
    if '.' in dolaroficial:
        dolaroficial = dolaroficial.replace('.', ',')
    return 'El valor del dólar oficial es de $' + dolaroficial[:6]

def cotizaciones():
    a = dolar_blue()
    b = dolar_oficial('')
    c = dolar_oficial('💵 Cotización dólar oficial con impuestos')
    return a + "\n" + b + "\n" + c


def circulacion_monetaria():
    url = 'https://api.estadisticasbcra.com/circulacion_monetaria'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzkxMDE4MDAsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.Znwt0xyLHGP8IgRkB-widW1XqzJjLBxmgdw0U4tb0p6Arhn5VArO29gJQezuvWjU2PE07QSY0l9F0cUlBa1r5w'}
    request = requests.get(url, headers=header)
    circulacion = request.json()
    largo = (len(circulacion)-1)
    circulacion = circulacion[largo]
    circulacion = str(circulacion['v'])
    circulacion = float(circulacion)
    return f'La circulación monetaria actual es de ${circulacion:,.2f} millones'

def inflacion():
    url = 'https://api.estadisticasbcra.com/inflacion_interanual_oficial'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzkxMDE4MDAsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.Znwt0xyLHGP8IgRkB-widW1XqzJjLBxmgdw0U4tb0p6Arhn5VArO29gJQezuvWjU2PE07QSY0l9F0cUlBa1r5w'}
    request = requests.get(url, headers=header)
    inflacion = request.json()
    largo = (len(inflacion)-1)
    inflacion = inflacion[largo]
    inflacion = str(inflacion['v'])
    return 'La inflación interanual es de ' + inflacion + '%'
