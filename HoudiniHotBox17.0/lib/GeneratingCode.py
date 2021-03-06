import hou
import os
#return ../copy2
def getRefencePath(pathStr):
    pathArr = pathStr.split('"')
    for i in pathArr:
        if i[0:3] =="../":
            if i[-1] == "/":
                i = i[0:-1] 
            return i
#return   ['..', <hou.SopNode of type copy at /obj/geo1/copy3>]          
def getNewRefencePath(currentNode,oldPath):
    classIndex = len(oldPath.split("/"))
    classString = oldPath.split("/")
    nameOfOldNode = oldPath.split("/")[-1]
    newNode = ""
    nodeArr = []
    for i in range(classIndex):
        if i < (classIndex-1):
            if classString[i] == "..":
            
                newNode =currentNode.parent()
                nodeArr.append("..")
            else:
                currentNodeName = classString[i]
                
                for node in newNode.children():
                    if node.name() == currentNodeName:
                        newNode = node
                        nodeArr.append(newNode)
        #last node
        else:
            currentNodeName = classString[i]
                
            for node in newNode.children():
                if node.name() == currentNodeName:
                    newNode = node
                    nodeArr.append(newNode)
                    return nodeArr    

                    
def  getNewRefencePathString(f,NodesourceArr):
    exportExpress =""
    for istr in NodesourceArr:
        if istr =="..":
            exportExpress+=istr
            exportExpress+="/"
        else:
            NodecoadName = "SopNode"+istr.name()
            exportExpress+=NodecoadName
            exportExpress+="/"
    return  exportExpress       
#set Init Name     
def setInitNodeName(node):
    oldName = node.name()
    index = str(len(node.path().split("/")))
    newName = node.parent().type().name()+index+"__"+oldName
    node.setName(newName,1)
    if node.isLockedHDA()==0 and node.children():
        for a in node.children():
            setInitNodeName(a)
#clear Init Name 
def setclearNodeName(node):
    oldName = node.name()
    newName = oldName.split("__")[-1]
    node.setName(newName,1)
    if node.isLockedHDA()==0 and node.children():
        for a in node.children():
            setclearNodeName(a)
# return [1]      
def getAsConnctInfo(node ):
    c="0"
    try:
        a=  node.asCode()
        b= a.split("\n")
        for i in b :
            if i.split("indirectInputs")[-1][0:3] == "()[":
                c =i.split(")")[-2]
    
        return c
    except:
        
        return c
# write python file to set  Node  DisFlig in foreach class or subnet class      
def getNodeDisFlig(f,node ):
    display =node.isDisplayFlagSet()
    if display ==1:
    
        f.write("SopNode"+node.name()+".setDisplayFlag("+str(display) + ")"+"\n")
    
def MainsetInputConect(f,vopNode):
    #subnet foreach
    if  vopNode.parent().type().name() == "foreach"  and getAsConnctInfo(vopNode)[0] == "[":
        vopNodeName ="SopNode"+vopNode.name()
        vopTypeName = vopNode.type().name()
        for con in list(vopNode.inputConnections()):
            inpuIndex =   con.inputIndex()
            inputNode =  con.inputNode()
            outputIndex = con.outputIndex()
            f.write( vopNodeName+".setInput("+str(inpuIndex)+","+"SopNode"+vopNode.parent().name()+".indirectInputs()"+getAsConnctInfo(vopNode)+")\n")    
    
    #subnet connect
    elif vopNode.parent().type().name() == "subnet"  and getAsConnctInfo(vopNode)[0] == "[":
        vopNodeName ="SopNode"+vopNode.name()
        vopTypeName = vopNode.type().name()
        for con in list(vopNode.inputConnections()):
            inpuIndex =   con.inputIndex()
            inputNode =  con.inputNode()
            outputIndex = con.outputIndex()
            f.write( vopNodeName+".setInput("+str(inpuIndex)+","+"SopNode"+vopNode.parent().name()+".indirectInputs()"+getAsConnctInfo(vopNode)+")\n")            
                 
    else :
        vopNodeName ="SopNode"+vopNode.name()
        vopTypeName = vopNode.type().name()
        for con in list(vopNode.inputConnections()):
            inpuIndex =   con.inputIndex()
            inputNode =  con.inputNode()
            outputIndex = con.outputIndex()
            f.write( vopNodeName+".setInput("+str(inpuIndex)+","+"SopNode"+inputNode.name()+","+str(outputIndex)+")\n")        

