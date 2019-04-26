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
		
		#set the tree to call to open a file when double clicked
		self.Tree.bind("<Double-1>", self.dubClick)
		
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

		# set the button to call to open the command options when right clicked
		self.Tree.bind("<Button-3>", self.functions_config)
			
	#list all files from a directory into an array
	def changeDir (self, dir):
		#set curDir to the new directory
		self._curDirectory = dir
		#set dirFiles to a list of all the file names in the directory
		self._dirFiles = sorted(os.listdir(self._curDirectory))
		#empty the directory count array
		self.dirCon = []
		
	#function to open a file from its default program
	def openFile (self, file):
		try:
			os.startfile(file)
		except:
			#notify if the file wasn't able to be opened
			print "file not found"
			
	#function to handle when an object is double clicked
	def dubClick (self, event):
		#determine which region was clicked (so we know which file)
		item = self.Tree.focus()
		#get the file location from the selected item
		folder = self.Tree.item(item)["tags"]
		folder = int(folder[0])
		
		#get the file's names
		name = self.Tree.item(item)["text"]
		#create the file's address
		file = self.dirCon[folder] + "/" + name
		
		#call to open the file
		self.openFile(file)
		
	#place all of the current directory into a hiearchy tree
	def loadTree (self, path, id = "start", spot = 0):
		#if the id is "start" then there is no tree yet so dont feed calls the id
		#if no spot is provided then it is first start, so now spot counts to keep an item tag equal to an index to link to its directory path
		
		#add the current directory path to the array so it can be found later
		self.dirCon.append(path)
		
		#iset files array for the given path
		files = sorted(os.listdir(path))
		
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
					self.Tree.insert("", "end", text = files[i], tags = str(spot))
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
				self.loadTree(newPath, newID, spot + 1)

	def functions_config(self, event):
		# displays popup menu
		self.menu = Menu()
		# initializes the label commands options after you right click
		self.menu.add_command(label="Open File", command=self.openFile)
		# self.menu.add_command(label="Cut", command=storeobj['Cut'])
		# self.menu.add_command(label="Paste", command=storeobj['Paste'])
		# self.menu.add_separator()
		# self.menu.add_command(label="Select All", command=storeobj['SelectAll'])
		# self.menu.add_separator()
		# displays the pop up menu
		self.menu.tk_popup(event.x, event.y)
		return

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
t=GUITest(window, "C:\Users\Kalia Patterson/Downloads/RoomAdventure")
#call to set up the GUI
t.setupGUI()
#wait for the window to be closed
window.mainloop()
