import requests
import re
import json
import urllib
import Functions
T = 60
L_L = []
L = []
L_P = []
S = []
i = 0
c = 0
Buy = 61
Sell = 61

# read history
f = open('Data.txt')
# use readline() to read the first line 
line = f.readline()
while line:
    m = re.search('Z (.+?)\n', line)
    try:
        i = float(m.group(1))
        L.append(i)
        line = f.readline()
        if L.__len__() == T:
            k=[]
            for p in L:
                k.append(p - L[0])
            L_L.append(k)
            L = []
            i = 0
    except:
        line = f.readline()

f.close()

XBT, cash = Functions.calculate_Q()
Q = 2
r = requests.get('http://lauzhack.sqpub.ch/prices', stream=True)
for chunk in r.iter_content(chunk_size=1024):
    current = chunk
    # we get the price information:
    text = chunk.decode("utf-8")
    m = re.search('Z (.+?)\n', text)
    val = float(m.group(1))
    L.append(val)
    if i == Buy:
        Functions.buyBitcoin(Q)
        XBT, cash = Functions.calculate_Q()
        Q = (cash / 10) / val
    if i == Sell:
        Functions.sellBitcoin(Q)
        XBT, cash = Functions.calculate_Q()
        print(XBT)
        Q = (XBT / 10)
    i = i + 1
    if L.__len__() == T:
        k = []
        for p in L:
            k.append(p - L[0])
        L_P = L_L[Functions.choose(L, L_L)]
        L_L.append(k)
        Buy = Functions.findBuy(L_P)
        Sell = Functions.findSell(L_P)
        L = []
        i = 0


    def findBuy(L):
        """this function finds the minumum point, which tells us
        we should buy"""
        # L: list of 30 elements
        return L.index(min(L))


def findSell(L):
    """ finds the maximum point, where we should sell"""
    return L.index(max(L))


def buyBitcoin(x):
    x = str(x)
    data = 'BUY' + x + 'BTC jmf784hkuhkufsd'
    info = requests.post('http://lauzhack.sqpub.ch', data=data)
    print(info)


def sellBitcoin(x):
    x = str(x)
    data = 'SELL' + x + 'BTC jmf784hkuhkufsd'
    info = requests.post('http://lauzhack.sqpub.ch', data=data)


def streamData():
    r = requests.get("http://lauzhack.sqpub.ch/prices", stream=True)

    for chunk in r.iter_content(chunk_size=1024):
        t = 0
        for x in chunk:
            if x <= ' ':
                break
            t = t + 1
        print(chunk[t, len(chunk) - 1])


def calculate_Q():
    url = urllib.request.urlopen("http://lauzhack.sqpub.ch/teams")
    data = json.loads(url.read().decode())
    return data[4]["XBT"], data[4]["cash"]
