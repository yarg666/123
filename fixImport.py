import hou,os
import ppSgtkLibs.ppSgtkCmds as ppSgtkCmds
try:
    from ppSgtkLibs.ppProjectSettings import Project_Settings
except ImportError, e:
    from ppSgtkLibs.ppProjectUtils import Project_Settings
import tank.platform.engine
from tank_vendor import yaml

remapRoot = 'root'
remapTransform = 'transform'
settingsRoot = 'projectSettings'
remapRootNode = 'subnet'
localDrive = '/mnt/data/'

def buildAndUpdateScene(node):
    """ get infos from fix import selected """
    fixIParentPath = node.parent().path()
    fixINodePos = node.position()
    allPublishedCamera = []
    
    """ get project settings from sgtk """
    ctxSettings = Project_Settings()
    ctxSettingsList = ctxSettings.get_project_settings()
    engine = tank.platform.engine.current_engine()
    entity = engine.context.entity
    sg_entity_type = engine.context.entity["type"]
    sg_filters = [["id", "is", entity["id"]]]  
    
    """ get published infos from sgtk """
    c = ppSgtkCmds.Cmds()
    allPublished = c.get_publishedFile(entityType = c.ctx.entity.get('type'),entityName = c.ctx.entity.get('name'),publishedType = ['Alembic'])
    allPublishedCameraCamBaked = c.get_publishedFile(entityType = c.ctx.entity.get('type'),entityName = c.ctx.entity.get('name'),publishedType = ['Camera'],filters=[["code", "contains", "abc"]],name ="cambaked")
    #allPublishedCameraCamTrack = c.get_publishedFile(entityType = c.ctx.entity.get('type'),entityName = c.ctx.entity.get('name'),publishedType = ['Camera'],filters=[["code", "contains", "abc"]],name ="camtrack")
    allPublishedCamera = allPublishedCameraCamBaked
    
    """ set embeded environement variables """
    rebuild = node.parm('rebuild_root').evalAsInt()
    animation = node.parm('update_animation').evalAsInt()
    scene = node.parm('update_scene_env').evalAsInt()
    
    """ get camera settings """
    width = ctxSettingsList.get('render_render_width').get('value')
    height = ctxSettingsList.get('render_render_height').get('value')
    ratio = ctxSettingsList.get('render_render_pixelAspectRatio').get('value')
    hou.hscript("set RES_WITH = " + str(width))
    hou.hscript("set RES_HEIGHT = " + str(height))
    
    if(animation == 1):
        print "refresh animation infos"
        fields = ['sg_inframe', 'sg_outframe']
        data = engine.shotgun.find_one(sg_entity_type, filters=sg_filters, fields=fields)
        
        # get frame in frame out
        if(sg_entity_type != 'Asset'):
            in_frame = int(data.get('sg_inframe'))
            out_frame = int(data.get('sg_outframe'))
        
        else:
            in_frame = 101
            out_frame = 300
            
        preroll = ctxSettingsList.get('houdini_houdini_export_preroll').get('value')
        postroll = ctxSettingsList.get('houdini_houdini_export_postroll').get('value')
        prestock = ctxSettingsList.get('houdini_houdini_export_prestock').get('value')
        poststock = ctxSettingsList.get('houdini_houdini_export_poststock').get('value')
        frameIn = in_frame - preroll
        frameOut = out_frame + postroll
    
        hou.hscript("set START_P_FRAME = " + str(frameIn))
        hou.hscript("set END_P_FRAME = " + str(frameOut))
        hou.hscript("set START_FRAME = " + str(in_frame))
        hou.hscript("set END_FRAME = " + str(out_frame))
        hou.hscript("set START_S_FRAME = " + str(prestock))
        hou.hscript("set END_S_FRAME = " + str(poststock))
        
        node.parm('start_frame').setExpression('$START_FRAME')
        node.parm('end_frame').setExpression('$END_FRAME')
        node.parm('start_p_frame').setExpression('$START_P_FRAME')
        node.parm('end_p_frame').setExpression('$END_P_FRAME')
        node.parm('start_s_frame').setExpression('$START_S_FRAME')
        node.parm('end_s_frame').setExpression('$END_S_FRAME')
        
        node.parm('update_animation').set(0)

    if(scene == 1):
        print "refresh scene infos"
        step = engine.context.step.get('name')
        task = engine.context.task.get('name')
        project_Name = engine.context.project.get('name')
        shot_name = engine.context.entity["name"]
    
        hou.hscript("set TYPE = " + str(sg_entity_type))
        hou.hscript("set STEP = " + step)
        hou.hscript("set TASK = " + task)
        hou.hscript("set SHOT_NAME = " + shot_name)
        hou.hscript("set PROJECT_NAME = " + project_Name)
                
        node.parm('project_name').setExpression('$PROJECT_NAME')
        node.parm('type').setExpression('$TYPE')
        node.parm('Asset_Name').setExpression('$SHOT_NAME')
        node.parm('step').setExpression('$STEP')
        node.parm('task').setExpression('$TASK')        
        
        node.parm('update_scene_env').set(0)    
        
    """ launch command """
    """ check if root already exist and destroy it """
    if(rebuild == 1):
        try:
            hou.node(fixIParentPath + '/' + remapRoot).destroy()
            
        except:
            pass
        
        """ init fps """
        fps = ctxSettingsList.get('final_final_framerate').get('value')
        sf = node.parm('start_frame').eval()
        ef = node.parm('end_frame').eval()
        init_setup_the_scene(fps,int(sf),int(ef))
        createdRoot = create_rootSubnet(c.ctx.entity,node,fixIParentPath,fixINodePos,settingsRoot)
        
        """ import all published abc """
        if(allPublished != []):
            try:
                create_alembicNodes(createdRoot,allPublished)                
            except:
                pass
        else:
            print "no geometrie imported"
        
        """ import all published camera abc """    
        if(allPublishedCamera != []):
            try:
                create_alembicCamera(createdRoot,allPublishedCamera,width,height,ratio)                
            except:
                pass
        else:
            print "no camera imported"
            
            
