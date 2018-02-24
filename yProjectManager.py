#install in python interface
#import yProjectManager
#reload(yProjectManager)

#def createInterface():
#    return yProjectManager.createInterface()




from hutil.Qt import QtWidgets
import os
import hou

print "Hello yProjectManager"

def openScene(hipName):

    hipFile=hipName.data()
     
    #open hipFile
    hou.hipFile.load(hipFile)
    
def createInterface():

    proj = "/media/vfx/"
    widget = QtWidgets.QLabel(proj)
    listWidget = QtWidgets.QListWidget()
    
    
    for dir in os.walk(proj).next()[1]:
        projLevelOne = proj+dir
        for file in os.listdir(projLevelOne):
            if file.endswith('.hip'):
                hipPath = projLevelOne+"/"+file 
                #print hipPath
                #print file
                listWidget.addItem(hipPath)
                
    listWidget.doubleClicked.connect(openScene)
    
    return listWidget
