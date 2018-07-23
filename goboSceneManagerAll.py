#install in python interface
#import fixSceneManager
#reload(fixSceneManager)

#def createInterface():
#    return     fixSceneManager.fixSceneManagerClass()
# Z:\lacoste\prods\xmas18\xmas18_01\xmas18_01_006\fx\work\houdini

from PySide2 import QtWidgets
import os
import hou
import applyScript
print "Houdini c'est cool, Copperfield c'est mieu !"

class fixSceneManagerClass(QtWidgets.QWidget): 
    
    def __init__(self):
        super(fixSceneManagerClass,self).__init__()

        self.setupUi()
        self.setupList()
        self.buttonConnect()
        self.afficherLaNote()


    def setupUi(self):


        self.roots = "Z:/"
        #variable widget
        self.projectLine=QtWidgets.QLineEdit()
        self.projectLine.setPlaceholderText("type project name")
        self.stepLine=QtWidgets.QLineEdit()
        self.shotNameLine=QtWidgets.QLineEdit()
        self.startNameLine=QtWidgets.QLineEdit()
        self.endNameLine=QtWidgets.QLineEdit()
        #variable
        self.projectLine.setText("lacoste")
        self.projectName=self.projectLine.text() 
        self.stepLine.setText("fx")
        self.step=self.stepLine.text() 		
        #search hip file throug any path
        self.anyPath=QtWidgets.QLineEdit()
        self.anyPath.setPlaceholderText('type any path to list hip file')
        self.boutonListfromAnyPath=QtWidgets.QPushButton("listFromAnyPath")
        self.anyName=self.anyPath.text()	
        #setup path
        self.sequencesRoots= self.roots+self.projectName+"/prods/xmas18/"
        #les widgets
        self.label = QtWidgets.QLabel(self.sequencesRoots)
        #filter list
        self.filtrer=QtWidgets.QLineEdit()
        self.filtrer.setPlaceholderText('project filter he oh')
        #list
        self.listWidget = QtWidgets.QListWidget()
        # refresh 
        self.refreshBouton=QtWidgets.QPushButton("filter and reload stg variable !")
        self.allProjectName=QtWidgets.QPushButton("print filter project name")
        self.versionUp=QtWidgets.QPushButton("versionUp")
        self.openAndScript=QtWidgets.QPushButton("openSceneAndApplyScript")
        self.textScript=QtWidgets.QPlainTextEdit()
        self.textScript.setPlaceholderText('pasteScriptHere')

        #layout
        mainLayout=QtWidgets.QVBoxLayout()
        #add widget to layout
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.projectLine)
        mainLayout.addWidget(self.stepLine)
        mainLayout.addWidget(self.anyPath)
        mainLayout.addWidget(self.boutonListfromAnyPath)
        #widget util
        mainLayout.addWidget(self.filtrer)
        mainLayout.addWidget(self.refreshBouton)
        mainLayout.addWidget(self.allProjectName)
        mainLayout.addWidget(self.versionUp)
        mainLayout.addWidget(self.openAndScript)
        mainLayout.addWidget(self.textScript,0,0)
        mainLayout.addWidget(self.listWidget,5,0)
        #set layout
        self.setLayout(mainLayout)

    def variablesReload(self):
        newProject = self.projectLine.text()
        newStep = self.stepLine.text()
        print newStep
        self.stepLine.setText(newStep)
        self.step=self.stepLine.text() 
        print self.stepLine.text()
        self.projectLine.setText(newProject)
        self.projectName=self.projectLine.text()
        self.sequencesRoots= self.roots+self.projectName+"/prods/xmas18/"
        self.label = QtWidgets.QLabel(self.sequencesRoots)
        self.anyName=self.anyPath.text()


        print"reload !"



    def openScene(self,hipName):
        hipFile=hipName.data()
        hou.hipFile.load(hipFile)
        self.variablesReload()

    def hipNameFromList(self,hipName):
        self.hipFileFromList=hipName.data()

    def afficherLaNote(self):
        hipPath = hou.expandString('$HIP')
        applyScriptPath= hipPath + "/applyScript.py"
        with open (applyScriptPath,'r') as f:
            contenuDeLaNote = f.read()
            #print contenuDeLaNote
			
        print contenuDeLaNote
        self.textScript.setPlainText(contenuDeLaNote)
	
	
    def openSceneAndApplyScript(self):
        #hipFile=self.hipFileFromList
        #hou.hipFile.load(hipFile)
        #reload variables
        #self.variablesReload()
        #print os.path.realpath(__file__)
        
        myScriptToWrite=self.textScript.toPlainText()
        hipPath = hou.expandString('$HIP')
        applyScriptPath= hipPath + "/applyScript.py"
        print applyScriptPath
        writeMyScript = open(applyScriptPath, 'w')
        writeMyScript.write(myScriptToWrite)
        reload (applyScript)
        #applyScript.temp()

        #print"openSceneAndApplyScript"


    def incrementScene(self):
        hou.hipFile.saveAndIncrementFileName()

    def printProjectName(self):

        print "projectNames"
        sortList=[]
        tempProj = []
        for proj in os.walk(self.roots).next()[1]:

            tempProj.append(proj)

        sortList= sorted(tempProj)
        selectionFilter=self.filtrer.text()
        filtreProj= []

        if len(selectionFilter) == 0:
            print sortList
        else :
            for listElement in sortList:
                if selectionFilter in listElement:
                    print listElement
 

    def setupList(self):
        print self.sequencesRoots
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
            tempList=["ouvrir une scene deja pipe ou en creer une, puis appuier sur les fleches en haut a gauche "]
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


    def setupAnyList(self):
        print self.anyName
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

        for dir in os.walk(self.anyName).next()[1]:
            projLevelOne = self.anyName+dir
            for file in os.listdir(projLevelOne):
                if file.endswith('.hip'):
                    hipPath = projLevelOne+"/"+file
                    tempList.append(hipPath)

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
        self.refreshBouton.clicked.connect(self.variablesReload)
        self.refreshBouton.clicked.connect(self.setupList)

        self.boutonListfromAnyPath.clicked.connect(self.variablesReload)
        self.boutonListfromAnyPath.clicked.connect(self.setupAnyList)

        self.listWidget.doubleClicked.connect(self.openScene)

        self.allProjectName.clicked.connect(self.printProjectName)
        self.versionUp.clicked.connect(self.incrementScene)


        #self.listWidget.clicked.connect(self.hipNameFromList)
        self.openAndScript.clicked.connect(self.openSceneAndApplyScript)


#to do

#recupperer le bouton publish de shotgun

#python script: ouvre la scene selectionnee et lui applique un script
# une texte box et un bouton qui lance le script
#donc il faut creer un fichier script temp a la racine de script pour le stocker et l'appeler apres

#list widget

#ajouter la fonction merge 
#from selectListWidgetItem

#faire des onglet pour mettre tout les scripts en une seul interface


