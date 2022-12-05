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
		self.ip_flags : str
		self.fragment_offset : str
		self.time_to_live : int
		self.protocol : str
		self.header_checksum : str
		self.src_ip = ""
		self.dest_ip = ""
		self.options_padding_ip : str

		#tcp
		self.src_port : int
		self.dest_port : int
		self.sequence_number : int
		self.ack : int
		self.thl : int
		self.reserved : str
		self.tcp_flags : str
		self.window : int
		self.checksum : str
		self.urgentPointer : int
		self.options_padding_tcp : str

		#http
		self.content_http : str

		self.mess_is = ""
		self.mess_error = ""

	def __repr__(self):
		return self.content

	def analyze_trame(self):
		if self.is_ethernet():
			self.analyze_ethernet()
			print("Analyse Partie Ethernet : \n")
			print("Adresse mac de destination : " +self.dest_mac)
			print("Adresse mac source : " +self.src_mac)
			print("Type : " + str(self.type))
			print("\n\n")
			if self.is_ipv4():
				self.analyze_ipv4()
				print("Analyse Partie IPv4 : \n")
				print("Version : " + str(self.ip_v))
				print("Header Length : " + str(self.header_length))
				print("ToS : "+ str(self.ToS))
				print("Total length : " + str(self.total_length))
				print("Identifier : " + str(self.identifier))
				print("Ip_Flags : " +self.ip_flags)
				print("Fragment Offset : " + self.fragment_offset)
				print("TTL : " + str(self.time_to_live))
				print("Protocole : " + self.protocol)
				print("Header Checksum : " + self.header_checksum)
				print("Ip source : " + self.src_ip)
				print("Ip dest : " + self.dest_ip)
				print("Options + padding : " + self.options_padding_ip)
				print("\n\n")
				if self.is_tcp():
					self.analyze_tcp()
					print("Analyse Partie TCP : \n")
					print("Port Source : " + str(self.src_port))
					print("Port Dest : " + str(self.dest_port))
					print("Sequence Number : " + str(self.sequence_number))
					print("ACK : " + str(self.ack))
					print("Thl : " + str(self.thl))
					print("Reserved : " + self.reserved)
					print("TCP Flags : " + self.tcp_flags)
					print("Window : " + str(self.window))
					print("Checksum : " + str(self.checksum))
					print("Urgent Pointer : " + str(self.urgentPointer))
					print("Options + padding : " + self.options_padding_tcp)
					print("\n\n")					
					self.conversion_ascii()
					if self.is_http():
						print("HTTP : " + self.content_http)
						return
					else:
						self.content_http = None
				else:
					self.mess_is = "Ceci n'est pas une trame TCP\n" + self.mess_is
			else:
				self.mess_is = "Ceci n'est pas une trame IPv4\n" + self.mess_is
		else:
			self.mess_is = "Ceci n'est pas une trame Ethernet II\n" + self.mess_is


	def is_ethernet(self):
		if  len(self.non_etud) < 128:
			self.mess_error = "Trame trop courte (moins de 64 octets)"
			self.ethernet = False
		elif len(self.non_etud) > 3028:
			self.mess_error = "Trame trop longue (plus de 1512 octets)"
			self.ethernet = False
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
			elif self.type == "86dd":
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

			temp = bin(int(self.non_etud[12],16))[2:]
			temp_size = len(temp)
			while temp_size < 4:
				temp = "0" + temp
				temp_size += 1

			self.ip_flags = temp[:3]
			self.fragment_offset = temp[3] + self.non_etud[13:16]


			self.time_to_live = int(self.non_etud[16:18],16)
			self.protocol = self.non_etud[18:20]
			self.header_checksum = self.non_etud[20:24]

			src_ip = self.non_etud[24:32]
			dest_ip = self.non_etud[32:40]

			i = 0
			while i < 8:
				self.dest_ip += str(int(dest_ip[i:i+2],16))+"."
				self.src_ip += str(int(src_ip[i:i+2],16))+"."
				i += 2

			self.dest_ip = self.dest_ip[:-1]
			self.src_ip = self.src_ip[:-1]

			options_size = (self.header_length*4 - 20)*2
			i = 40 + options_size

			self.options_padding_ip = self.non_etud[40:i]

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

	def analyze_tcp(self):
		self.src_port = int(self.non_etud[:4],16)
		self.dest_port = int(self.non_etud[4:8],16)
		self.sequence_number = int(self.non_etud[8:16],16)
		self.ack = int(self.non_etud[16:24],16)
		self.thl = int(self.non_etud[24:25],16)*4

		temp = bin(int(self.non_etud[25:28],16))[2:]
		temp_size = len(temp)
		while temp_size < 14:
			temp = "0" + temp
			temp_size += 1

		self.reserved = temp[:6]
		self.tcp_flags = temp[6:]

		self.window = int(self.non_etud[28:32],16)
		self.checksum = self.non_etud[32:36]
		self.urgentPointer = int(self.non_etud[36:40],16)

		options_size = (self.thl - 20)*2
		i = 40 + options_size

		self.options_padding_tcp = self.non_etud[40:i]

		self.non_etud = self.non_etud[i:]

	def conversion_ascii(self):
		self.http = False		
		i = 0
		self.content_http = ""
		while i < len(self.non_etud) - 3:
			self.content_http += chr(int(self.non_etud[i:i+2],16))
			i += 2

	def is_http(self):
		self.is_http = False
		if "HTTP" in self.content_http:
			self.is_http = True
		return self.is_http


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
	new[0].analyze_trame()
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