def create_rootSubnet(context,fixINode,fixIParentPath,fixINodePos,projectSettings): 
    """ set the fix import node display """
    color = fixINode.setColor(hou.Color((0.6, 1.0, 0.6)))
    
    try:
        fixINode.setName(projectSettings)
    
    except:
        pass
    
    """ set the fix import node display """
    root = hou.node(fixIParentPath).createNode(remapRootNode,remapRoot,1)
    root.setPosition(hou.Vector2(fixINodePos[0],fixINodePos[1] - 1.5))
    color = root.setColor(hou.Color((1,0.96,0.45)))
    root.setInput(0,fixINode,0)
    
    """ create subnet transform node """  
    transform = hou.node(root.path()).createNode(remapRootNode,remapTransform,1)
    subnetOutput = root.indirectInputs()
    transform.setInput(0,subnetOutput[0])
    color = transform.setColor(hou.Color((1,0.96,0.45)))
    
    """ apply sceneScale scale to root """
    fixImportNodeName = fixINode.name()
    root.parm('tx').lock(1)
    root.parm('ty').lock(1)
    root.parm('tz').lock(1)
    root.parm('rx').lock(1)
    root.parm('ry').lock(1)
    root.parm('rz').lock(1)
    root.parm('sx').lock(1)
    root.parm('sy').lock(1)
    root.parm('sz').lock(1)
    root.parm('px').lock(1)
    root.parm('py').lock(1)
    root.parm('pz').lock(1)
    root.parm('scale').setExpression('ch("../' + fixImportNodeName + '/global_scale")')
    
    """ apply scene transform to transform """
    fixImportNodeName = fixINode.name()
    transform.parm('tx').setExpression('ch("../../' + fixImportNodeName + '/translatex")')
    transform.parm('ty').setExpression('ch("../../' + fixImportNodeName + '/translatey")')
    transform.parm('tz').setExpression('ch("../../' + fixImportNodeName + '/translatez")')
    transform.parm('rx').setExpression('ch("../../' + fixImportNodeName + '/rotatex")')
    transform.parm('ry').setExpression('ch("../../' + fixImportNodeName + '/rotatey")')
    transform.parm('rz').setExpression('ch("../../' + fixImportNodeName + '/rotatez")') 
    transform.parm('sx').lock(1)
    transform.parm('sy').lock(1)
    transform.parm('sz').lock(1)
    transform.parm('px').lock(1)
    transform.parm('py').lock(1)
    transform.parm('pz').lock(1)
    transform.parm('scale').lock(1)
    return transform
    
    
