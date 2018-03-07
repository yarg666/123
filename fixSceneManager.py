#install in python interface
#import fixSceneManager
#reload(fixSceneManager)

#def createInterface():
#    return     fixSceneManager.fixSceneManagerClass()


from PySide2 import QtWidgets

import os
import hou
print "Houdini c'est cool, Copperfield c'est mieu !"

class fixSceneManagerClass(QtWidgets.QWidget): 
    
    def __init__(self):
        super(fixSceneManagerClass,self).__init__()



        self.setupUi()
        self.setupList()
        self.buttonConnect()


    def setupUi(self):


        self.roots = "/prod/project/"
        #variable widget
        self.projectLine=QtWidgets.QLineEdit()
        self.stepLine=QtWidgets.QLineEdit()
        self.shotNameLine=QtWidgets.QLineEdit()
        self.startNameLine=QtWidgets.QLineEdit()
        self.endNameLine=QtWidgets.QLineEdit()
        #variable
        self.projectLine.setText(hou.expandString("$PROJECT_NAME"))
        self.projectName=self.projectLine.text() 
        self.stepLine.setText(hou.expandString("$STEP"))
        self.step=self.stepLine.text() 
        self.shotNameLine.setText(hou.expandString("$SHOT_NAME"))
        self.startNameLine.setText(hou.expandString("$START_FRAME"))
        self.endNameLine.setText(hou.expandString("$END_FRAME"))
        #setup path
        self.sequencesRoots= self.roots+self.projectName+"/sequences/"
        #les widgets
        self.label = QtWidgets.QLabel(self.sequencesRoots)
        #filter list
        self.filtrer=QtWidgets.QLineEdit()
        self.filtrer.setPlaceholderText('project filter')
        #list
        self.listWidget = QtWidgets.QListWidget()
        # refresh 
        self.refreshBouton=QtWidgets.QPushButton("reload !")
        self.fixImportBouton=QtWidgets.QPushButton("createFixImportandBuildScene")
        #layout
        mainLayout=QtWidgets.QVBoxLayout()
        #add widget to layout
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.projectLine)
        mainLayout.addWidget(self.stepLine)
        mainLayout.addWidget(self.shotNameLine)
        mainLayout.addWidget(self.startNameLine)
        mainLayout.addWidget(self.endNameLine)
        #widget util
        mainLayout.addWidget(self.filtrer)
        mainLayout.addWidget(self.refreshBouton)
        mainLayout.addWidget(self.fixImportBouton)
        mainLayout.addWidget(self.listWidget)
        #set layout
        self.setLayout(mainLayout)

    def variablesReload(self):
        self.projectLine.setText(hou.expandString("$PROJECT_NAME"))
        self.stepLine.setText(hou.expandString("$STEP"))        
        self.shotNameLine.setText(hou.expandString("$SHOT_NAME"))
        self.startNameLine.setText(hou.expandString("$START_FRAME"))
        self.endNameLine.setText(hou.expandString("$END_FRAME"))
        print"reload !"

    def createFiximport(self):
        obj = hou.node("/obj")
        children = obj.children()
        exist = 0 
        # creer un fix import si il n'existe pas encore dans la scene
        for child in children:
            if child.name() == "projectSettings":
                exist = 1
                
        if exist ==0 :
            fixImport = obj.createNode("fixImport","projectSettings")
            fixImport.parm('/obj/projectSettings/buildAndUpdateScene').pressButton()


    def openScene(self,hipName):
        #open houdini scene
        hipFile=hipName.data()
        hou.hipFile.load(hipFile)
        #reload variables
        self.variablesReload()

    def setupList(self):
        #empty list
        #create and clear all List
        self.listeFlitre=[]
        tempList = []
        del tempList[:]
        sortList= []
        del sortList[:]
        self.listeFlitre=[]
        del self.listeFlitre[:]
        self.listWidget.clear()
        #iteration dans les dossiers 

        try:
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
        except:
            tempList=["ouvrir une scene deja pipee puis appuier sur les fleches en haut a gauche "]





        #sortList by alphabetical order
        sortList= sorted(tempList)
        # systeme de filtres par mot
        selectionFilter=self.filtrer.text()
        # test if there is a key word to filter the list with
        if len(selectionFilter) == 0:
            self.listeFlitre=sortList
        else :
            for listElement in sortList:
                if selectionFilter in listElement:
                    self.listeFlitre.append(listElement)
        #list sorted
        for hipPathSorted in self.listeFlitre:
            self.listWidget.addItem(hipPathSorted)

    def buttonConnect(self):

        self.refreshBouton.clicked.connect(self.setupList)
        self.refreshBouton.clicked.connect(self.variablesReload)
        self.listWidget.doubleClicked.connect(self.openScene)
        self.fixImportBouton.clicked.connect(self.createFiximport)


#to do

#faire en sorte que le fixSceneManager ne plante pas 
#si on est hors pipe 

#linker le scene manager avec le fixImpor

#recupperer le bouton version up current scene
#recupperer le bouton publish de shotgun


#python script pour
#appliquer un script python
#a toutes les scenes 
#selctionnes dans le
#list widget

#ajouter la fonction merge 
#from selectListWidgetItem



