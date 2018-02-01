# -*- coding: utf-8 -*-
"""
@author yalogr
"""

from socket import *
import time
import threading

HOST = 'jjfaedp.hedevice.com'
#HOST = '10.0.6.245'
PORT = 876
ADDR = (HOST,PORT)
sock = socket(AF_INET, SOCK_STREAM)

DEVICE_ID = '24613664' #light on
#DEVICE_ID = '24806294'  #temp
API_KEY = 'coSivwr8sEk0Hnt154IgMWdqVqk='

#API_KEY = 'rcrqs2KYydSzIqPZ=7v9QpmwkXM='
EXIT=0


CONN_REQ=1
CONN_RESP=2
PUSH_DATA=3
CONN_CLOSE=4
SAVE_DATA=8
SAVE_ACK=9
CMD_REQ=10
CMD_RESP=11
PING_REQ=12
PING_RESP=13
ENCRYPT_REQ=14
ENCRYPT_RESP=15


def addShortStr(str):
    lenHi = (len(str) & 0xff00 ) >> 8
    lenLow = len(str) & 0x00ff
    return chr(lenHi) + chr(lenLow)+ str

def EDP_CONN_REQ(device_id, api_key):
    ret = False
    
    reqStr = addShortStr('EDP') + chr(0x01) + chr(0x40) + chr(0x01) + chr(0x00)
    reqStr += addShortStr(device_id)
    reqStr += addShortStr(api_key)
    reqStr = chr(0x10) + chr(len(reqStr)) + reqStr 
    
    try:
        sock.send(reqStr)
        time.sleep(1)
        
        rx_byte=bytes(sock.recv(4))
        print len(rx_byte), rx_byte[0].encode("hex"), rx_byte[1].encode("hex"), rx_byte[2].encode("hex"), rx_byte[3].encode("hex")
        SUCCESS_FLAG ='\x20\x02\x00\x00'
        ret = (rx_byte == SUCCESS_FLAG)
    except BaseException, e:
        print e
    return ret

def strLenSmallEnd(data):
    tstr = ""
    l = len(data)
    c = (len(str(hex(l))) - 2 ) / 2
    i = 0
    while c > 0:
        t = (l >> (i * 8)) & 0xff
        if c > 1:
            t = t | 0x80
        tstr = tstr + chr(t)
        i = i + 1
        c = c - 1
    return tstr

def strLenBigEndInt(data):
    l = len(data)
    tstr = chr(l & 0xff000000) + chr(l & 0x00ff0000) + chr(l & 0x0000ff00) + chr(l & 0x000000ff)
    return tstr


def EDP_SAVE_DATA(devid, msgid, data, type):
    flag = 0x80
    if msgid:
        flag = 0xc0

    Rstr = chr(flag) + addShortStr(devid)
    if msgid:
        Rstr = Rstr + chr( (msgid & 0xff00) >> 8 )  + chr(msgid & 0xff)

    if type==3:
        Rstr = Rstr + chr(type) + chr( (len(data) & 0xff00) >> 8) + chr( (len(data) & 0xff))

    Rstr = Rstr + data

    l = len(Rstr)
    c = (len(str(hex(l))) - 2 ) / 2
    tstr = chr(SAVE_DATA << 4)
    i = 0
    while c > 0:
        t = (l >> (i * 8)) & 0xff
        if c > 1:
            t = t | 0x80
        tstr = tstr + chr(t)
        i = i + 1
        c = c - 1
    tstr = tstr + Rstr
    sock.send(tstr)
    print "EDP_SAVE_DATA ", hex(msgid)


def PingReq():
    print "PingReq"
    reqStr = chr(PING_REQ<<4) + chr(0x00)
    sock.send(reqStr)

