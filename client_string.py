#!/usr/bin/env python
# -*- coding: utf-8 -*-
#头文件
import socket
import sys

def socket_client():
    try:
	#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#连接到服务器
        s.connect(('192.168.220.6', 6666))
    #socket建立失败
    except socket.error as msg:
        print msg
        sys.exit(1)
    #接受数据（前一步输入的地址），数据以字符串形式返回并打印
    print s.recv(1024)
    while 1:
	#把输入的值赋值给data
        data = raw_input('please input work: ')
	#发送数据
        s.send(data)
	#接受数据（前一步输入data），数据以字符串形式返回并打印
        print s.recv(1024)
	#如果接收到的字符是“exit”,就停止
        if data == 'exit':
            break
    #关闭套接字
    s.close()

#说明当前运行的脚本为主程序,就运行该函数 
if __name__ == '__main__':
    socket_client()
