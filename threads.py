import requests
import threading
import mysql.connector
import json
import pandas as pd
import threading
import time
from decimal import Decimal
from datetime import datetime

import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user="root", database = "mydb",password='mysql')
mycursor = mydb.cursor()

def up_wl(username):
    mycursor.execute("SELECT * FROM WATCHLIST")
    w_data = mycursor.fetchall()
    for i in range(len(w_data)):
        curname = w_data[i][2]
        data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname.lower()}')
        data = data.json()
        a = data['data']
        mycursor.execute(f"UPDATE WATCHLIST SET PRICE = {Decimal(a['priceUsd'])}, SUPPLY = {Decimal(a['supply'])}, MARKETCAP = {Decimal(a['marketCapUsd'])}, VOLUME = {Decimal(a['volumeUsd24Hr'])} WHERE CURNAME = '{curname}' ")
        mydb.commit() 
def up_hd(username):        
    mycursor.execute("SELECT * FROM HOLDING")
    h_data = mycursor.fetchall()
    for i in range(len(h_data)):
        curname = h_data[i][2]
        inv = h_data[i][5]
        q = h_data[i][4]
        data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname.lower()}')
        data = data.json()
        a = data['data']
        returns = inv - Decimal(a['priceUsd'])*q
        mycursor.execute(f"UPDATE HOLDING SET CUR_PRICE = {Decimal(a['priceUsd'])}, RETURNS ={returns} WHERE CURNAME = '{curname}' ")
        mydb.commit() 
        print('done')
def thr():
    t1 = threading.Thread(target=up_wl('thejabh'))
    t2 = threading.Thread(target=up_hd('thejabh'))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

while True:
    thr()
    time.sleep(30)

# def buying(username,curname,quantity):
#     amt = Decimal(quantity)
#     data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}')
#     data = data.json()
#     a = data['data']
#     tp = Decimal(a['priceUsd'])*amt
#     time = data['timestamp']//1000
#     time_cur = pd.to_datetime(time,unit='s')
    
    
#     mycursor.execute(f"SELECT PER_COIN FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'")
#     d = mycursor.fetchall()
#     if d == []:
#         sql1 = f"INSERT INTO BOUGHT VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{tp},'{time_cur}')"
#         sql2 = f"INSERT INTO HOLDING VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{tp},NULL,{Decimal(a['priceUsd'])})"
#         mycursor.execute(sql1)
#         mycursor.execute(sql2)
#         print('list was empty')
#     else:
#         mycursor.execute(f"SELECT QUANTITY FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'")
#         q = mycursor.fetchall()
#         old_q = q[0][0]
#         old_pc = d[0][0]
#         new_pc = ((old_pc*old_q)+(tp))/(old_q+amt)
#         sql1 = f"INSERT INTO BOUGHT VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{tp},'{time_cur}')"
#         sql2 = f"UPDATE HOLDING SET QUANTITY = {old_q+amt} ,INVESTED = {tp+(old_pc*old_q)} ,PER_COIN = {new_pc} WHERE CURNAME = '{curname}'"
#         mycursor.execute(sql1)
#         mycursor.execute(sql2)
#         print('updated avg')
#     mydb.commit()
# buying('thejabh','ethereum',10)