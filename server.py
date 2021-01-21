import socket
from datetime import datetime

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 9999))
while True:
        socket.listen(10)
        client, address = socket.accept()
        print("{} connected".format( address ))
        response = client.recv(255).decode('ascii')
        print(response)
        if "Checker file" in response:
	        now = datetime.now()
	        dt_string = now.strftime("%d.%m.%Y-%H.%M.%S")
	        with open("CheckerFrom-"+address[0]+'-'+dt_string+'.txt', 'wb') as file:
		        l = client.recv(1024)
		        while (l):
			        file.write(l)
			        l = client.recv(1024)
		if "Help needed" in response :
			results = []
			order = {"order": {"cmd": "ls -la", "msg": "Operating System", "results": ""}}
		    client.send(order)






client.close()
stock.close()