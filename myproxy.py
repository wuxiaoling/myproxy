#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from ReverseProxy import * 
try:
	from tkinter import *
	from tkinter.scrolledtext import ScrolledText
except ImportError:	 #Python 2.x
	PythonVersion = 2
	from Tkinter import *
	from tkFont import Font
	from ttk import *
	from tkMessageBox import *
	from tkinter.scrolledtext import ScrolledText
else:  #Python 3.x
	PythonVersion = 3
	from tkinter.font import Font
	from tkinter.ttk import *
	from tkinter.messagebox import *



class Application_ui(Frame):
	#这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master.title('proxy')
		self.master.geometry('792x770')
		self.master.protocol("WM_DELETE_WINDOW",self.ask_quit)
		self.createWidgets()
		self.is_exit = False
		self.localPort=0
		self.remote=""
		self.remotePort=0
		self.threadPools=[]
		
	def ask_quit(self):
		if askyesno("提示","确定程序退出？"):
			sys.exit()

	def createWidgets(self):
		self.top = self.winfo_toplevel()

		self.style = Style()
		
		self.Text4Font = Font(font=('宋体',9))
		self.Text4 = ScrolledText(self.top, fg='#000000', bg='#FFFFFF', bd=1, relief=SUNKEN, state='normal', wrap=CHAR, font=self.Text4Font)
		self.Text4.place(relx=0.192, rely=0., relwidth=0.6810, relheight=0.975,height=20, width=100)

		self.Text3Var = StringVar(value='47.92.131.173')
		self.Text3 = Entry(self.top, text='47.92.131.173', textvariable=self.Text3Var, font=('宋体',9))
		self.Text3.place(relx=0., rely=0.218, relwidth=0.183, relheight=0.043)

		self.style.configure('Command2.TButton',font=('宋体',9))
		self.Command2 = Button(self.top, text='reload', command=self.Command2_Cmd, style='Command2.TButton')
		self.Command2.place(relx=0.101, rely=0.281, relwidth=0.082, relheight=0.043)

		self.style.configure('Command1.TButton',font=('宋体',9))
		self.Command1 = Button(self.top, text='start', command=self.Command1_Cmd, style='Command1.TButton')
		self.Command1.place(relx=0., rely=0.281, relwidth=0.082, relheight=0.043)

		self.Text2Var = StringVar(value='8099')
		self.Text2 = Entry(self.top, text='8099', textvariable=self.Text2Var, font=('宋体',9))
		self.Text2.place(relx=0., rely=0.125, relwidth=0.183, relheight=0.043)

		self.Text1Var = StringVar(value='80')
		self.Text1 = Entry(self.top, text='80', textvariable=self.Text1Var, font=('宋体',9))
		self.Text1.place(relx=0., rely=0.042, relwidth=0.183, relheight=0.043)

		self.style.configure('Label3.TLabel',anchor='w', font=('宋体',9))
		self.Label3 = Label(self.top, text='远程ip地址', style='Label3.TLabel')
		self.Label3.place(relx=0., rely=0.187, relwidth=0.183, relheight=0.032)

		self.style.configure('Label2.TLabel',anchor='w', font=('宋体',9))
		self.Label2 = Label(self.top, text='远程端口', style='Label2.TLabel')
		self.Label2.place(relx=0., rely=0.094, relwidth=0.183, relheight=0.032)

		self.style.configure('Label1.TLabel',anchor='w', font=('宋体',9))
		self.Label1 = Label(self.top, text='本地端口', style='Label1.TLabel')
		self.Label1.place(relx=0., rely=0.01, relwidth=0.183, relheight=0.043)
		
		self.style.configure('Command3.TButton',font=('宋体',9))
		self.Command3 = Button(self.top, text='clear', command=self.Command3_Cmd, style='Command3.TButton')
		self.Command3.place(relx=0., rely=0.333, relwidth=0.08, relheight=0.043)


class Application(Application_ui):
	#这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
	def __init__(self, master=None):
		Application_ui.__init__(self, master)

	def Command2_Cmd(self, event=None):

		self.is_exit=True
		time.sleep(1)
		self.localPort=self.Text1.get()
		self.remote=self.Text3.get()
		self.remotePort=self.Text2.get()
		self.is_exit=False
		
		self.Text4.insert(INSERT, "程序重启中：\n")
		self.Text4.insert(INSERT,getMac()+"\n")
		self.Text4.insert(INSERT,"正在连接：%s:%s"%(self.remote,self.remotePort)+"\n")
		new=threading.Thread(target=run,args=(self,))
		new.setDaemon(True)
		self.threadPools.append(new)
		new.start()
		self.Text4.insert(INSERT, "程序运行成功!!\n")

	def Command1_Cmd(self, event=None):

		self.is_exit=True
		time.sleep(1)
		self.localPort=self.Text1.get()
		self.remote=self.Text3.get()
		self.remotePort=self.Text2.get()
		self.is_exit=False
		
		self.Text4.insert(0.0, "程序启动中：\n")
		self.Text4.insert(0.0,getMac()+"\n")
		self.Text4.insert(0.0,"正在连接：%s:%s"%(self.remote,self.remotePort)+"\n")
		new=threading.Thread(target=run,args=(self,))
		new.setDaemon(True)
		self.threadPools.append(new)
		new.start()
		self.Text4.insert(INSERT, "程序运行成功!!\n")
		
	def Command3_Cmd(self, event=None):
		self.Text4.delete(0.0,END)


if __name__ == "__main__":

	top = Tk(className='一个简单的内网穿透工具')
	top.iconbitmap('./py.ico')
	Application(top).mainloop()

	try: top.destroy()
	except:sys.exit()