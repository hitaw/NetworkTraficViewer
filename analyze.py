global trames

class Trame:

	i = 0

	def __init__(self, content):
		self.num = i
		i = i+1
		self.content = content

		self.ethernet : bool
		self.ipv4 : bool
		self.tcp : bool
		self.http : bool

		#ethernet
		self.dest_mac : str
		self.src_mac : str
		self.type : int

		#ip
		self.ip_v : int
		self.header_length : int
		self.ToS : int
		self.total_length : int
		self.identifier : int
		self.ip_flags : int
		self.fragment_offset : int
		self.time_to_live : int
		self.protocol : str
		self.header_checksum : int
		self.src_ip : str
		self.dest_ip : str

		#tcp
		self.src_port : int
		self.dest_port : int
		self.sequence_number : int
		self.ack : int
		self.thl : int
		self.reserved : int
		self.tcp_flags : int
		self.window : int
		self.checksum : int
		self.options_padding : int

		#http
		self.method : str
		self.request_answer : bool
		self.url : int
		self.statut : int
		self.version : int
		self.champs : dict
		self.data : str




def analyze_trames(content):
	global lines
	global trames

	trames = content.replace(" ","") #on retire les espaces
	trames = trames.splitlines() #on sépare les lignes
	t = trames
	new = []
	lines = 0
	while t != []:
		(res, t) = new_trame(t) #on crée toutes les trames, on vérifie leur validité
		new.append(res)
	for i in range(len(new)):
		analyze_trame(new[i])
	print(new)
	return "Analysé !"

def new_trame(t):
	global lines

	res = []
	if t[0][:4] == "0000": #on vérifie si le début de la nouvelle trame commence bien par l'offset "0000"
		res.append(t[0].lower()) #si oui, on ajoute la ligne à la nouvelle trame
		lines += 1
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
