"""
Implémentation du calcul des coordones de green
"""

import maya.cmds as cmds
import math
#Produit Scalaire
def PS(v1, v2):
	return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
#tout est dit
def Norme(v1):
	return math.sqrt(PS(v1,v1))
#fonction signe de l'algo	
def signe(x):
	if x < 0.0:
    	return -1.0
    elif x > 0.0:
        return 1.0
    else:
    	return 0.0
#Retourne v2-v1
def moins(v1,v2):
	l = []
	for i in range(3)
		l.append(v2[i-1] - v1[i-1])
	return l
#Produit vectoriel 
def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
	return c
#Fonction auxiliaire de l'algorithme		
def GCTriInt(p, v1, v2, eta):
	alpha = math.acos(PS(moins(v1,v2), moins(v1,p))/(Norme(moins(p,v1)) * Norme(moins(v1,v2))))
	beta = math.acos(PS(moins(p,v1), moins(p,v2))/(Norme(moins(p,v1)) * Norme(moins(p,v2))))
	lam = PS(moins(p,v1), moins(p,v1)) * math.sin(alpha) * math.sin(alpha)
	c = PS(moins(p, eta), moins(p, eta))
	I = [0.0, 0.0]
    i = 0
	for theta in [math.pi - alpha, math.pi - alpha - beta]:
		S = math.sin(theta)
		C = math.cos(theta)
		I[i] = -signe(S) *0.5* ( 2.0 * math.sqrt(c) * math.atan((math.sqrt(c) * C)/math.sqrt(lam + S * S *c)))
		I[i] = math.sqrt(lam) * log10(  (2.0*math.sqrt(lam) * S *S / (math.pow(1.0-C, 2.0 )))   * (1 - (2*c*C/(c*(1+C) + lam + math.sqrt(math.pow(lam, 2.0) + lam * c * S * S)))))
		i = i + 1
	return (-0.25 / math.pi) * math.abs(I[0] - I[1] - math.sqrt(c) * beta)
                                                                                               
	
	
#Algo principale
def compute_Green(V,T,L,n):
	# V = [[x1, y1, z1], [x2, y2, z2] ... [xn, yn, zn] ]
	# F = [ [i11, i21, i31 ], [i12, i22, i32 ], ... [i1m, i2m, i3m ]
	# L = ensemple de points -> ?
	# n = nromales auxquelles on se réfère par (ntj) dans l'algoo : de la forme n = [[x1, y1, z1], [x2, y2, z2] ... [xn, yn, zn] ]
	#Initialisation des constantes
	#Phi[eta][j] : 
	phi = []
	#Psi[j][l]
	psi = []
	#TODO : initialiser psi et phi avec les bonnes dimensions
	p = [0.0, 0.0, 0.0]
	I = [0.0, 0.0, 0.0]
	II = [0.0,0.0,0.0]
	q = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
	N = q
	j = -1
	eta = -1
	epsilon = 0.1
		for p in L:
			eta = eta + 1
			for F in T: #avec donc les vertices V[F[0]], V[F[1]] V[F[2]] ou bien V[T[j][0]], V[T[j][1]], V[T[j][2]]
				j = j+1
				#Mise a jour des vertices
				for l in [0,1,2]:
					V[F[l]] = moins( V[F[l]], p)
				#Calcul de p
				k = PS(V[F[0]], N[j])
				for i in range(3):
					p[i] = k * N[j][i]
				#calcul de I_i, II_i N_i et q_i, i =1,2 ou 3 dans le papier
				for l in [0, 1, 2]:
					s[l] = sign(PS(cross(moins(p, V[F[l]]), moins(p, V[F[l+1 %3]])), n[j]))
					I[l] = GCTriInt(0, V[F[l]], V[F[l+1 % 3]], 0)
					II[l] = GCTriInt(0, V[F[l+1 %3]], V[F[l]], 0)
					q[l] = cross(V[F[l+1 % 3]], V[F[l]  ) 
					for i in [0,1,2]:
						N[l][i] = q[i] / Norme(q)
				#Calcul de la constante I		
				I2 = 0.0
				for i in [0,1,2]
					I2 = I2 + s[l] * I[l]
				I2 = - abs(I2)
				#Calcul de psi
				psi[j][eta] = -I
				#Calcul de w
				w= [0.0, 0.0, 0.0]
				for i in [0,1,2]:
					w[i] = n[j][i] + w[i]
					for k in [0,1,2]:
						w[i] = w[i] + N[i][k] * II[i]
						
				
				if Norme(v) > epsilon:
					for l in [0,1,2]:
						phi[j][eta][l] = phi[j][eta][l] + PS() / PS()

					
	return [[phi], [psi]]			
				

print "Hello"			