def MainsetParm(f,vopNode):
    vopNodeName ="SopNode"+vopNode.name()
    vopTypeName = vopNode.type().name()

    for vopParm in list(vopNode.parms()):
        if vopParm.isAtDefault() ==1:
            pass
        else:
            
            try:
                vopParmValueExpress = vopParm.expression()
                vopParmValueType  = "hou.exprLanguage.Hscript"
                if vopParm.expressionLanguage().name() == "Python":
                    vopParmValueType ="hou.exprLanguage.Python"
                vopParmName = vopParm.name()
                f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".setExpression("+"'" +vopParmValueExpress+"'"+","+vopParmValueType+")\n")
            except:    
                vopParmValue = vopParm.eval() 
                vopParmName =  vopParm.name()
                if isinstance(vopParmValue, str):
                    f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".set("+"'" +str(vopParmValue)+"'"+")\n")
                else:
                    f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".set("+str(vopParmValue)+")\n")

def secondSetParm(f,vopNode):
    vopNodeName ="SopNode"+vopNode.name()
    vopTypeName = vopNode.type().name()
    for vopParm in list(vopNode.parms()):
        vopParmValue = vopParm.eval() 
        vopParmName =  vopParm.name()
        if vopParm.isAtDefault() ==1:
            pass
        else:
            if  vopParm.evalAsString()[0:3] =="../"  and vopParm.evalAsString()[3:6] != "../":
                
                getNodeTextName = "SopNode"+  vopParm.evalAsString().split("../")[-1]
                
                f.write( "SencondParm = "+"'../'"+"+"+getNodeTextName +".name()"+"\n")
                f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".set("+"SencondParm"+")\n")
            
def getNwePathformsecondParm2(vopParmValueExpress,zhuhe):
    
    oldExp =vopParmValueExpress
    
    newExp =""
    oldExpArr = oldExp.split('"')
    
    
    
    
    tempSplit =""
    
    for i in oldExpArr:
        if i[0:3] =="../":
            tempSplit = i
    oldExpArr = oldExp.split(tempSplit) 
    newExp    = oldExpArr[0][0:-1] +"'+"+"'\"'"+"+"   +zhuhe+  "+"+"'\"'"+"+'"+    oldExpArr[1][1:]  
            
        
    print newExp
    return newExp
###############################################  "../"+"../"+SopNodegeo4__subnet1.name()+"/"+SopNodesubnet5__null1.name()
def getClipPathName( strSource):
    a = strSource.split("/")
    b= ""
    b+='"'
    for i in a:
        if i == "..":
            b+='"'
            b+=i
            b+="/"
            b+='"+'
        else:
            b+=("SopNode"+i+".name()")
            
            b+='+"/"+'
    b+='"'
    return b[1:-6] 
    
    
    
                
