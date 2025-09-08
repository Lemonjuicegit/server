import requests

def plus(a,b):
    res = requests.get(fr'http://192.168.2.50:45453/test/testplus?a={a}&b={b}')
    return res.json()