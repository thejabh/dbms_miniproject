import mysql.connector
import requests
import json
import pandas as pd
import threading
import time
import hashlib
from decimal import Decimal
mydb = mysql.connector.connect(host = "localhost", user="root", database = "mydb",password='mysql')
mycursor = mydb.cursor()

#FOR SIGNUP
def selectfromusers(username):
    sql = "SELECT * FROM USER_INFO WHERE USERNAME = %s "
    val = (username,)
    mycursor.execute(sql,val)
    userdata = mycursor.fetchall()
    for i in userdata:
        return i
#FOR SIGNUP    
def insertintousers(fullname,username,phno,passwd):
    sql = "INSERT INTO USER_INFO VALUES(%s,%s,%s,SHA2(%s,256))"
    val = (fullname,username,phno,passwd,)
    mycursor.execute(sql,val)
    mydb.commit()
#FOR LOGIN    
def logindatabase(username,passwd):
    sql = "SELECT * FROM USER_INFO WHERE USERNAME = %s"
    val = (username,)
    mycursor.execute(sql,val)
    logindata = mycursor.fetchall()
    for i in logindata:
        if passwd==i[3] : #hashlib.sha256(passwd.encode()).hexdigest() == i[3]:
            return True
#FOR HISTORICAL DATA    
def get_his(curname,interval):#interval = 1d,1week,1month,1year 
    #if want more data points use start and end in .get()
    price = []
    time = []
    if interval == '1d':
        data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}'+"/history?interval=m1")
        data = data.json()
        for i in data['data']:
            price = price + [Decimal(i['priceUsd'])]
            time_ = (i['time']//1000)
            time__ = pd.to_datetime(time_,unit='s')
            time = time + [time__]
    elif interval == '1w':
        data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}'+"/history?interval=m15")
        data = data.json()
        for i in data['data']:
            price = price + [Decimal(i['priceUsd'])]
            time_ = (i['time']//1000)
            time__ = pd.to_datetime(time_,unit='s')
            time = time + [time__]
    elif interval == '1m':
        data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}'+"/history?interval=h1")
        data = data.json()
        for i in data['data']:
            price = price + [Decimal(i['priceUsd'])]
            time_ = (i['time']//1000)
            time__ = pd.to_datetime(time_,unit='s')
            time = time + [time__]
    elif interval == '1y':
        data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}'+"/history?interval=h12")
        data = data.json()
        for i in data['data']:
            price = price + [Decimal(i['priceUsd'])]
            time_ = (i['time']//1000)
            time__ = pd.to_datetime(time_,unit='s')
            time = time + [time__]
    df = pd.DataFrame(list(zip(price,time)),columns = ['price','time'])
    return df
def current_data(curname):
    data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}')
    data = data.json()

    new_data=data['data']
    price = Decimal(new_data['priceUsd'])
    time_ = data['timestamp']//1000
    time__ = pd.to_datetime(time_,unit='s')
    #cur_data = pd.DataFrame(list(zip(list(price),list(time__)),column=['price','time']))
    return pd.DataFrame([{'price':price,'time':time__}])
#adding cur to watchlist
def addtowatchlist(username,curname):
    data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}')
    data = data.json()
    a = data['data']
    sql = f"INSERT INTO WATCHLIST VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{Decimal(a['supply'])},{Decimal(a['marketCapUsd'])},{Decimal(a['volumeUsd24Hr'])})"
    mycursor.execute(sql)
    mydb.commit()
#deleting from watchlist
def delfromwatchlist(username,curname):
    sql = "DELETE FROM WATCHLIST WHERE USERNAME = %s AND CURNAME = %s"
    val = (username,curname)
    mycursor.execute(sql, val)
    mydb.commit()

 #buying curr
def buying(username,curname,quantity):
    amt = Decimal(quantity)
    data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}')
    data = data.json()
    a = data['data']
    tp = Decimal(a['priceUsd'])*amt
    time = data['timestamp']//1000
    time_cur = pd.to_datetime(time,unit='s')
    
    
    mycursor.execute(f"SELECT PER_COIN FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'")
    d = mycursor.fetchall()
    if d == []:
        sql1 = f"INSERT INTO BOUGHT VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{tp},'{time_cur}')"
        sql2 = f"INSERT INTO HOLDING VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{tp},{Decimal(a['priceUsd'])},NULL)"
        mycursor.execute(sql1)
        mycursor.execute(sql2)
    else:
        mycursor.execute(f"SELECT QUANTITY FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'")
        q = mycursor.fetchall()
        old_q = q[0][0]
        old_pc = d[0][0]
        new_pc = ((old_pc*old_q)+(tp))/(old_q+amt)
        sql1 = f"INSERT INTO BOUGHT VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{tp},'{time_cur}')"
        sql2 = f"UPDATE HOLDING SET QUANTITY = {old_q+amt} ,INVESTED = {tp+(old_pc*old_q)} ,PER_COIN = {new_pc} WHERE CURNAME = '{curname}'"
        mycursor.execute(sql1)
        mycursor.execute(sql2)
    
    mydb.commit()
#selling cur
def selling(username,curname,quantity):
    if quantity == 0:
        print("invalid")
        return
    amt = Decimal(quantity)
    data = requests.get("http://api.coincap.io/v2/assets/"+f'{curname}')
    data = data.json()
    a = data['data']
    time = data['timestamp']//1000
    time_cur = pd.to_datetime(time,unit='s')
    
    mycursor.execute(f"SELECT QUANTITY FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'")
    d = mycursor.fetchall()
    if d == []:
        pass
        #cur doesn't exist (*depends upon where we want to show sell button*!!!!!!!!!!)
    else:
        old_q = d[0][0]
        if old_q < amt:
            print("invalid")
        else:
            mycursor.execute(f"SELECT PER_COIN FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'")
            pc = mycursor.fetchall()
            pc_ = pc[0][0]
            total_r = (pc_ - Decimal(a['priceUsd']))*amt
            new_q = old_q - amt
            if new_q == 0:
                sql1 = f"DELETE FROM HOLDING WHERE USERNAME = '{username}' AND CURNAME = '{curname}'"
                sql2 = f"INSERT INTO SELL_OUT VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{total_r},'{time_cur}')"
                mycursor.execute(sql1)
                mycursor.execute(sql2)

            else:
                inv = pc_ * new_q
                sql1 = f"UPDATE HOLDING SET QUANTITY = {new_q}, INVESTED = {inv}"
                sql2 = f"INSERT INTO SELL_OUT VALUES('{username}','{a['symbol']}','{a['name']}',{Decimal(a['priceUsd'])},{amt},{total_r},'{time_cur}')"
                mycursor.execute(sql1)
                mycursor.execute(sql2)
    mydb.commit()
