import maya.OpenMaya as OpenMaya

def particleFillSelection(  ):

	# get the active selection
	selection = OpenMaya.MSelectionList()
	OpenMaya.MGlobal.getActiveSelectionList( selection )
	iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)
 
	# go througt selection
	while not iterSel.isDone():
 
		print "inside while"
		# get dagPath
		dagPath = OpenMaya.MDagPath()
		iterSel.getDagPath( dagPath )
		
		# create empty point array
		inMeshMPointArray = OpenMaya.MPointArray()
		inMeshMNormalArray = OpenMaya.MFloatVectorArray()
		inMeshMTriangleArray = OpenMaya.MIntArray()
		inMeshMTriangleCount = OpenMaya.MIntArray()
        
		# create function set and get points in world space
		currentInMeshMFnMesh = OpenMaya.MFnMesh(dagPath)
		currentInMeshMFnMesh.getPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)
		currentInMeshMFnMesh.getNormals(inMeshMNormalArray, OpenMaya.MSpace.kWorld)
		currentInMeshMFnMesh.getTriangles(inMeshMTriangleCount, inMeshMTriangleArray)
		
		totalList = [] #first points, then normals, then triangles
		pointList = []
		
		for i in range( inMeshMPointArray.length() ) :
			pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )
		

		totalList.append(pointList)
		print "nb points"
		print pointList
		
		normalList = []
		nbNormals = 0
		
		for j in range (inMeshMNormalArray.length() ) :
		  normalList.append( [inMeshMNormalArray[j][0], inMeshMNormalArray[j][1], inMeshMNormalArray[j][2]] )
		  nbNormals = nbNormals + 1    
       
		totalList.append(normalList)
		print "Normals"
		print nbNormals
		print normalList
		triangleCountList = []
		triangleList = []
		for k in range (inMeshMTriangleCount.length() ) :
		    triangleList.append([inMeshMTriangleArray[k*3], inMeshMTriangleArray[k*3+1], inMeshMTriangleArray[k*3 +2]])
        
		print "Nb triangles count "
		print inMeshMTriangleCount.length()
		print "Nb points array"
		print inMeshMTriangleArray.length()
		print triangleList
		
		for T in range (inMeshMTriangleCount.length()):
		    index = triangleList[T][0] 
		    print pointList[index]
		iterSel.next() 
		totalList.append(inMeshMTriangleCount.length())
		totalList.append(triangleList)
	return totalList 

print "success"
particleFillSelection()