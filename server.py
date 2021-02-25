#!/usr/bin/env python

import socket
from datetime import datetime
import subprocess
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 9999))
while True:
		s.listen(10)
		client, address = s.accept()
		print("{} connected".format( address ))
		response = client.recv(255).decode('ascii').lower()
		print(response)
		if "checker" in response:
			print("checker")
			now = datetime.now()
			dt_string = now.strftime("%d.%m.%Y-%H.%M.%S")
			with open("CheckerFrom-"+address[0]+'-'+dt_string+'.txt', 'wb') as file:
				l = client.recv(1024)
				while (l):
					file.write(l)
					l = client.recv(1024)

		elif "help" in response:
			client.send('getline'.encode('ascii'))
			response=client.recv(1024).decode('ascii')
			print(response)
			cli=input("open/close ?")
			if "open" in cli.lower():
				client.send("open".encode('ascii'))
			elif "close" in cli.lower():
				client.send("close".encode('ascii'))

client.close()
stock.close()
