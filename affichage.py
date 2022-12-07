from interface import *
liste_label = []

def affichage_analyzed(content, canva, cont, frame):
	global liste_label

	(trames_ethernet, trames_non_ethernet) = tri_trames(content)

	dico,j = recup_address(trames_ethernet)
	for address in dico:
		l = Label(frame, text = address, font = "Arial", justify = "center", bg = "lightgrey")
		liste_label.append(l)
		l.place(dico[address], 10)
		canva.create_line(dico[address],20,dico[address], 1000, fill = "grey", dash = (5,1))

	f = " "*j
	for i in range(len(trames_ethernet)):
		trame = trames_ethernet[i]

		if trame.ipv4:
			source = trame.src_ip
			dest = trame.dest_ip

			if trame.tcp :
				if not trame.http:
					trame.mess_is = str(trame.src_port) + " -> " + str(trame.dest_port) + " " + trame.flags + " Seq = " + str(trame.relative_sequence_number) + " ACK = " + str(trame.relative_ack_number)			

		canva.create_line(dico[source],50 + i*40,dico[dest],50 + i*40,arrow="last",tag=trame.mess_is)
		#f += "\n"*40
	erreurs = "Les Trames "
	for t in trames_non_ethernet:
		erreurs += str(trames_non_ethernet[t]) + ", "
	erreurs = erreurs[:-2]
	erreurs += " ne sont pas des trames Ethernet ou ne sont pas exploitables."

	#f += "\n"
	cont.set(f)
	return erreurs


def recup_address(liste_trames):
	res = {}
	j = 50

	for trame in liste_trames:

		if not trame.ipv4:

			source = trame.src_mac
			dest = trame.dest_mac

		else :

			source = trame.src_ip
			dest = trame.dest_ip

		if source not in res:
			res.update({source:j})
			j += 300

		if dest not in res:
			res.update({dest:j})
			j += 300

	return res,j

def tri_trames(liste_trames):

	trames_ethernet = []
	trames_non_ethernet = {}

	for trame in liste_trames:
		if trame.ethernet:
			trames_ethernet.append(trame)
		else:
			trames_non_ethernet.update({trame:liste_trames.index(trame)})

	return (trames_ethernet, trames_non_ethernet)