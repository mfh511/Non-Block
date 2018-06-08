#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import struct
#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#连接到服务器
s.connect(('192.168.220.6', 8888))

while 1:
	#把输入的值赋值给filepth
        filepath = raw_input('please input file path: ')      
	#如果filepath是一个存在的文件
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath),
                                os.stat(filepath).st_size)
	    #发送数据,包含文件名和文件大小
            s.send(fhead)
	    #文件路径
            print 'client filepath: {0}'.format(filepath)
	    #以二进制读模式打开
            fp = open(filepath, 'rb')
            while 1:
	        # 每次读取 1024 个字节（即 1 KB）的内容
                data = fp.read(1024)
	        #无法读取时停止
                if not data:
                    break
		#将读取到的字节传送
                s.send(data)
		print '{0} file send over...'.format(filepath)
        	print s.recv(1024)
        fp.close()
	


