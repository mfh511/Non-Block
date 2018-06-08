#!/usr/bin/env python
# -*- coding=utf-8 -*-
#头文件
import socket
import threading
import time
import sys
import os
import struct


def socket_service():
    try:
	#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个服务端
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#将套接字与指定的ip和端口相连
        s.bind(('192.168.220.6', 8888))
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
    conn.settimeout(500)
    conn.send('Hi, Welcome to the server!')

    while 1:
      try:
	#设置超时间
	conn.settimeout(500)
	#定义文件信息，文件名为128bytes长度
        fileinfo_size = struct.calcsize('128sl')
	#接受的是客户端发送过来的头部信息
        buf = conn.recv(fileinfo_size)
        if buf:
	    #解包buf得到文件名和文件大小
            filename, filesize = struct.unpack('128sl', buf)
	    #使用trip删除打包时候的多余空字符
            fn = filename.strip('\00')
	    #重新处理文件名new_filename
            new_filename = os.path.join('./', 'new_' + fn)
	    print 'start receiving...'
	    #输出新的文件名和文件大小
            print 'file new name is {0}, filesize is {1}'.format(new_filename,
                                                                 filesize)
	    #初始化接受了的文件大小0
            recvd_size = 0 
	    #读写打开文件 
            fp = open(new_filename, 'wb')
            #当没接收完时候执行
            while not recvd_size == filesize:
		#叠加大小
		#(实际文件大小大于1k,继续读取 1024 个字节（即 1 KB）的内容,新读取的字符长度加到新建文件长度中)
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
		#（实际文件多余1K小于2K的部分，继续读取filesize - recvd_size的大小）
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
		#写入
                fp.write(data)
	    #关闭文件
            fp.close()
            conn.send('end receive...');
            print 'end receive...'
      #超时报错
      except socket.timeout:
        conn.close()
    while True:
	#当有连接时，将接收到的套接字存到connection中，远程连接细节保存到address中
        connection,address=s.accept()
        print('Connected by ',address)
	#创建线程对象
        thread = threading.Thread        (target=conn_thread,args=(connection,address)) 
        thread.start()
       
#说明当前运行的脚本为主程序,就运行该函数 
if __name__ == '__main__':
    socket_service()
