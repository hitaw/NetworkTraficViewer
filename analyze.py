global trames

class Trame:

	def __init__(self, content):
		self.content = content

		self.ethernet : bool
		self.ipv4 : bool
		self.tcp : bool
		self.http : bool

		self.non_etud = content

		#ethernet
		self.dest_mac = ""
		self.src_mac = ""
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

		self.mess_not = ""
		self.mess_is = ""
		self.mess_error = ""

	def __repr__(self):
		return self.content

	def analyze_trame(self):
		if self.is_ethernet():
			self.analyze_ethernet()
			if self.is_ipv4():
				if self.is_tcp():
					if self.is_http():
						return
				else:
					self.mess_not = "Ceci n'est pas une trame TCP\n"
			else:
				self.mess_not = "Ceci n'est pas une trame IPv4\n"
		else:
			self.mess_not = "Ceci n'est pas une trame Ethernet II\n" + self.mess_not


	def is_ethernet(self):
		if  len(self.non_etud) < 128:
			self.mess_not = "Trame trop courte (moins de 64 octets)"
		elif len(self.non_etud) > 3028:
			self.mess_not = "Trame trop longue (plus de 1512 octets)"
		elif int(self.non_etud[24:28],16) > 1500:
			self.ethernet = True
		else:
			self.ethernet = False
		return self.ethernet

	def analyze_ethernet(self):
		dest_mac = self.non_etud[:12]
		src_mac = self.non_etud[12:24]
		self.type = self.non_etud[24:28]
		i = 0
		while i < 12:
			self.dest_mac += dest_mac[i:i+2]+":"
			self.src_mac += src_mac[i:i+2]+":"
			i += 2
			
		self.dest_mac = self.dest_mac[:-1]
		self.src_mac = self.src_mac[:-1]
		self.non_etud = self.non_etud[28:]

	def is_ipv4(self):
		if self.type == "0800" :
			self.ipv4 = True
		else:
			self.ipv4 = False
			if self.type == "0806":
				self.mess_is = "Trame ARP"
			elif self.type == "0x86dd":
				self.mess_is = "Trame IPv6"
			else:
				self.mess_is = "Type inconnu"

		return self.ipv4

	def analyze_ipv4(self):
		self.ip_v = int(self.non_etud[0],16)

		if self.ip_v == 4:
			self.header_length = int(self.non_etud[1],16)
			self.ToS =  int(self.non_etud[2:4],16)
			self.total_length = int(self.non_etud[4:8],16)
			self.identifier = int(self.non_etud[8:12],16)

			temp = bin(int(self.non_etud[13],16))
			self.ip_flags = temp[2:5]
			self.fragment_offset = temp[6] + self.non_etud[14:17]

			self.time_to_live = int(self.non_etud[17:19],16)
			self.protocol = self.non_etud[19:21]
			self.header_checksum = self.non_etud[21:25]

			src_ip = self.non_etud[25:33]
			dest_ip = self.non_etud[33:41]

			i = 0
			while i < 8:
				self.dest_ip += str(int(dest_ip[i:i+2],16))+"."
				self.src_ip += str(int(src_ip[i:i+2],16))+"."
				i += 2

			self.dest_ip = self.dest_ip[:-1]
			self.src_ip = self.src_ip[:-1]

			options_size = self.header_length*4 - 20
			i = 41 + options_size

			self.non_etud = self.non_etud[i:]

		else:
			self.mess_error = 'Mauvaise valeur : ip_version != 4'

	def is_tcp(self):
		if self.protocol == "06":
			self.tcp = True
		else:
			self.tcp = False

			if self.protocol == "01":
				self.mess_is = "Protocole ICMP"
			
			elif self.protocol == "02":
				self.mess_is = "Protocole IGMP"

			elif self.protocol == "11":
				self.mess_is = "Protocole UDP"
		
		return self.tcp

	def is_http(self):
		#jsp comment on reconnaît une trame http mdrr
		return True


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
		new[i].analyze_trame()
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

	for i in range(len(res)):
		res[i] = res[i][4:]
	res = verify_trame(res) #on vérifie que la trame créée est valide
	res = "".join(res)
	res = Trame(res)
	return (res,t)

def verify_trame(trame):
	for i in range(0,len(trame)):
		if i != len(trame)-1: #si ce n'est pas la dernière ligne de la trame, on vérifie que sa longueur est égale à 32
			if len(trame[i]) != 32:
				return None
		else:
			if len(trame[i]) > 32: #si c'est la dernière ligne, on vérifie qu'elle est plus petite que 32
				return None
		for j in trame[i]:
			if (j < "0" or j > "9") and (j < "a" or j > "z"): #on vérifie que tous les caractères de la ligne soient des caractères hexadécimaux
				return None
	return trame