def create_alembicNodes(root,allPublished):
    allPublished.reverse()
    latestPublishedFilesName = []
    latestPublishedFiles = []
    
    for sgPf in allPublished:
        if not sgPf['name'] in latestPublishedFilesName:
            
            latestPublishedFilesName.append(sgPf['name'])
            latestPublishedFiles.append(sgPf)
            
    """ create alembic nodes """
    for latestPublishedFile in latestPublishedFiles:
                       
            """ get infos from pp_meta_data """
            meta_data = latestPublishedFile['sg_pp_meta_data']
            data = yaml.load(meta_data)
            
            abcType = data.get('abcType')
            assetName = data.get('entityInfo').get('entityName')
            entityName = data.get('entityInfo').get('name')
            entitySubType = data.get('entityInfo').get('entitySubType')
            
            """ SUBNET SUBTYPE """
            """ check and create subType Subnet """
            
            data = yaml.load(meta_data)
            
            abcType = data.get('abcType')
            assetName = data.get('entityInfo').get('entityName')
            entityName = data.get('entityInfo').get('name')
            entitySubType = data.get('entityInfo').get('entitySubType')
            
            """ SUBNET SUBTYPE """
            """ check and create subType Subnet """
            rootPath = root.path()
            subnetTypeNodePath = rootPath + '/' + entitySubType
            subnetEntityNodePath = subnetTypeNodePath + '/' + assetName
            
            rootPath = root.path()
            subnetTypeNodePath = rootPath + '/' + entitySubType
            subnetEntityNodePath = subnetTypeNodePath + '/' + assetName
            
            """ if the subnodeType doesn t exist create it """
            subnetSubTypeNode = hou.node(subnetTypeNodePath)
            
            if subnetSubTypeNode == None:
                subnetSubTypeNode = hou.node(root.path()).createNode(remapRootNode)
                subnetSubTypeNode.setName(entitySubType)
                subnetSubTypeNode.setColor(hou.Color((1,0.96,0.45)))
                subnetOutput = root.indirectInputs()
                subnetSubTypeNode.setInput(0,subnetOutput[0])
                
            """ SUBNET ASSETS  """
            """ if the subnetEntityNode doesn t exist create it """
            subnetEntityNode = hou.node(subnetEntityNodePath)
            
            if subnetEntityNode == None:
                subnetEntityNode = hou.node(subnetSubTypeNode.path()).createNode(remapRootNode)
                subnetEntityNode.setName(assetName)
                subnetEntityNode.setColor(hou.Color((1,0.96,0.45)))
                subnetOutput = subnetSubTypeNode.indirectInputs()
                subnetEntityNode.setInput(0,subnetOutput[0])
            
            """ ALEMBIC ANIM   """
            """ create alembic nodes """
            abcNode = hou.node(subnetEntityNode.path()).createNode('alembicarchive')
                        
            try:
                abcNode.setName(entityName + '_' + abcType)
                abcNode.parm("fileName").set(latestPublishedFile['path']['local_path_linux'])
            
            except:
                print "same name"
            
            """ connect alembic to the subnet """
            subnetOutput = subnetEntityNode.indirectInputs()
            abcNode.setInput(0,subnetOutput[0])
            
            """ refresh the buildAlembicHierarchie """
            abcNode.parm('buildHierarchy').pressButton()
            
            
def create_alembicCamera(root,allPublishedCamera,width,height,ratio):
    allPublishedCamera.reverse()
        
    """ SUBNET SUBTYPE """
    """ check and create subType Subnet """
    rootPath = root.path()
    entitySubType = 'camera'
    subnetTypeNodePath = rootPath + '/' + entitySubType 
    
    subnetSubTypeNode = hou.node(subnetTypeNodePath)
    camera_subNet = hou.node(root.path()).createNode('subnet')
    camera_subNet.setName(entitySubType)
    
    subnetOutput = root.indirectInputs()
    camera_subNet.setInput(0,subnetOutput[0])
    camera_subNet.setColor(hou.Color((1,0.96,0.45)))
    
    """ CAMERA """
    """ create the camera alembic node """
    abcNode = hou.node(subnetTypeNodePath).createNode('alembicarchive')
    size = len(allPublishedCamera)
    
    abcNode.setName(allPublishedCamera[0]['name'])
    abcNode.parm("fileName").set(allPublishedCamera[0]['path']['local_path_linux'])
          
    """ connect alembic to the subnet """
    subnetOutput = camera_subNet.indirectInputs()
    abcNode.setInput(0,subnetOutput[0])
    
    """ refresh the buildAlembicHierarchie """
    abcNode.parm('buildHierarchy').pressButton()
         
    """ set viewport into the camera """
    allChildrenNode = abcNode.allSubChildren()
    cameraListNode = []
    
    for tmp in allChildrenNode:
        nodeType = tmp.type()
        
        if nodeType.name() == 'cam':
            cameraListNode.append(tmp)
    
    cameraNodePath = cameraListNode[0].path()
    cameraNode = hou.node(cameraNodePath)
    cameraNode.parm('resx').set(width)
    cameraNode.parm('resy').set(height)
    cameraNode.parm('aspect').set(ratio) 
    
    hou.ui.paneTabOfType(hou.paneTabType.SceneViewer).curViewport().setCamera(hou.node(cameraNodePath))
    
    
