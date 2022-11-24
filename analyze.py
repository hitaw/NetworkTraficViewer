global trames

"""class Trame:

	i = 0

	def __init__(self, content):
		self.num = i
		i = i+1
		self.content = content"""


def analyze_trames(content):
	global trames
	trames = content.replace(" ","") #on retire les espaces
	trames = trames.splitlines() #on sépare les lignes
	t = trames
	new = []
	while t != []:
		(res, t) = new_trame(t) #on crée toutes les trames, on vérifie leur validité
		new.append(res)
	for i in range(len(new)):
		analyze_trame(new[i]) 
	return t

def new_trame(t):
	res = []
	lines = 0
	if t[0][:4] == "0000": #on vérifie si le début de la nouvelle trame commence bien par l'offset "0000"
		res.append(t[0].lower()) #si oui, on ajoute la ligne à la nouvelle trame
		lines = 1
		t = t[1:] #on retire la première ligne pour gérer les autres
	else:
		return None
	suiv = True
	while suiv and t != []:
		if int(t[0][:4],16) == int(res[len(res)-1][:4],16)+16: #on ajoute les autres lignes SSI les offset se suivent
			res.append(t[0].lower()) 
			t = t[1:] #on retire la première ligne pour gérer les autres
		else:
			suiv = False
	res = verify_trame(res) #on vérifie que la trame créée est valide
	return (res,t)

def verify_trame(trame):
	for i in range(0,len(trame)):
		if i != len(trame)-1: #si ce n'est pas la dernière ligne de la trame, on vérifie que sa longueur est égale à 36 (4 pour l'offset et 32 pour le nombre d'octets)
			if len(trame[i]) != 36:
				return None
		else:
			if len(trame[i]) > 36: #si c'est la dernière ligne, on vérifie qu'elle est plus petite que 36
				return None
		for j in trame[i]:
			if (j < "0" or j > "9") and (j < "a" or j > "z"): #on vérifie que tous les caractères de la ligne soient des caractères hexadécimaux
				return None
	return trame

def analyze_trame(trame):
	#est-ce que je crée le fichier ici ou dans analyze_trames ?
	#dans analyze_trames ça nous ferait ouvrir le fichier qu'une seule fois mais ce serait peut-être moins pratique
	return
