from Tkinter import *
from ttk import *
import os

#############################################################################################################################################################################################################
class GUITest(Frame):
    #initialization asks for the directory to open (we want to open on the shared drive)
	def __init__ (self, parent, start):
		Frame.__init__(self, parent)
		#set the directory to the inital one just given
		self.changeDir(start)
		
	#getter and setter for curDirectory
	@property
	def curDirectory (self):
		return self._curDirectory
	@curDirectory.setter
	def curDirectory (self, location):
		self._curDirectory = location

	def setupGUI(self):
		s = Scrollbar()
		L = Listbox()
		self.Tree = Treeview()
		
		##position all of the widgets in a grid
		#Tree.grid(row = 0, column = 0)

		s.pack(side=LEFT,fill=Y)
		L.pack(side=RIGHT,fill=Y)
		#pack the tree widget to the left side with a small padding from the window border
		self.Tree.pack(side = LEFT, fill = Y, padx = 3)
		
		#make the tree have the scroll bar
		s.config(command=self.Tree.yview)
		self.Tree.config(yscrollcommand=s.set)

		for f in range(len(self._dirFiles)):
			L.insert(END,self._dirFiles[f])
		
		#fill the tree
		self.loadTree(self._curDirectory)
			
	#list all files from a directory into an array
	def changeDir (self, dir):
		#set curDir to the new directory
		self._curDirectory = dir
		#set dirFiles to a list of all the file names in the directory
		self._dirFiles = sorted(os.listdir(self._curDirectory))	
		
	#place all of the current directory into a hiearchy tree
	def loadTree (self, path, id = "start"):
		#if the id is "start" then there is no tree yet so dont feed calls the id
		
		#iset files array for the given path
		files = sorted(os.listdir(path))
		
		#counter integer
		spot = 0
		
		#loop through for the number of files in the directory
		for i in range(len(files)):
			#check to see if the item is a file or a folder
			#variable saying if it is a file (else its a folder)
			file = False
			#loop through the filename and look for a "." (means it has a file ending)
			for n in files[i]:
				if (n == "."):
					file = True
			
			#if it is a file just add it to the tree at the end of the hiearchy
			if (file == True):
				#handle case if it is the first level
				if (id == "start"):
					self.Tree.insert("", "end", text = files[i], tags = "ttk")
				else:
					self.Tree.insert(id, "end", text = files[i])
				##come through and add styling to it like picture and such
			#if it is a folder add it to the tree and use recursion to start in that folder and work inside out
			else:
				#handle case if it is the first level
				if (id == "start"):
					newID = self.Tree.insert("", "end", text = files[i])
					##add pictures and stuff
				else:
					newID = self.Tree.insert(id, "end", text = files[i])
					##add pictures and such
				#create the new path for the next iteration
				newPath = path + "/" + files[i]
				#feed the call the id of the folder to make it place it under it
				self.loadTree(newPath, newID)
			
##########################################################################################################################################################################################################
# Main #
##########################################################################################################################################################################################################
#default width and height of the window
WIDTH=800
HEIGHT=600
#create the parent frame as 'window'
window=Tk()
#set the window title
window.title("Pi Server Manager")
#actually set the size of the window instead of just having pointless constants stated
window.geometry(str(WIDTH)+"x"+str(HEIGHT))
#create an instance of GUITest and feed it a default directory
t=GUITest(window, "C:/Programming Projects/Python")
#call to set up the GUI
t.setupGUI()
#wait for the window to be closed
window.mainloop()