def secondSetParm2(f,vopNode):
    vopNodeName ="SopNode"+vopNode.name()
    vopTypeName = vopNode.type().name()
    for vopParm in list(vopNode.parms()):
        vopParmValue = vopParm.eval() 
        vopParmName =  vopParm.name()
        if vopParm.isAtDefault() ==1:
            pass
        else:
            
            try:
                if  getRefencePath(vopParm.expression())[0:3] =="../":
                   
                    oldPath = getRefencePath(vopParm.expression())
                    classIndex = len(oldPath.split("/"))
                    nameOfOldNode = oldPath.split("/")
                    ### newPath =??
                   
                         
                    
                    ##../SopNodegeo4__subnet1/SopNodesubnet5__null1/
                    
                    #zhuhe = getNewRefencePathString(f,currentNode)#[0:-1].split("/")
                    
                    newPath = getClipPathName(oldPath)
                    print newPath
                    
                    
                    
                    
                    vopParmValueExpress = vopParm.expression()
                    vopParmValueType  = "hou.exprLanguage.Hscript"
                    if vopParm.expressionLanguage().name() == "Python":
                        vopParmValueType ="hou.exprLanguage.Python"
                    
                    
                    
                    finalExp = getNwePathformsecondParm2(vopParmValueExpress,newPath)
                    
                     ###+"newVopParmValueExpress"+"'"+","+"newVopParmValueType"+       
                    f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".setExpression("+"'" +finalExp+"'"+")\n")
                            
            except:
                pass
            

def AsCoadMainOfNode(f,nodes,_mainFatherGeoNodeName,_InstallNodeName):
   
    
    
#    for child in nodes:
#        setInitNodeName(child)
        
    
    checkParentCreat =0
    secondParent =0
    InstallNodeName = ""
    mainFatherGeoNodeName = _mainFatherGeoNodeName
    InstallNodeName = _InstallNodeName
    
    for child in nodes:
        
        sopTypeName = child.type().name()
        sopName = "SopNode"+ child.name()
        
        if child.type().name() == "attribvop":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'attribvop1'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n") 
        elif child.type().name() == "volumevop":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'volumevop1'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n") 
            
        elif child.type().name() == "popvop":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'popvop'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n")    
            
            
        elif child.type().name() == "geometryvop":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'geometryvop'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n")    
            
            
        elif child.type().name() == "gasfieldvop":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'gasfieldvop'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n")
        
        elif child.type().name() == "foreach":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'foreach'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n")
        elif child.type().name() == "subnet":
            
            f.write("##Strat creat " +sopName+"\n")
            
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+",'subnet'"+" , run_init_scripts=False, load_contents=True, exact_type_name=True"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n")        
            
            
        else:
            
            
            f.write("##Strat creat " +sopName+"\n")
            f.write( sopName+"="+mainFatherGeoNodeName+".createNode("+"'"+sopTypeName+"'"+")\n")
            
            
            f.write("##End creat " +sopName+"\n\n")

    
        
            
    for child in nodes:
               
        if child.type().name() == "attribvop" or child.type().name() == "volumevop"  or child.type().name() == "popvop"  or child.type().name() == "geometryvop" or child.type().name() == "gasfieldvop":
                childNodes= child.children()
                vopFatherConnectName = "fatherConectNode_"+ child.name()
                for vopNode in childNodes:
                    vopNodeName ="vopNode"+vopNode.name()
                    vopTypeName = vopNode.type().name()
                    f.write( vopNodeName+"="+ "SopNode"+ child.name()+".createNode("+"'"+vopTypeName+"'"+")\n")
                    
                for vopNode in childNodes:
                    vopNodeName ="vopNode"+vopNode.name()
                    vopTypeName = vopNode.type().name()    
                    for vopParm in list(vopNode.parms()):
                        if vopParm.isAtDefault() ==1:
                            pass
                        else:
                            vopParmValue = vopParm.eval() 
                            vopParmName =  vopParm.name()
                            if isinstance(vopParmValue, str):
                                f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".set("+"'" +str(vopParmValue)+"'"+")\n")
                            else:
                                f.write( vopNodeName+".parm("+"'"+ vopParmName+"'"+")"+".set("+str(vopParmValue)+")\n")
                
                
                for vopNode in childNodes:
                    vopNodeName ="vopNode"+vopNode.name()
                    vopTypeName = vopNode.type().name()
                    for con in list(vopNode.inputConnections()):
                        inpuIndex =   con.inputIndex()
                        inputNode =  con.inputNode()
                        outputIndex = con.outputIndex()
     
                        f.write( vopNodeName+".setInput("+str(inpuIndex)+","+"vopNode"+inputNode.name()+","+str(outputIndex)+")\n")   

    for child in nodes:        
        
        f.write("##Strat connect " +sopName+"\n")    
        MainsetInputConect(f,child) 
        MainsetParm(f,child)
        f.write("##End connect " +sopName+"\n\n") 
        
    for child in nodes:  
        secondSetParm(f,child)
        getNodeDisFlig(f,child)
        
        
    
        
    ## difui foreack dop pop sub sover
    for child in nodes:
        if child.type().name() == "foreach" or child.type().name() == "subnet":
            foreachNodes = list(child.children())
            foreachFatherGeoNodeName = "SopNode"+child.name()
            foreachInstallNodeName = "SopNode"+ foreachNodes[0].name()
                    
            AsCoadMainOfNode(f,foreachNodes,foreachFatherGeoNodeName,foreachInstallNodeName)
            
            
                
            
    __InstallNodeName   =  "SopNode"+ nodes[0].name()
    return __InstallNodeName                    

