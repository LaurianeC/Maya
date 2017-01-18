import maya.cmds as cmds
#ouverture du fichier
filepath2 = "C:/Users/ensimag/Documents/maya/scripts/olaf.off"
file = open(filepath2, 'r')
#Chargement du fichier
line = file.readline()
line = file.readline()
data = line.split()
nvert = int(data[0])
nface = int(data[1])
verts = []
print "vertices"
for i in range(nvert):
    line = file.readline()
    data = line.split()
    verts.append([float(data[0]), float(data[1]), float(data[2])])

faces = []
print "faces"
for i in range(nface):
    line = file.readline()
    data = line.split()
    faces.append([int(data[1]), int(data[2]), int(data[3])])
#Création de la mesh

print "mesh generation"
j = 0
for F in faces:
    j = j+1
    if j%100 == 0:
        print "cent facettes affichées"
    p1 = F[0]
    p2 = F[1]
    p3 = F[2]
    cmds.polyCreateFacet( p=[(verts[p1][0], verts[p1][1], verts[p1][2]), (verts[p2][0], verts[p2][1], verts[p2][2]), (verts[p3][0], verts[p3][1], verts[p3][2])] )