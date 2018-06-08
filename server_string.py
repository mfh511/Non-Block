#!/usr/bin/env python
# -*- coding: utf-8 -*-
#头文件
import socket
import threading
import time
import sys

def socket_service():
    try:
 	#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个服务端
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#将套接字与指定的ip和端口相连
        s.bind(('192.168.220.6', 6666))
	#启动监听，并将最大连接数设为10 
        s.listen(10)
    #socket创建异常
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'

    while 1:
	#当有连接时，将接收到的套接字存到conn中，远程连接细节保存到addr中
        conn, addr = s.accept()
	#利用多线程技术，为每个请求连接的 TCP 客户端创建一个新线程，实现了一台服务器同时与多台客户端进行通信的功能
        t = threading.Thread(target=deal_data, args=(conn, addr))
	#启动线程活动
        t.start()

def deal_data(conn, addr):  
    print 'Accept new connection from {0}'.format(addr)
    conn.send('Hi, Welcome to the server!')
    while 1:
	#接受套接字的数据，数据以字符串形式返回
        data = conn.recv(1024)
	#输出
        print '{0} recv: {1}'.format(addr, data)
        #time.sleep(1)
	#结束条件
        if data == 'exit' or not data:
            print '{0} connection close'.format(addr)
            conn.send('Connection closed!')
            break
	#向客户端输出hello+信息
        conn.send('Hello, {0}'.format(data))
    #关闭套接字
    conn.close()

#说明当前运行的脚本为主程序,就运行该函数 
if __name__ == '__main__':
    socket_service()
