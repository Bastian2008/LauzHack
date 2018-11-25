import json
import requests
import urllib
import re

T = 50


def findBuy(L):
    """this function finds the minumum point, which tells us
    we should buy"""
    # L: list of 30 elements
    return L.index(min(L))


def findSell(L):
    """ finds the maximum point, where we should sell"""
    return L.index(max(L))


def buyBitcoin(x):
    x = float(x)
    x = str(x)
    data = 'BUY ' + x + ' BTC jmf784hkuhkufsd'
    info = requests.post('http://lauzhack.sqpub.ch', data=data)
    print(data)



def sellBitcoin(x):
    x = float(x)
    x = str(x)
    data = 'SELL ' + x + ' BTC jmf784hkuhkufsd'
    info = requests.post('http://lauzhack.sqpub.ch', data=data)
    print(data)


def streamData():
    r = requests.get("http://lauzhack.sqpub.ch/prices", stream=True)

    for chunk in r.iter_content(chunk_size=1024):
        t = 0
        chunk = str(chunk)
        for x in chunk:
            if x <= ' ':
                break
            t = t + 1
        i = t + 1
        for i in range(len(chunk)):
            if chunk[i] > '9' or chunk[i] < '0' or chunk[i] != '.':
                break
            i = i + 1
        val = float(chunk[t + 1:i])
        print(val)


def popLowest(L_L,A):
    i = A.index(min(A))
    print(i)
    L_L.pop(2*i)
    L_L.pop(2*i)
    A.pop(i)
    A.append(0)

def choose(L, L_L):
    var = float("inf")
    closest = 0
    i=0
    for i in range(int(len(L_L)/2)):
        s = 0
        for k in range(T):
            s += abs(L[k] - L_L[2*i][k])
        if (s < var):
            closest = i
            var = s
    return 2*i + 1


def calculate_Q():
    url = urllib.request.urlopen("http://lauzhack.sqpub.ch/teams")
    data = json.loads(url.read().decode())
    return data[4]["XBT"], data[4]["cash"]


