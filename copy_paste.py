import pyperclip
import time
from pynput import keyboard
import os

def copy_paste():
    list = []
    while True:    
        if pyperclip.paste() != 'None':
            value = pyperclip.paste()
            print( pyperclip.paste())
            if value not in list:            
                list.append(value)
            print (list) 
            time.sleep(4)
            f = open('paste.txt','w')
            for ele in list:
              f.write(ele+'\n')
            f.close()

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
    print("Key {} pressed".format(key_name))
    print("Key type: {}".format(key.__class__.__name__))



if __name__ == "__main__":
#    liste = ['pip list | grep -F pyperclip','pip list | grep -F pynput']
#    for elem in liste:
#        result = os.system(elem)
#        print (result)
#        if result != 0:
#          lastelem = elem.split(" ").pop();
#          os.system('pip install '+lastelem)
#    list = []
#    with keyboard.Listener(on_press = on_press) as listener:
#      listener.join()
      copy_paste()
