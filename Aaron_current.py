from Tkinter import *
from ttk import *
import os
import subprocess
import shutil
from time import sleep

#############################################################################################################################################################################################################
# noinspection PyUnreachableCode
class GUITest(Frame):
	#initialization asks for the directory to open (we want to open on the shared drive)
	def __init__ (self, parent, start):
		Frame.__init__(self, parent)
		#set the directory to the inital one just given
		self.changeDir(start)
		#self.grid(sticky=N+E+W+S)
		self.parent = parent

	#getter and setter for curDirectory
	@property
	def curDirectory (self):
		return self._curDirectory
	@curDirectory.setter
	def curDirectory (self, location):
		self._curDirectory = location

	def setupGUI(self):

		#setup different frames for different parts of the windowframe to hold
		#main frame to hold everything
		#change rowspan and columnspan to adapt to more widgets
		self.mainFrame = Frame(self.parent)
		self.mainFrame.grid(row = 0, rowspan = 2, column = 0, columnspan = 4, sticky = "nsew")

		#frame to hold the tree
		self.treeFrame = Frame(self.mainFrame)
		self.treeFrame.grid(row = 1, column =0, columnspan = 4, sticky = "nsew")
		self.treeFrame.grid_rowconfigure(1, weight = 1)
		self.treeFrame.grid_columnconfigure(0, weight = 2)
		self.treeFrame.grid_columnconfigure(1, weight = 1)

		#frame to hold the progressbar and its labels
		self.barFrame = Frame(self.mainFrame)
		self.barFrame.grid(row = 2, column = 0, columnspan = 4, sticky = "nsew")
		self.barFrame.grid_rowconfigure(2, weight = 1)
		self.barFrame.grid_columnconfigure(0, weight = 1)
		#make column 2 adjust the most
		self.barFrame.grid_columnconfigure(1, weight = 2)
		self.barFrame.grid_columnconfigure(2, weight = 1)
		self.barFrame.grid_columnconfigure(3, weight = 1)
		
		#frame to hold the taskbar
		self.taskbarFrame = Frame(self.mainFrame)
		self.taskbarFrame.grid(row = 0, column = 0, columnspan = 5, sticky = "nsew")
		self.taskbarFrame.grid_rowconfigure(0, weight = 1)
		self.taskbarFrame.grid_columnconfigure(0, minsize = WIDTH/10, weight = 0)
		self.taskbarFrame.grid_columnconfigure(1, minsize = WIDTH / 10, weight = 0)
		self.taskbarFrame.grid_columnconfigure(2, weight = 1)
		self.taskbarFrame.grid_columnconfigure(3, minsize = 2*WIDTH/5, weight = 0)
		self.taskbarFrame.grid_columnconfigure(4, minsize = WIDTH/10, weight = 0)

		#reconfigure the main grid to adjust to the new rows and columns being used
		#use minsize to set the size of the rows and columns
		#do so with proportions of WIDTH and HEIGHT to keep everything proportional
		self.mainFrame.grid_rowconfigure(0, minsize = HEIGHT/40)
		self.mainFrame.grid_rowconfigure(1, minsize = 18*HEIGHT/20)
		self.mainFrame.grid_rowconfigure(2, minsize = 3*HEIGHT/40)
		self.mainFrame.grid_columnconfigure(1, minsize = WIDTH)

		#create the scroll bar
		s = Scrollbar(self.treeFrame)
		#create the hiearchy tree
		self.Tree = Treeview(self.treeFrame)
		#create the progressbar reset button
		rst = Button(self.barFrame, text="REFRESH", command=lambda: self.setupGUI())

		#set the tree to call to open a file when double clicked
		self.Tree.bind("<Double-1>", self.dubClick)
		# set the button to call to open the command options when right clicked
		self.Tree.bind("<Button-3>", self.functions_config)

		#make the tree have the scroll bar
		s.config(command=self.Tree.yview)
		self.Tree.config(yscrollcommand=s.set)

		#fill the tree
		self.loadTree(self._curDirectory)

		# load the storage bar
		self.loadBar()
		
		#load the task bar
		self.loadTask()

		#setup all widgets in the grid
		self.Tree.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew")
		s.grid(row = 1, column = 2, sticky = "nsew")
		self.pbar_det.grid(row = 2, column = 1, sticky = "nsew")
		self.lab_det_used.grid(row =2,column = 0, sticky = "nsew")
		self.lab_det_max.grid(row = 2, column = 2, sticky = "nsew")
		rst.grid(row = 2, column = 3, sticky = "nsew")
		self.File.grid(row = 0, column = 0, sticky = "nsew")
		self.Edit.grid(row = 0, column = 1, stick = "nsew")
		self.searchBar.grid(row = 0, column = 3, sticky ="nsew")
		self.searchButton.grid(row = 0, column = 4, sticky = "nsew")

	#list all files from a directory into an array
	def changeDir (self, dir):
		#set curDir to the new directory
		self._curDirectory = dir
		#set dirFiles to a list of all the file names in the directory
		self._dirFiles = sorted(os.listdir(self._curDirectory))
		#empty the directory count array
		self.dirCon = []
		#empty the id array
		self.ids = []
		#empty array of items
		self.items = []
		
	#function to open a file from its default program
	##need to fix to work with spaces in file/folder names
	def openFile (self, file):
		try:
			#subprocess calls to open the file
			subprocess.call(("xdg-open", file))
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
	def loadTree (self, path, id = "", spot = 0):
		#if the id is "start" then there is no tree yet so dont feed calls the id
		#if no spot is provided then it is first start, so now spot counts to keep an item tag equal to an index to link to its directory path
		
		#add the current directory path to the array so it can be found later
		self.dirCon.append(path)
		
		#add the id to the array
		self.ids.append(id)
		
		#iset files array for the given path
		files = sorted(os.listdir(path))
		
		#loop through for the number of files in the directory
		for i in range(len(files)):
			#check to see if the item is a file or a folder
			#create the full address
			full = path + "/" + files[i]
			#variable to hold the true or false
			file = os.path.isfile(full)
			
			#if it is a file just add it to the tree at the end of the hiearchy
			if (file == True):
				#handle case if it is the first level
				identity = self.Tree.insert(id, "end", text = files[i], tags = str(spot))
				#append identity to self.items
				self.items.append(identity)
				##come through and add styling to it like picture and such
			#if it is a folder add it to the tree and use recursion to start in that folder and work inside out
			else:
				newID = self.Tree.insert(id, "end", text = files[i], tags = str(-1))
				##add pictures and such
				#append NewID to self.items (cause it is like that inclusive/exclusive stuff)
				self.items.append(newID)
				#create the new path for the next iteration
				newPath = path + "/" + files[i]
				#feed the call the id of the folder to make it place it under it
				self.loadTree(newPath, newID, spot + 1)

	def functions_config(self, event):
		# displays popup menu
		self.menu = Menu(self.treeFrame, tearoff = 0)

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

		#adds the open command to the menu for the current item
		self.menu.add_command(label="Open", command= lambda: self.openFile(file))
		#adds the create folder command
		self.menu.add_command(label = "Create Folder", command = lambda: self.createFolder())
		#add the rename command to the list
		self.menu.add_command(label = "Rename", command = lambda: self.rename(direct, file, item))
		#add the delete command to the list
		self.menu.add_command(label = "Delete", command = lambda: self.delete(direct, item))
		
		##########
		# Needed #
		##########
		#1-copy
		#2-cut
		#3-paste
		##further investigation proved working with the windows clipboard is rather frustrating

		# initializes the label commands options after you right click
		#self.menu.add_command(label="Create", command=storeobj['Cut'])
		# self.menu.add_command(label="Paste", command=storeobj['Paste'])
		# self.menu.add_separator()
		# self.menu.add_command(label="Select All", command=storeobj['SelectAll'])
		# self.menu.add_separator()
		# displays the pop up menu
		
		self.menu.tk_popup(event.x, event.y)
		return
	
	#function to copy a file to a select location
	def copyTo (self):
		# general process of the getting the file and such
		##find the currently selected item
		item = self.Tree.focus()
		
		# get the file location from the selected item
		folder = self.Tree.item(item)["tags"]
		folder = folder[0]
		
		# if it is just a folder then do nothing with the name
		if (folder != "-1"):
			# get the file's names
			name = self.Tree.item(item)["text"]
			# get the directory location of the current file
			direct = self.dirCon[int(folder)]
			# create the file's address
			file = direct + "/" + name
			
		#get the requested location to copy the file to
		target = self.inputWindow()
		
		#try to copy it
		try:
			shutil.copy(file, target)
		except OSError:
			print "Error"
		
	#method to delete a file or folder and remove it from the tree
	def delete (self, file, item):
		#delete the item from the tree
		
		#if it is a folder it needs to delete everything inside of it
	
		self.Tree.delete(item)
		
		#delete the file or folder from the os
		try:
			os.remove(file)
		except OSError:
			shutil.rmtree(file)
		
	#method to renae a file
	def rename (self, folder, file, item):
		#ask for the new name
		name = self.inputWindow()
		
		#change the name in the tree view
		self.Tree.item(item, text = name)
		
		#change the name in the os file system
		#first make the new directory
		new = folder + "/" + name
		#then change dat dang
		try:
			os.rename(file, new)
		except OSError:
			print "Error"

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
		self.pbar_det = Progressbar(self.barFrame, orient=HORIZONTAL, length = 100, mode="determinate", variable=self.var_det,\
									maximum=int(5))
		#self.pbar_det.grid(row = 0)
		self.lab_det_used = Label(self.barFrame, text="Used: " + str(pathused) + " GB")
		self.lab_det_max = Label(self.barFrame, text="Max: 5")
		
	#function to load up the taskbar at the top
	def loadTask (self):
		##File##
		# make the menubutton
		self.File = Menubutton(self.taskbarFrame, text = "File")
		#create a menu to hold all of the options for File
		self.File.menu = Menu(self.File, tearoff = 0)
		#add all the commands
		self.File.menu.add_command(label = "New Window", command = lambda: self.newWindow())
		self.File.menu.add_command(label = "Change Folder", command = lambda: self.changeFolder())
		self.File.menu.add_command(label = "Close", command = lambda: self.quit())
		#set the menu to the menubutton
		self.File["menu"] = self.File.menu
		
		##Edit##
		# make the menubutton
		self.Edit = Menubutton(self.taskbarFrame, text = "Edit")
		# create a menu to hold all of the options for File
		self.Edit.menu = Menu(self.Edit, tearoff = 0)
		# add all the commands
		self.Edit.menu.add_command(label = "Move To", command = lambda: self.moveTo())
		self.Edit.menu.add_command(label = "Copy To", command = lambda: self.copyTo())
		# set the menu to the menubutton
		self.Edit["menu"] = self.Edit.menu
		
		##Search Bar##
		#make the entry for the user to type into
		self.searchBar = Entry(self.taskbarFrame)
		#create the button to click and search
		self.searchButton = Button(self.taskbarFrame,text = "Search", command = lambda: self.search())
		
	#method to search through the tree and hide all items without the key word/phrase
	def search (self):
		#OH NO, NO, No, NO
		#must reattach folders
		
		#reenable all items before searching through them
		
		#just restart the whole tree, who really cares at this point :(
		self.Tree.delete(*self.Tree.get_children())
		#self.Tree = Treeview(self.treeFrame)
		self.changeDir(self._curDirectory)
		self.loadTree(self._curDirectory)
		
		# #loop through all items and make sure to turn them on
		# if (len(self.off) > 0):
		# 	print "got it"
		# 	for m in self.items:
		# 		if m in self.off:
		# 			self.Tree.reattach(self.Tree.item(m))
		
		##restart the tree before sorting
		#self.Tree = Treeview(self.treeFrame)
		#self.changeDir(self._curDirectory)
		#self.loadTree(self._curDirectory)
			
		#get the string from the search bar entry
		key = self.searchBar.get()
		
		# #get an array of all the the children in the tree
		# children = self.Tree.get_children()
		#
		# for l in self.ids:
		# 	tempp = self.Tree.get_children(self.Tree.item(l))
		# 	children = list(children) + list(tempp)
		
		#loop through all the items and detach any without key in their text
		for n in self.items:
			if not(n in self.ids):
				if not(key in self.Tree.item(n)["text"]):
					self.Tree.delete(n)
			
		#if a folder without the key in its name doesn't have an attached file, detach it
		#needs to go backwards so that it will delete folders in folders
		for z in range(0, len(self.ids)-1):
			spottie = len(self.ids) - (z+1)
			if (len(self.Tree.get_children(self.ids[spottie])) == 0):
				if not(key in self.Tree.item(self.ids[spottie])["text"]):
					self.Tree.delete(self.ids[spottie])
			
		# for o in range(len(self.items)):
		# 	if self.items[o] in self.ids:
		# 		#next folder is the next one in self.ids
		# 		#everything between is the first's files
		# 		#variable to hold index of next folder
		# 		nxt = None
		# 		#loop and find the next folder
		# 		for p in range(o, len(self.items)):
		# 			if self.items[p] in self.ids:
		# 				nxt = p
		# 				break
		# 		#if w is none then it is the last folder
		# 		#set a variable to tell which spot to stop at
		# 		if (nxt == None):
		# 			spot = len(self.items)
		# 		else:
		# 			spot = nxt
		#
		# 		#boolean to hold if the folder had a live file or not
		# 		hot = False
		#
		# 		#loop and find file thats are under this folder
		# 		for q in range(o + 1, nxt):
		# 			if (key in self.Tree.item(q)):
		# 				hot = True
		#
		# 		#if hot is still False then the folder needs to be detached
		# 		if (hot == False):
		# 			#make sure that the file name doesn't have the key before detaching
		# 			if not(key in self.Tree.item(self.items[o])["text"]):
		# 				self.Tree.detach(self.items[o])
		#
		# 		#check to see if there are any files in the folder
		# 		if ((nxt - o) == 1):
		# 			if not(key in self.Tree.item(o)["text"]):
		# 				self.Tree.delete(self.Tree.item(o))
		
		
	#method to open a new window of this file browser
	def newWindow (self):
		#create the new window as a top level so that it appears above the currently selected
		extra = Tk()
		# set the window title
		extra.title("Pi Server Manager")
		# actually set the size of the window instead of just having pointless constants stated
		extra.geometry(str(WIDTH) + "x" + str(HEIGHT))
		# create an instance of GUITest and feed it a default directory
		f = GUITest(extra, self._curDirectory)
		# call to set up the GUI
		f.setupGUI()
		# wait for the window to be closed
		extra.mainloop()
	
	#method to change the directory and refresh the tree
	def changeFolder (self):
		#get the new directory to go to
		destination = self.inputWindow()
		
		#change the directory
		self.changeDir(destination)
		
		#reset the window to reset the tree
		self.setupGUI()
		
	#method to move a file or folder to a new directory
	def moveTo (self):
		# general process of the getting the file and such
		##find the currently selected item
		item = self.Tree.focus()
		
		# get the file location from the selected item
		folder = self.Tree.item(item)["tags"]
		folder = folder[0]
		
		# if it is just a folder then do nothing with the name
		if (folder != "-1"):
			# get the file's names
			name = self.Tree.item(item)["text"]
			# get the directory location of the current file
			direct = self.dirCon[int(folder)]
			# create the file's address
			file = direct + "/" + name
		
		#get the target destination
		target = self.inputWindow()
		
		#try to move the file or folder
		try:
			shutil.move(file, target)
		except OSError:
			print "Error"
		
	#function to create a window to ask for input and then returns the input
	def inputWindow (self):
		
		# create an empty variable to hold the users message
		text = None

		# create a temporary window
		root = Toplevel()
		
		# entry label
		e1 = Entry(root)
		e1.grid(row = 0, column = 0, columnspan = 2)
		
		# creating the buttons
		button1 = Button(root, text = "Ok", command = lambda: root.quit())
		button1.grid(row = 1, column = 1)
		button2 = Button(root, text = "Cancel", command = lambda: root.destroy()) #destroys the window and stops the mainloop
		button2.grid(row = 1, column = 0)
		
		root.columnconfigure(0, weight = 1)
		
		root.mainloop()
		
		text = e1.get()
		
		return text

	def createFolder (self):
			
		#get the name from the input window
		name = self.inputWindow()
		
		#def namegrab ():
		#name.append(e1.get())
		
		if (name != None):
			
			####
			#get the item which is currently selected
			item = self.Tree.focus()
			#get the directory address from it
			folder = self.Tree.item(item)["tags"]
			id = int(folder[0])
			#ready the path
			path = self.dirCon[id] + "/" + name
			#get the id
			id = self.ids[id]
			
			#create the new folder on the computer
			try:
				os.mkdir(path)
			except OSError:
				print "Failed to create folder"
			
			#add the folder to the tree
			newID = self.Tree.insert(id, "end", text = name, tags = str(-1))
			#####################################################
			################## FIX THIS SHIT ####################
			#####################################################
			
			#append the directory to the directory array
			self.dirCon.append(path)
			self.ids.append(newID)

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
t=GUITest(window, "/home/ARGY/Pictures")
#call to set up the GUI
t.setupGUI()
#wait for the window to be closed
window.mainloop()
