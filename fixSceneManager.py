#install in python interface
#import fixSceneManager
#reload(fixSceneManager)

#def createInterface():
#    return     fixSceneManager.fixSceneManagerClass()


from PySide2 import QtWidgets

import os
import hou
print "Hello from fixSceneManager"

class fixSceneManagerClass(QtWidgets.QWidget): 
    
    def __init__(self):
        super(fixSceneManagerClass,self).__init__()

        #/prod/project/LANCOME_LVEB_17_1358/sequences/001/001_0053/sfx/work/houdini
        #declare project variables
        self.roots = "/prod/project/"

        self.projectLine=QtWidgets.QLineEdit()
        self.projectLine.setText(hou.expandString("$PROJECT_NAME"))
        self.projectName=self.projectLine.text() 
        
        self.stepLine=QtWidgets.QLineEdit()
        self.stepLine.setText(hou.expandString("$STEP"))
        self.step=self.stepLine.text() 

        self.stepLine=QtWidgets.QLineEdit()
        self.stepLine.setText(hou.expandString("$STEP"))
        self.step=self.stepLine.text()

        self.shotNameLine=QtWidgets.QLineEdit()
        self.shotNameLine.setText(hou.expandString("$SHOT_NAME"))

        self.startNameLine=QtWidgets.QLineEdit()
        self.startNameLine.setText(hou.expandString("$START_FRAME"))

        self.endNameLine=QtWidgets.QLineEdit()
        self.endNameLine.setText(hou.expandString("$END_FRAME"))

        self.sequencesRoots= self.roots+self.projectName+"/sequences/"
        
        #les widgets
        self.label = QtWidgets.QLabel(self.sequencesRoots)
        #filter
        self.filtrer=QtWidgets.QLineEdit()
        self.filtrer.setPlaceholderText('project filter')
        #list widget
        self.listWidget = QtWidgets.QListWidget()
        # refresh widget
        self.refreshBouton=QtWidgets.QPushButton("refresh")
        
        #layout
        mainLayout=QtWidgets.QVBoxLayout()

        #add widget to layout
        #info variable shotgun
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.projectLine)
        mainLayout.addWidget(self.stepLine)
        mainLayout.addWidget(self.shotNameLine)
        mainLayout.addWidget(self.startNameLine)
        mainLayout.addWidget(self.endNameLine)
        #widget util
        mainLayout.addWidget(self.filtrer)
        mainLayout.addWidget(self.refreshBouton)
        mainLayout.addWidget(self.listWidget)
        #set layout
        self.setLayout(mainLayout)

        print "class"
        self.createInterface()




    def openScene(self,hipName):

        hipFile=hipName.data()
        hou.hipFile.load(hipFile)
        print "openScene Actif"


    def createInterface(self):
        #create and clear all List
        tempList = []
        del tempList[:]
        sortList= []
        del sortList[:]
        listeFlitre=[]
        del listeFlitre[:]
        self.listWidget.clear()

        #iteration dans les dossiers 
        for seq in os.walk(self.sequencesRoots).next()[1]:        
            seqPath = self.sequencesRoots+seq+"/"
            #iteration dans les shot
            for shot in os.walk(seqPath+"/").next()[1]:
                shotPath = seqPath+shot+"/"
                #check if the path already exist    
                try:
                    for file in os.listdir(shotPath+self.step+"/work/houdini/"):
                        if file.endswith('.hip'):
                            hipPath = shotPath+self.step+"/work/houdini/"+file
                            tempList.append(hipPath)
                except(OSError): 
                    pass

        #sortList by alphabetical order
        sortList= sorted(tempList)
        # systeme de filtres par mot
        selectionFilter=self.filtrer.text()
        # test if there is a key word to filter the list with
        if len(selectionFilter) == 0:
            listeFlitre=sortList
        else :
            for listElement in sortList:
                if selectionFilter in listElement:
                    listeFlitre.append(listElement)
        print listeFlitre

        for hipPathSorted in listeFlitre:
            self.listWidget.addItem(hipPathSorted)

        print "fixSceneManager scanning is a sucess !"

        self.refreshBouton.clicked.connect(self.createInterface)

        self.listWidget.doubleClicked.connect(self.openScene)

