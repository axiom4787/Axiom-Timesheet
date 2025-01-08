from window import createWindow

#Thread the window
import threading

t = threading.Thread(target=createWindow)
t.start()