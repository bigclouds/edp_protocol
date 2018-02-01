# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 09:02:38 2016

@author: io0ot
"""

from socket import *
import time

HOST = 'jjfaedp.hedevice.com'
PORT = 876
ADDR = (HOST,PORT)
sock = socket(AF_INET, SOCK_STREAM)


def EDP_CONN_REQ(device_id, api_key):
    
    def addShortStr(str):
        lenHi = (len(str) & 0xff00 ) >> 8
        lenLow = len(str) & 0x00ff
        
        return chr(lenHi) + chr(lenLow)+ str
        
    
    ret = False
    
    reqStr = addShortStr('EDP') + chr(0x01) + chr(0x40) + chr(0x01) + chr(0x00)
    reqStr += addShortStr(device_id)
    reqStr += addShortStr(api_key)
    reqStr = chr(0x10) + chr(len(reqStr)) + reqStr 
    
    try:
        sock.send(reqStr)
        time.sleep(1)
        
        rx_byte=bytes(sock.recv(4))
        print rx_byte[0].encode("hex"), rx_byte[1].encode("hex"), rx_byte[2].encode("hex"), rx_byte[3].encode("hex")
        SUCCESS_FLAG ='\x20\x02\x00\x00'
        ret = (rx_byte == SUCCESS_FLAG)
    except BaseException, e:
        print e
        
    finally:
        sock.close()
        
    return ret


def main():
    
    DEVICE_ID = '24582590'  #请使用你自己的device id和api key来替代下面的内容
    API_KEY = 'rcrqs2KYydSzIqPZ=7v9QpmwkXM='
    
    try:
        sock.connect(ADDR)
    
        ret = EDP_CONN_REQ(DEVICE_ID, API_KEY)
        if ret:
            print '登录请求成功'
        else:
            print '登录请求失败'

        while 0:
            data = sock.recv(4)
            code = data[0] & 0xf0
            if code == 10:
                print "recv cmd req"
    except:
        print '网络连接错误'
        
    
if __name__ == '__main__':
    main()
