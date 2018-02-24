#install in python interface
#import fixSceneManager
#reload(fixSceneManager)

#def createInterface():
#    return 	fixSceneManager.createInterface()


from hutil.Qt import QtWidgets
import os
import hou

print "Hello fixSceneManager"

def openScene(hipName):

    hipFile=hipName.data()
     
    #open hipFile
    hou.hipFile.load(hipFile)
    
def createInterface():
    
    #declare project variables
    roots = "/home/yarg/"
    projectName= "projetTest"
    step="sfx" 
    
    projectRoots= roots+projectName+"/sequence/"
    #les widgets
    widget = QtWidgets.QLabel(projectRoots)
    listWidget = QtWidgets.QListWidget()
    
    #iteration dans les dossiers 
    for seq in os.walk(projectRoots).next()[1]:        
        seqPath = projectRoots+seq
        #print seqPath
        for shot in os.walk(seqPath+"/shot/").next()[1]:
            shotPath = seqPath+"/shot/"+shot + "/"
            print shotPath
            for file in os.listdir(shotPath+step+"/houdini/"):
                if file.endswith('.hiplc'):
                    hipPath = shotPath+step+"/houdini/"+file
                    print hipPath
                    #print file
                    listWidget.addItem(hipPath)
    
    listWidget.doubleClicked.connect(openScene)                    
    return listWidget    
    