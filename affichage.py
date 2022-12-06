from interface import *

def recup_ip_address(content):
	res = {}
	j = 1
	for i in len(content):
		trame = content[i]
		if trame.ethernet:

			if not trame.ipv4:

				source = trame.src_mac
				dest = trame.dest_mac

			else :

				source = trame.src_ip
				dest = trame.dest_ip

			if source not in res:

				res.update({source:j})
				j += 1

			if dest not in res:
				
				res.update({dest:j})
				j +=1
		return res