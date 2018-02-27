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
        self.listWidget = QtWidgets.QListWidget()

        # refresh widget
        self.refreshBouton = QtWidgets.QPushButton('refresh')


        
        self.createInterface()
        #layout
        mainLayout=QtWidgets.QVBoxLayout()

        #add widget to layout
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.projectLine)
        mainLayout.addWidget(self.stepLine)
        mainLayout.addWidget(self.shotNameLine)
        mainLayout.addWidget(self.startNameLine)
        mainLayout.addWidget(self.endNameLine)
        mainLayout.addWidget(self.refreshBouton)
        mainLayout.addWidget(self.listWidget)

        self.setLayout(mainLayout)

    def setupConnections(self):
        self.refreshBouton.clicked.connect(self.refreshPannel)

    def refreshPannel(self):

        print ("refresh")

    def openScene(self, hipName):

        hipFile=hipName.data()
        #open hipFile
        hou.hipFile.load(hipFile)
        self.shotNameLine.update()
        print hipFile

    def createInterface(self):

        tempList = []

        #iteration dans les dossiers 
        for seq in os.walk(self.sequencesRoots).next()[1]:        
            seqPath = self.sequencesRoots+seq+"/"
            #print seqPath+"seqPath"
            for shot in os.walk(seqPath+"/").next()[1]:
                shotPath = seqPath+shot+"/"
                #print shotPath+"shotpath"
                #check if the path already exist    
                try:
                    for file in os.listdir(shotPath+self.step+"/work/houdini/"):
                        #print "path exist"
                        if file.endswith('.hip'):
                            hipPath = shotPath+self.step+"/work/houdini/"+file
                            #print hipPath+" hipPath"
                            #print file
                            tempList.append(hipPath)
                            #print self.listWidget
                except(OSError): 
                    pass

        #sortList by alphabetical order
        sortList= sorted(tempList)
        for hipPathSorted in sortList:
            self.listWidget.addItem(hipPathSorted)


        print "fixSceneManager scanning is a sucess !"
        self.listWidget.doubleClicked.connect(self.openScene)
