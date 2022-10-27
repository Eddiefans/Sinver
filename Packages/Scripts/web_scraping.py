import requests

def scrap(tipo, dimension, orden):

    # payload = {"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","foreign-issuer","","etf","etf,odd","etf,otc","etf,cfd"]},{"left":"exchange","operation":"in_range","right":["AMEX","NASDAQ","NYSE"]},{"left":"is_primary","operation":"equal","right":True}],"options":{"lang":"en"},"markets":["america"],"symbols":{"query":{"types":[]},"tickers":[]},"columns":["logoid","name","sector","close","change_abs","change","low","high","price_52_week_low","price_52_week_high","volume","average_volume_90d_calc","market_cap_basic","premarket_open","premarket_close","premarket_change_abs","premarket_change","postmarket_open","postmarket_close","postmarket_change_abs","postmarket_change","description","type","subtype","update_mode","pricescale","minmov","fractional","minmove2","currency","fundamental_currency_code"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,6000]}
    url = "https://scanner.tradingview.com/america/scan"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}
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
        for i1, item in acciones[-1].items():
            if str(type(item)) == "<class 'NoneType'>":
                if i1 == "simbolo" or i1 == "nombre" or i1 == "sector" or i1 == "unidad":
                    acciones[-1][i1] = ""
                else:
                    acciones[-1][i1] = 0
    return acciones


def scrap_todas_acciones():
    return scrap("name", 9000, "asc")


def scrap_acciones_activas():
    return scrap("volume", 15, "desc")


def scrap_acciones_cap():
    return scrap("market_cap_basic", 15, "desc")