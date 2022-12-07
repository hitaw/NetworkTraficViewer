from interface import *

def print_analyzed_file():
	global canva
	global cont

	(trames_ethernet, trames_non_ethernet) = tri_trames(content)

	for i in len(trames_ethernet):
		trame = trames_ethernet[i]
		dico = recup_ip_address(trames_ethernet)
		source = trame.src_ip
		dest = trame.dest_ip

		commentaire = ""
		if trame.tcp :
			if trame.http:
				return
			else:

			ports += "port source : "
			ports += trame.src_port
			ports += " port destination : "
			ports += trame.dest_port
			canva.create_line(dico[source],i,dico[dest],i,arrow="last",tag=commentaire)
	return

def recup_address(liste_trames):
	res = {}
	j = 50

	for i in range(len(liste_trames)):

		trame = liste_trames[i]

		if not trame.ipv4:

			source = trame.src_mac
			dest = trame.dest_mac

		else :

			source = trame.src_ip
			dest = trame.dest_ip

		if source not in res:
			res.update({source:j})
			j += 200

		if dest not in res:
			res.update({dest:j})
			j += 200

		return res

def tri_trames(liste_trames):

	trames_ethernet = []
	trames_non_ethernet = []

	for trame in liste_trames:
		if trame.etherne:
			trames_ethernet.append(trame)
		else:
			trames_non_ethernet.append(trame)

	return (trames_ethernet, trames_non_ethernet)