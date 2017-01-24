import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import math
# get the active selection
#Selection du modèle



def computeNormal(n1,n2,n3):
	n = [0.0,0.0,0.0]
	for i in range(3):
		n[i] = n1[i] + n2[i] + n3[i]
	norme = math.sqrt(n[1] * n[1] + n[2] * n[2] + n[0] * n[0])
	for i in range(3):
		n[i] = n[i] / norme
	return n

def getDataFromCage():	
	selection = OpenMaya.MSelectionList()
	OpenMaya.MGlobal.getActiveSelectionList( selection )
	iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)
	trList=[]
	pointList = []
	normalList = []
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

		
		 #first points, then normals, then triangles
		#for each triangle to a list
		
		
		for i in range (inMeshMTriangleArray.length()/3):
			trList.append([inMeshMTriangleArray[3*i], inMeshMTriangleArray[3*i + 1], inMeshMTriangleArray[3*i + 2]])
		
		for i in range( inMeshMPointArray.length() ) :
			pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )

		for i in range (inMeshMNormalArray.length() ) :
			normalList.append( [inMeshMNormalArray[i][0], inMeshMNormalArray[i][1], inMeshMNormalArray[i][2]] )

			
		normalList.append( [inMeshMNormalArray[0], inMeshMNormalArray[1], inMeshMNormalArray[2]] )
		
		iterSel.next()
	ListeNormales = []
	No= OpenMaya.MIntArray()
	for i in range(len(trList)):
		currentInMeshMFnMesh.getFaceNormalIds(i, No)
		ListeNormales.append(computeNormal( normalList[No[0]], normalList[No[1]], normalList[No[2]] ))
	return trList, pointList, ListeNormales

def getVerticesFromModel():	
	selection = OpenMaya.MSelectionList()
	OpenMaya.MGlobal.getActiveSelectionList( selection )
	iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)
	trList=[]
	pointList = []
	normalList = []
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
	
		for i in range (inMeshMTriangleArray.length()/3):
			trList.append([inMeshMTriangleArray[3*i], inMeshMTriangleArray[3*i + 1], inMeshMTriangleArray[3*i + 2]])
		
		for i in range( inMeshMPointArray.length() ) :
			pointList.append( [inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]] )
		iterSel.next()


	#FUSIONNER LES VERTS AVANT#
	return pointList
"""
cmds.select( 'pCylinder1' )	
[V,T,N] = getDataFromCage()
"""
#cmds.select('polyMergeVert1')
L = getVerticesFromModel()
print len(L)
print L
