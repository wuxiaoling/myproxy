# -*- coding: utf-8 -*-
"""
@ 本地反向代理机
@ 最新功能是可以实现代理
@ author: wu
"""
#引入模块
import socket,json,signal,sys,uuid
import threading
import time

reload(sys)
sys.setdefaultencoding("utf-8")

#客户端
Index=0;
#is_exit = False	   #监听退出的条件
#localPort=80	   #本地服务器端口
#remote="47.92.131.173"#远程服务器地址
#remotePort=8099			 #远程服务器端口

def getMac():
	mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
	return ":".join([mac[e:e+2] for e in range(0,11,2)])

def send(self,request,data):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
	
	try:
		msg=client.connect_ex(('127.0.0.1', int(self.localPort)))
		if msg==0:
			pass
		else:
			return False;
	except Exception as e:
		self.Text4.insert(0.0,"本地服务器连接失败！\n")
		return False;
	
	client.send(data)
	data=client.recv(1024)
	#完整发数据到外网机器
	datas=data
	while data:
		Len=request.send(data)
		data=client.recv(1024)
		datas=datas+data
	self.Text4.insert(0.0,"响应数据 %s:%s----------------->>>>%s:%s data :\n%s"%(request.getsockname()[0],request.getsockname()[1],self.remote,self.remotePort,datas)+"\n")
	return

def handler(signum, frame):	 
	global is_exit	
	is_exit = True	
	print "receive a signal %d, is_exit = %d"%(signum, is_exit)
	sys.exit()
	
def getLink(self):

	remoteclent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remoteclent.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
	msg=remoteclent.connect_ex((str(self.remote),int(self.remotePort)))
	
	#上报mac
	sum=remoteclent.send(json.dumps({"MAC":getMac()}))

	while not self.is_exit:
		try:
			data=remoteclent.recv(2048)
			if data:
				self.Text4.insert(0.0,"get %s:%s<<<<<-----------------%s:%s data :\n%s"%(remoteclent.getsockname()[0],remoteclent.getsockname()[1],self.remote,self.remotePort,data)+"\n")
				threading.Thread(target=send,args=(self,remoteclent,data,)).start()
			else:
				time.sleep(5)
				remoteclent.send('link')#心跳包
		except Exception as e:
			return False;

def run(self):
	remoteclent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remoteclent.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
	msg=remoteclent.connect_ex((str(self.remote),int(self.remotePort)))
	if msg==0:
		self.Text4.insert(0.0,"远程连接网络畅通，可以通讯\n")
	else:
		self.Text4.insert(0.0,"远程连接出错，请重试\n")

	while not self.is_exit:
		threading.Thread(target=getLink,args=(self,)).start()
		time.sleep(1)
	return False

if __name__ == '__main__':
	#监听ctrl+c 信号
	signal.signal(signal.SIGINT, handler)
	signal.signal(signal.SIGTERM, handler)
	print getMac()
	while not is_exit:
		threading.Thread(target=getLink,args=(remote,remotePort,)).start()
		time.sleep(1)
	



