#coding=utf-8
from analyze import Trame

def recup_address(liste_trames):
	res = {}
	j = 200

	for trame in liste_trames:

		if not trame.ipv4:

			source = trame.src_mac
			dest = trame.dest_mac

		else :

			source = trame.src_ip
			dest = trame.dest_ip

		if source not in res:
			res.update({source:j})
			j += 500

		if dest not in res:
			res.update({dest:j})
			j += 500

	return res,j

def tri_trames(liste_trames):

	trames_ethernet = []
	trames_non_ethernet = []

	for trame in liste_trames:
		if trame.ethernet:
			trames_ethernet.append(trame)
		else:
			trames_non_ethernet.append(trame)

	return (trames_ethernet, trames_non_ethernet)