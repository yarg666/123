#install in python interface
#import yProjectManager
#reload(yProjectManager)

#def createInterface():
#    return yProjectManager.yProjectManagerClass()
from PySide2 import QtWidgets
import os
import hou
print "Hello from yProjectManager"

class yProjectManagerClass(QtWidgets.QWidget): 

	def __init__(self):
		super (yProjectManagerClass,self).__init__()
		#variables de projet
		self.proj="/media/vfx/"
		#les widgets
		self.roots=QtWidgets.QLineEdit(self.proj)
		self.filtrer=QtWidgets.QLineEdit()
		self.filtrer.setPlaceholderText('project filter')
		self.refreshBouton=QtWidgets.QPushButton("refresh")
		self.listWidget = QtWidgets.QListWidget()
	    #le layout
		mainLayout=QtWidgets.QVBoxLayout()
		mainLayout.addWidget(self.roots)
		mainLayout.addWidget(self.filtrer)
		mainLayout.addWidget(self.refreshBouton)
		mainLayout.addWidget(self.listWidget)
		self.setLayout(mainLayout)
		self.newInterface()
		print"classy" 

	def openScene(self,hipName):
	    hipFile=hipName.data()
	    #open hipFile
	    hou.hipFile.load(hipFile)
	    print"open"

	def newInterface(self):

		self.proj=self.roots.text()
		self.listWidget.clear()
		#boucle qui list les hip dans les dossiers
		tempList=[]

		for dir in os.walk(self.proj).next()[1]:
			projLevelOne = self.proj+dir
			for file in os.listdir(projLevelOne):
				if file.endswith('.hip'):
					hipPath = projLevelOne+"/"+file
					tempList.append(hipPath)
		#triage de la liste
		sortList=sorted(tempList)
		# systeme de filtres par mot
		selectionFilter=self.filtrer.text()
		listeFlitre=[]
		# test if there is a key word to filter the list with
		if len(selectionFilter) == 0:
			listeFlitre=sortList
		else :
			for listElement in sortList:
				if selectionFilter in listElement:
					listeFlitre.append(listElement)
		# assigne la liste filtrer au widget liste
		for hipPathSorted in listeFlitre:
			self.listWidget.addItem(hipPathSorted)
		# set widget connection
		print "create"
		self.listWidget.doubleClicked.connect(self.openScene)
		self.refreshBouton.clicked.connect(self.newInterface)
		return self.listWidget
		




