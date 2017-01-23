import maya.OpenMaya as OpenMaya

# get the active selection
selection = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getActiveSelectionList( selection )
iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)

# go througt selection
while not iterSel.isDone():

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
	#for each triangle to a list
	trList = []
	nTr = 0
	for i in range (inMeshMTriangleArray.length()/3):
		trList.append([inMeshMTriangleArray[3*i], inMeshMTriangleArray[3*i + 1], inMeshMTriangleArray[3*i + 2]])
		nTr = nTr + 1
	
 
	# put each point to a list
	pointList = []
	nbPoints = 0
	for i in range( inMeshMPointArray.length() ) :

		pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )
		
	totalList.append(pointList)
	
	
		
	normalList = []
	nbNormals = 0 
	
	for i in range (inMeshMNormalArray.length() ) :
		normalList.append( [inMeshMNormalArray[i][0], inMeshMNormalArray[i][1], inMeshMNormalArray[i][2]] )
		nbNormals = nbNormals + 1
		
	totalList.append(normalList)
	iterSel.next() 
	
print inMeshMNormalArray.length(), inMeshMPointArray.length(), inMeshMTriangleArray.length()/3
print trList
print pointList
print normalList



