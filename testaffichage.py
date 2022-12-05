from appli import *
liste_ip = []

def affichage(liste_de_trames):
	back = None
	commentaire = ""
	for trame in liste_de_trames:

		if trame.ethernet:

			if trame.ipv4:

				if trame.tcp:

					if trame.http:
						back = "lightgreen"
			
						i = 0
						while self.content_http[i] != "\n":
							commentaire += self.content_http[i]
							i += 1

					else:
						back = "lightblue"
				else:
					back = "lightpurple"
			else:
				back = "lightred"