def init_setup_the_scene(fps,in_frame,out_frame):
    """ set the scene in Manual """
    hou.setUpdateMode(hou.updateMode.Manual)

    """ set the timeline """
    hou.setFps(fps)
    hou.hscript("tset `((%s-1)/$FPS)` `(%s/$FPS)`" % (in_frame, out_frame))
    hou.playbar.setPlaybackRange(in_frame, out_frame)
    hou.setFrame(in_frame)
        
def set_shot_timeLine(node):
    """ get frame in frame out from shotgun"""
    in_frame = float(node.parm('start_frame').evalAsString())
    out_frame = float(node.parm('end_frame').evalAsString())
    
    """ set the timeline """
    hou.hscript("tset `((%s-1)/$FPS)` `(%s/$FPS)`" % (in_frame, out_frame))    
    hou.playbar.setPlaybackRange(in_frame, out_frame)
    hou.setFrame(in_frame)
    
def set_dyn_timeLine(node):
    """ get frame in frame out from shotgun"""
    in_frame = float(node.parm('start_p_frame').evalAsString())
    out_frame = float(node.parm('end_p_frame').evalAsString())
    
    """ set the timeline """
    hou.hscript("tset `((%s-1)/$FPS)` `(%s/$FPS)`" % (in_frame, out_frame))
    hou.playbar.setPlaybackRange(in_frame, out_frame)
    hou.setFrame(in_frame)
    
def set_stock_timeLine(node):
    """ get frame in frame out from shotgun"""
    in_frame = float(node.parm('start_s_frame').evalAsString())
    out_frame = float(node.parm('end_s_frame').evalAsString())
    
    """ set the timeline """
    hou.hscript("tset `((%s-1)/$FPS)` `(%s/$FPS)`" % (in_frame, out_frame))
    hou.playbar.setPlaybackRange(in_frame, out_frame)
    hou.setFrame(in_frame)
    
def updateAnimationEnv(node):
    ctxSettings = Project_Settings()
    ctxSettingsList = ctxSettings.get_project_settings()
    engine = tank.platform.engine.current_engine()
    entity = engine.context.entity
    sg_entity_type = engine.context.entity["type"]
    sg_filters = [["id", "is", entity["id"]]]     

    fields = ['sg_inframe', 'sg_outframe']
    data = engine.shotgun.find_one(sg_entity_type, filters=sg_filters, fields=fields)
    
    # get frame in frame out
    if(sg_entity_type != 'Asset'):
        in_frame = int(data.get('sg_inframe'))
        out_frame = int(data.get('sg_outframe'))
    
    else:
        in_frame = 101
        out_frame = 300

    """ updates global animation env """
    startFrame = node.parm('start_frame').deleteAllKeyframes()
    end_frame = node.parm('end_frame').deleteAllKeyframes()
    start_p_frame = node.parm('start_p_frame').deleteAllKeyframes()
    end_p_frame = node.parm('end_p_frame').deleteAllKeyframes()
    start_s_frame = node.parm('start_s_frame').deleteAllKeyframes()
    end_s_frame = node.parm('end_s_frame').deleteAllKeyframes()   

    start_p_frame = node.parm('start_p_frame').eval()
    end_p_frame = node.parm('end_p_frame').eval()
    start_s_frame = node.parm('start_s_frame').eval()
    end_s_frame = node.parm('end_s_frame').eval()
    
    hou.hscript("set START_FRAME = " + str(in_frame))
    hou.hscript("set END_FRAME = " + str(out_frame))
    hou.hscript("set START_P_FRAME = " + str(start_p_frame))
    hou.hscript("set END_P_FRAME = " + str(end_p_frame))
    hou.hscript("set START_S_FRAME = " + str(start_s_frame))
    hou.hscript("set END_S_FRAME = " + str(end_s_frame))
    
    node.parm('start_frame').setExpression('$START_FRAME')
    node.parm('end_frame').setExpression('$END_FRAME')
    node.parm('start_p_frame').setExpression('$START_P_FRAME')
    node.parm('end_p_frame').setExpression('$END_P_FRAME')
    node.parm('start_s_frame').setExpression('$START_S_FRAME')
    node.parm('end_s_frame').setExpression('$END_S_FRAME')