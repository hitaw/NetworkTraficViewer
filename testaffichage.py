liste_ip = []
lite_mac = []
from interface import *

def change_cont(cont):
	r = ""
	for i in range(1000):
		r += "\n"
	cont.set(r)
"""def affichage(liste_de_trames):
	global canva

	back = None
	commentaire = ""
	First = True
	total = len(liste_de_trames)
	for trame in liste_de_trames:

		if trame.ethernet:

			if trame.ipv4:

				if trame.dest_ip not in liste_ip:
					liste_ip += trame.dest_ip
					canva.create_line(40,100,200, 0, fill = "grey", dash = 40) 
				if trame.src_ip not in liste_ip:
					liste_ip += trame.src_ip

				if trame.tcp:

					if trame.http:
						back = "lightgreen"
			
						i = 0
						while trame.content_http[i] != "\n":
							commentaire += trame.content_http[i]
							i += 1

					else:
						back = "lightblue"
						trame.analyze_flags_tcp()
						commentaire = 

				else:
					back = "lightpurple"

			else:
				back = "lightred"
				liste_mac += self.dest_mac
				liste_mac += self.src_mac"""



