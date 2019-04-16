from Tkinter import *
import os
path = "/home/pi/Desktop/Final Project"

class GUITest(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

    def setupGUI(self):
        s = Scrollbar()
        L = Listbox()

        s.pack(side=RIGHT,fill=Y)
        L.pack(side=RIGHT,fill=Y)

        s.config(command=L.yview)
        L.config(yscrollcommand=s.set)

        for filename in os.listdir(path):
            L.insert(END,filename)

WIDTH=800
HEIGHT=600
window=Tk()
window.title("Pi Server Manager")
t=GUITest(window)
t.setupGUI()
window.mainloop()
