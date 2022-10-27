import json
import datetime
from getpass import getpass

import bcrypt
import requests
from pwinput import pwinput
from unidecode import unidecode
from Packages.Classes.usuario import Usuario
from Packages.Scripts import web_scraping
from Packages.Scripts import usuario_script
from Packages.Scripts import simulador_script

def rInput(mssg):
    try:
        entrada = int(input(mssg))
        return entrada
    except ValueError:
        return -1


result = 100 / 777
# {"keyword":"width"."decimals"f}
# keyword is not necessary
print("The result is {r:0.3f}".format(r=result))  # Default width with 3 decimals
print("The result is {:10.5f}".format(result))  # 10 width with 5 decimals




s = "hola@comóañÑ"
print(s)
print(5 in range(1, 6))

s = s.replace("ñ", "n")
s = s.replace("Ñ", "N")
print(s)
if unidecode(s) != s:
    print("* No se permiten acentos *")

usuario = object()
usuario = Usuario("daf")
print(usuario.nombreUsuario)
x = datetime.datetime.now()
print(x.day)

print(datetime.datetime.now().date())

list1 = list(range(1,6))
for i, item in enumerate(list1):
    print(i, " ", item)

    si = -1
while True:
    print("Sheesh")
    si += 1
    if(si != 2):
        continue
    print("Listo")
    break

a = type(datetime.datetime.now().date().isoformat())
print(a)

list1 = [5, 1, 7, 3, 8, 4]
list1.sort()
print(list1)
print(datetime.datetime.now()-datetime.datetime(2022, 3, 18, 12, 30, 0, 0))
d=datetime.datetime(2022, 3, 19, 18, 6, 6, 24244)
d1 = datetime.datetime(2022, 3, 19, 15, 30, 0, 0).isoformat()
print(datetime.datetime.now() > d)
print((datetime.datetime.now().date() - datetime.datetime.fromisoformat(d1).date() ))
print(datetime.datetime.now().time() > datetime.datetime(2022, 1, 1, 7, 30, 0, 0).time())
print(((datetime.datetime.now() - datetime.datetime.fromisoformat(d1)).total_seconds())/60)
print(d.date())
print("{}-{}-{}  {}:{}".format(datetime.datetime.fromisoformat(d1).day,
                               datetime.datetime.fromisoformat(d1).month,
                               datetime.datetime.fromisoformat(d1).year,
                               datetime.datetime.fromisoformat(d1).hour,
                               datetime.datetime.fromisoformat(d1).minute))

contra = pwinput(prompt='contraseña: ')
hashedPass = bcrypt.hashpw(contra.encode('utf-8'), bcrypt.gensalt(10))
print(hashedPass)
hashedPass = hashedPass.decode('utf-8')
print((hashedPass))
confirmar = pwinput(prompt='contra: ')
if bcrypt.checkpw(confirmar.encode('utf-8'), hashedPass.encode('utf-8')):
    print("si")
tipo, dimension, orden = "name", 9000, "asc"
url = "https://scanner.tradingview.com/america/scan"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}
payload = {"filter": [{"left": "{}".format(tipo), "operation": "nempty"},
                      {"left": "type", "operation": "in_range", "right": ["stock", "fund"]},
                      {"left": "subtype", "operation": "in_range",
                       "right": ["common", "foreign-issuer", "", "etf", "etf,odd", "etf,otc", "etf,cfd"]},
                      {"left": "exchange", "operation": "in_range", "right": ["AMEX", "NASDAQ", "NYSE"]}],
           "options": {"lang": "en"}, "markets": ["america"], "symbols": {"query": {"types": []}, "tickers": []},
           "columns": ["logoid", "name", "sector", "close", "change_abs", "change", "low", "high",
                       "price_52_week_low", "price_52_week_high", "volume", "average_volume_90d_calc",
                       "market_cap_basic", "premarket_open", "premarket_close", "premarket_change_abs",
                       "premarket_change", "postmarket_open", "postmarket_close", "postmarket_change_abs",
                       "postmarket_change", "description", "type", "subtype", "update_mode", "pricescale", "minmov",
                       "fractional", "minmove2", "currency", "fundamental_currency_code"],
           "sort": {"sortBy": "{}".format(tipo), "sortOrder": "{}".format(orden)}, "range": [0, dimension]}
r = requests.request("POST", url, headers=headers, json=payload).json()

acciones = []

for i in r['data']:
    acciones.append({"simbolo": i['d'][1],
                     "nombre": i['d'][21],
                     "sector": i['d'][2],
                     "unidad": i['d'][30],
                     "precioActual": i['d'][3],
                     "cambioActual": i['d'][4],
                     "cambiopActual": i['d'][5],
                     "precioMinimo": i['d'][6],
                     "precioMaximo": i['d'][7],
                     "precioMinimo52": i['d'][8],
                     "precioMaximo52": i['d'][9],
                     "volumen": i['d'][10],
                     "volumen90dias": i['d'][11],
                     "mercadoCap": i['d'][12],
                     "prePrimerPrecio": i['d'][13],
                     "preUltimoPrecio": i['d'][14],
                     "preCambio": i['d'][15],
                     "prepCambio": i['d'][16],
                     "postPrimerPrecio": i['d'][17],
                     "postUltimoPrecio": i['d'][18],
                     "postCambio": i['d'][19],
                     "postpCambio": i['d'][20]})
print(len(acciones))

info = rInput("ingresa tu np: ")
print(info)
'''
usuarios = [Usuario("Zen Eddie", "José Eddie Aguilar Ceballos", 21, "Masculino", "ed@a", "3DDi31716"),
            Usuario("Zen ", "Eddie Aguilar Ceballos", 31, "Femenino", "ed@aaguilar", "3DD1716"),
            Usuario("Eddie", "José Ceballos", 80, "Otro", "eddie@a", "3DD")]
with open('Packages\\Files\\usuarios.json', 'w') as f:
    json.dump(usuarios, f, indent=2, default=lambda x: x.__dict__)
try:
    with open('Packages\\Files\\usuarios.json') as f:
        users = json.load(f)
    usuarios1 = []
    for item in users:
        usuarios1.append(Usuario(**item))
    print(usuarios1[0].nombreCompleto)
except IOError:
    pass
'''
# user = json.loads(usuariosjs, object_hook=lambda d: list(Usuario(**item) for item in d))

print(datetime.datetime.now().day)