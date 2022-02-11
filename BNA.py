import json
from urllib.request import Request, urlopen
import requests

def dolar_blue():
    url = 'https://api.estadisticasbcra.com/usd'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU5NTI1ODcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.j3lut0Aj1a8DqpsRVFpCi_W1NnzMJfwfIMiBfMx_h7SDrgFFYezYIHrdmI867vH0gFk77FMml9yiz-U5d41LhA'}
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
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU5NTI1ODcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.j3lut0Aj1a8DqpsRVFpCi_W1NnzMJfwfIMiBfMx_h7SDrgFFYezYIHrdmI867vH0gFk77FMml9yiz-U5d41LhA'}
    request = requests.get(url, headers=header)
    dolaroficial = request.json()
    largo = (len(dolaroficial)-1)
    dolaroficial = dolaroficial[largo]
    dolaroficial = str(dolaroficial['v'])
    if impuesto == '💵 Dólar oficial con impuestos':
        dolaroficial = (float(dolaroficial)*1.65)
        dolaroficial = str(dolaroficial)
    if '.' in dolaroficial:
        dolaroficial = dolaroficial.replace('.', ',')
    return 'El valor del dólar oficial es de $' + dolaroficial[:6]

def cotizaciones():
    a = dolar_blue()
    b = dolar_oficial('')
    c = dolar_oficial('💵 Cotización dólar oficial con impuestos')
    return a, b, c


def circulacion_monetaria():
    url = 'https://api.estadisticasbcra.com/circulacion_monetaria'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU5NTI1ODcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.j3lut0Aj1a8DqpsRVFpCi_W1NnzMJfwfIMiBfMx_h7SDrgFFYezYIHrdmI867vH0gFk77FMml9yiz-U5d41LhA'}
    request = requests.get(url, headers=header)
    circulacion = request.json()
    largo = (len(circulacion)-1)
    circulacion = circulacion[largo]
    circulacion = str(circulacion['v'])
    circulacion = float(circulacion)
    return f'La circulación monetaria actual es de ${circulacion:,.2f} millones'

def inflacion():
    url = 'https://api.estadisticasbcra.com/inflacion_interanual_oficial'
    header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU5NTI1ODcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ0dW1pbGFzY2lsQGdtYWlsLmNvbSJ9.j3lut0Aj1a8DqpsRVFpCi_W1NnzMJfwfIMiBfMx_h7SDrgFFYezYIHrdmI867vH0gFk77FMml9yiz-U5d41LhA'}
    request = requests.get(url, headers=header)
    inflacion = request.json()
    largo = (len(inflacion)-1)
    inflacion = inflacion[largo]
    inflacion = str(inflacion['v'])
    return 'La inflación interanual es de ' + inflacion + '%'