from Tkinter import *
from ttk import *
import os
from random import randint

#############################################################################################################################################################################################################
# noinspection PyUnreachableCode
class GUITest(Frame):
    #initialization asks for the directory to open (we want to open on the shared drive)
	def __init__ (self, parent, start):
		Frame.__init__(self, parent)
		#set the directory to the inital one just given
		self.changeDir(start)
		self.grid(sticky=N+E+W+S)

	#getter and setter for curDirectory
	@property
	def curDirectory (self):
		return self._curDirectory
	@curDirectory.setter
	def curDirectory (self, location):
		self._curDirectory = location

	def setupGUI(self):
		s = Scrollbar()
		self.Tree = Treeview()

		#set the tree to call to open a file when double clicked
		self.Tree.bind("<Double-1>", self.dubClick)
		# set the button to call to open the command options when right clicked
		self.Tree.bind("<Button-3>", self.functions_config)

		##position all of the widgets in a grid
		self.Tree.grid(row = 0, column = 0, sticky = N+E+W)
		#position the scroll bar
		s.grid(row = 0, column = 1)
		#position the loadbar

		#make the tree have the scroll bar
		s.config(command=self.Tree.yview)
		self.Tree.config(yscrollcommand=s.set)

		#fill the tree
		self.loadTree(self._curDirectory)

		# load the storage bar
		self.loadBar()

		# load the refresh button
		self.loadRefresh()

		#setup progress bar
		self.pbar_det.grid(row = 2, column = 0, sticky = E+W+S)
		self.lab_det_used.grid(row = 2, column = 1, sticky = E+W+S)
		self.lab_det_max.grid(row = 2, column = 2, sticky = E+W+S)

		#print the grid size
		print self.Tree.grid_size()

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
					self.Tree.insert(id, "end", text = files[i], tags = str(spot))
				##come through and add styling to it like picture and such
			#if it is a folder add it to the tree and use recursion to start in that folder and work inside out
			else:
				#handle case if it is the first level
				if (id == "start"):
					newID = self.Tree.insert("", "end", text = files[i], tags = str(-1))
					##add pictures and stuff
				else:
					newID = self.Tree.insert(id, "end", text = files[i], tags = str(-1))
					##add pictures and such
				#create the new path for the next iteration
				newPath = path + "/" + files[i]
				#feed the call the id of the folder to make it place it under it
				self.loadTree(newPath, newID, spot + 1)

	def functions_config(self, event):
		# displays popup menu
		self.menu = Menu()

		##find the currently selected item
		item = self.Tree.focus()

		# get the file location from the selected item
		folder = self.Tree.item(item)["tags"]
		folder = folder[0]

		#if it is just a folder then do nothing with the name
		if (folder != "-1"):
			# get the file's names
			name = self.Tree.item(item)["text"]
			# get the directory location of the current file
			direct = self.dirCon[int(folder)]
			# create the file's address
			file = direct + "/" + name

			print file

			#adds the open command to the menu for the current item
			self.menu.add_command(label="Open", command=self.openFile(file))

		# initializes the label commands options after you right click
		#self.menu.add_command(label="Create", command=storeobj['Cut'])
		# self.menu.add_command(label="Paste", command=storeobj['Paste'])
		# self.menu.add_separator()
		# self.menu.add_command(label="Select All", command=storeobj['SelectAll'])
		# self.menu.add_separator()
		# displays the pop up menu
		self.menu.tk_popup(event.x, event.y)
		return

	def loadBar(self):
		self.var_det = IntVar(self)
		# finds the maximum amount of storage and the amount used
		def get_size(start_path=self._curDirectory):
			total_size = 0
			for dirpath, dirnames, filenames in os.walk(start_path):
				for f in filenames:
					fp = os.path.join(dirpath, f)
					total_size += os.path.getsize(fp)
			return '{:.2e}'.format(total_size)
		pathusedstr = str(get_size())
		pathused = pathusedstr[:4]
		self.var_det.set(pathused)

		# sets up the progress bar for the storage and the physical values of the max and used
		self.pbar_det = Progressbar(self, orient="horizontal", length=500, mode="determinate", variable=self.var_det,\
									maximum=int(5))
		self.lab_det_used = Label(self, text="Used: " + str(pathused) + " GB")
		self.lab_det_max = Label(self, text="Max: 5")


	def loadRefresh(self):
		Button(self, text="REFRESH", command=lambda: self.setupGUI()).grid(row=randint(1,100), column=randint(1,100), sticky = N+E+W+S)

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
t=GUITest(window, "/home/ARGY/Documents")
#call to set up the GUI
t.setupGUI()
#wait for the window to be closed
window.mainloop()
