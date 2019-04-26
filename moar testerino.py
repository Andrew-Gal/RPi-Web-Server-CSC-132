from Tkinter import *
from ttk import *
import ttk
import os

#############################################################################################################################################################################################################
class GUITest(Frame):
    #initialization asks for the directory to open (we want to open on the shared drive)
	def __init__ (self, parent, start):
		Frame.__init__(self, parent)
		#set the directory to the inital one just given
		self.changeDir(start)
		self.grid(sticky=E+W+N+S)
		
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
		
		##position all of the widgets in a grid
		#Tree.grid(row = 0, column = 0)

		s.grid(row=1,column=6,rowspan=10)
		#pack the tree widget to the left side with a small padding from the window border
		self.Tree.grid(row=1,column=0,rowspan=10,columnspan=3,sticky=E+W+N+S)
		
		#make the tree have the scroll bar
		s.config(command=self.Tree.yview)
		self.Tree.config(yscrollcommand=s.set)
		
		#fill the tree
		self.loadTree(self._curDirectory)

		# load the storage bar
		self.loadBar()

		# load the refresh button
		self.loadRefresh()
			
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

	def loadBar(self):
		self.var_det=IntVar(self)
                # finds the maximum amount of storage and the amount used
		def get_size(start_path=self._curDirectory):
			total_size=0
			for dirpath,dirnames,filenames in os.walk(start_path):
				for f in filenames:
					fp=os.path.join(dirpath,f)
					total_size+=os.path.getsize(fp)
			return '{:.2e}'.format(total_size)
		pathusedstr=str(get_size())
		pathused=pathusedstr[:4]
		self.var_det.set(pathused)
		# sets up the progress bar for the storage and the physical values of the max and used
		self.pbar_det=ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate", variable=self.var_det, maximum=int(5))
		self.pbar_det.grid(row=7,column=1,sticky=W+E+N+S)
		self.lab_det_used=Label(self, text="Used: " + str(pathused) + " GB")
		self.lab_det_used.grid(row=8,column=1,sticky=W+E+N+S)
		self.lab_det_max=Label(self, text="Max: 5")
		self.lab_det_max.grid(row=8,column=3,sticky=W+E+N+S)

	def loadRefresh(self):
		Button(self,text="REFRESH",command=lambda:self.setupGUI()).grid(row=2,column=2,sticky=E+W+N+S)
                        
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
t=GUITest(window, "C:/Users/and41/Documents/Desktop Folders") #C:/Programming Projects/Python
#call to set up the GUI
t.setupGUI()
#wait for the window to be closed
window.mainloop()
