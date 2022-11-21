global trames

def analyze_trames(content):
	global trames
	trames = content.replace(" ","")
	trames = trames.splitlines()
	t = trames
	new = new_trame(t)
	print(new)
	"""while t != []:
					new = new_trame(t)"""
	return "Anaysé !"

def new_trame(t):
	res = []
	new = True
	lines = 0
	if t[0][:4] == "0000":
		res.append(t[0])
		lines = 1
		t = t[1:]
	else:
		raise Exception("Trame invalide")
		return None
	suiv = True
	while suiv and t != []:
		if int(t[0][:4],16) == int(res[len(res)-1][:4],16)+16:
			res.append(t[0])
			t = t[1:]
		else:
			suiv = False
	return res

def analyze_trame(trame):
	return