def cmdResq(msgid, data):
    msgidlen = len(msgid)
    chrs = chr( (msgidlen & 0xff00) >> 8) + chr(msgidlen & 0xff) + msgid
    chrs = chrs + strLenBigEndInt(data) + data
    chrs = chr(CMD_RESP<<4) + strLenSmallEnd(chrs) + chrs
    #print chrs.encode("hex")
    print "cmdResq :", msgid
    sock.send(chrs)

def wping():
    time.sleep(1)
    PingReq()
    time.sleep(1)
    PingReq()
    time.sleep(1)

def lighton():
    msg='{"light_on":1}'
    EDP_SAVE_DATA(DEVICE_ID, 0x0202, msg, 3)

def lightoff():
    msg='{"light_on":0}'
    EDP_SAVE_DATA(DEVICE_ID, 0x0202, msg, 3)

def settem(a):
    msg='{"tem":a}'
    EDP_SAVE_DATA(DEVICE_ID, 0x0202, msg, 3)

def nexMsg():
    fb = bytes(sock.recv(1))
    if len(fb) == 0:
        return
    #print fb.encode("hex")
    code = (ord(fb) & 0xf0) >> 4
    if code == CONN_RESP:
        print "CONN_RESP"
    elif code == PUSH_DATA:
        print "PUSH_DATA"
    elif code == SAVE_DATA:
        print "SAVE_DATA"
    elif code == SAVE_ACK:
        print "SAVE_ACK"
        len1 = ord( bytes(sock.recv(1)) )
        data = sock.recv(len1)
        #flag1 = ord( bytes(sock.recv(1)) )
        #msgidh = ord( bytes(sock.recv(1)) ) << 8 
        #msgidl = ord( bytes(sock.recv(1)) )
        #msgid = msgidh + msgidl
        #print "SAVE_ACK ", len1 , flag1, hex(msgid)
        #d = ord( bytes(sock.recv(1)) )
        #print "SAVE_ACK result ", d

        flag1 = ord(data[0])
        msgidh = ord( data[1]) << 8
        msgidl = ord( data[2])
        msgid = msgidh + msgidl
        print "SAVE_ACK ", len1 , hex(flag1), hex(msgid)
        print "SAVE_ACK result ", ord(data[3])


    elif code == CMD_REQ:
        print "CMD_REQ"
        i = 0
        while(1):
            s = bytes(sock.recv(1))
            t = ord(s)
            i = i + (t & 0x7f)
            if t & 0x80:
                i = i << 8
                continue
            break
        print "length :", i
        s = bytes(sock.recv(1))
        t = ord(s)
        s1 = bytes(sock.recv(1))
        t1 = ord(s1)
        t = (t << 8) + t1
        print "cmdid length ", t
        id = sock.recv(t)
        print "cmdid len =", t, ":", id
        c = 4
        i = 0
        while(c):
            s = bytes(sock.recv(1))
            t = ord(s)
            c = c - 1
            i = i + t
            if c > 0:
                i = i << 8
        d = sock.recv(i)
        print "data len = ", i, " : ", d
        cmdResq(id, d)
        if str(d) == "open=1":
            lighton()
        else:
            lightoff()
            
    elif code == PING_RESP:
        sock.recv(1)
        print "PING_RESP"
    elif code == ENCRYPT_RESP:
        print "ENCRYPT_RESP"
    elif code == CONN_CLOSE:
        print "CONN_CLOSE"
        sock.recv(2)
        sock.close()
        EXIT = 1
    else:
        print "unknown code"

def main():
    
    
    try:
        sock.connect(ADDR)
    
        ret = EDP_CONN_REQ(DEVICE_ID, API_KEY)
        if ret:
            print '登录请求成功'
        else:
            print '登录请求失败'

        #PingReq()
        thread1 = threading.Thread(target = wping)
        thread1.start()
        #settem(10)
        lightoff()
        while EXIT == 0:
            nexMsg()
    except BaseException, e:
        print '网络连接错误', e
    finally:
        sock.close()
        
    
if __name__ == '__main__':
    main()
