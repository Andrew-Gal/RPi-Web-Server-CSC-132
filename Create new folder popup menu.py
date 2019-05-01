from Tkinter import *

class Folder(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) # calling constructor from superclass
        # creating the buttons
        self.button1 = Button(master)
        self.button1.config(text="Ok",\
                            fg="red", command = lambda: n())

        self.button1.pack(side=LEFT) 
        self.button2 = Button(master, text=\
                              "Cancel", fg="blue") # specifies location and excutes what you want to say
        self.button2.pack(side=RIGHT)
        #entry label
        e1 = Entry()
        e1.pack(side=TOP)
        self.name = ""
        # returns the name value
        def n():
            self.name = e1.get()
            print self.name

    

window = Tk()
app = Folder(window) # window mapped to 'master' in main part of program
window.mainloop()
