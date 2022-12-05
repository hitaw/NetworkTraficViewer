from appli import *


def affichage(liste_de_trames):
	background = None
	for trame in liste_de_trames:

		if trame.http:
			background = "lightgreen"

		elif trame.tcp:
			background = "lightblue"

		elif trame.ipv4:
			background = "lightpurple"
			
		elif trame.ethernet:
			background = "lightred"