## secondSetPatm
def AsCoadMainOfNode2(f,nodes,_mainFatherGeoNodeName,_InstallNodeName):    
    
    ###second setPatm2
    for child in nodes:
        sopTypeName = child.type().name()
        sopName = "SopNode"+ child.name()
        
          
        a = secondSetParm2(f,child)
        #print getNewRefencePathString(f,a)
       
        
        
       
    
    for child in nodes:
        if child.type().name() == "foreach" or child.type().name() == "subnet":
            foreachNodes = list(child.children())
            foreachFatherGeoNodeName = "SopNode"+child.name()
            foreachInstallNodeName = "SopNode"+ foreachNodes[0].name()
                    
            AsCoadMainOfNode2(f,foreachNodes,foreachFatherGeoNodeName,foreachInstallNodeName)
        

class GeneratingCode:
    def run(self):
        nodes = list(hou.selectedNodes())
        for i in nodes:
            setInitNodeName(i)
            
        
        serachName = hou.ui.readInput('Innput Python Script name',buttons=['Ok','Cancle'])[1]
        ascoadName =serachName
        ascoadPath =os.getenv('SMILEHOTBOX')+"\\lib" +"\\"+ ascoadName+".py"
        f=open(ascoadPath,"w")
        
        f.write("s_plane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)\n")
        f.write("s_pos = s_plane.selectPosition()\n")
        
        f.write("s_parent_node =s_plane.pwd() \n")
        mainFatherGeoNodeName = "s_parent_node"
        InstallNodeName = "SopNode"+ nodes[0].name()
        
        ##### setFirstParm
        InstallNodeName = AsCoadMainOfNode(f,nodes,mainFatherGeoNodeName,InstallNodeName)
        
        ##### setSecondParm
        AsCoadMainOfNode2(f,nodes,mainFatherGeoNodeName,InstallNodeName)
        ####setPose
        
        for i in nodes:
            f.write("s_pos[1]-=1\n")
             
            f.write("SopNode"+i.name()+".setPosition(s_pos)"+"\n")
        
        
        
        f.close()
        f=open(ascoadPath,"r")
        sourcePy=f.readlines()
        f.close()
        f=open(ascoadPath,"w")
        f.write("import hou \n")
        f.write("class "+ascoadName+" :" +" \n")
        f.write("    def run(self):  \n")
        f.write("        InstallSelectNode = list( hou.selectedNodes())[0]  \n")
        
        for line in list( sourcePy):
            lineNew = "        "+line
            f.write(lineNew)
             
        f.write("        try:  \n")
        f.write("            "+InstallNodeName+".setInput(0,InstallSelectNode, 0)"+"  \n")
        f.write("        except:  \n")
        f.write("            pass  \n")
        f.close()
        #clear Name
        for i in nodes:
            
            setclearNodeName(i)
            
