import maya.cmds as cmds
import math

def PS(v1, v2):
	return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def Norme(v1):
	return math.sqrt(PS(v1,v1))
	
def GCTriInt(p, v1, v2, eta):
	alpha = math.acos(PS(moins(v1,v2), moins(v1,p))/(Norme(moins(p,v1)) * Norme(moins(v1,v2))))
	beta = math.acos(PS(moins(p,v1), moins(p,v2))/(Norme(moins(p,v1)) * Norme(moins(p,v2))))
	lam = PS(moins(p,v1), moins(p,v1)) * math.sin(alpha) * math.sin(alpha)
	c = PS(moins(p, eta), moins(p, eta))
	
	for theta in [math.pi - alpha, math.pi - alpha - beta]:
		S = math.sin(theta)
		C = math.cos(theta)
		I
	
	
	
def moins(v1,v2):
	l = []
	for i in range(3)
		l.append(v2[l-1] - v1[l-1])
	return l

def compute_weights(V,T,L):
phi = []
psi = []
	for p in L:
		for j in T:
			for i in range(3):
				