from tkinter import *
from tkinter.filedialog import *
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
from analyze import *
from tri import *

content = None
en_cours = None
cont = None
label = None
canva = None
analyzed = False
lines = 0
column = 0
num = 1

class Interface(Tk):

	def __init__(self):
		global cont
		global canva
		global label

		Tk.__init__(self)

		canva = Canvas(self)

		self.create_menu_bar()
		self.geometry("1920x1080")
		self.title("Fireshark")
		self.create_canva()
		logo = PhotoImage(file = "logo.png")
		self.iconphoto(False, logo)

	def create_menu_bar(self):
		menu_bar = Menu(self)

		menu_file = Menu(menu_bar, tearoff = 0)
		menu_file.add_command(label = "Open", command = self.open_file, accelerator = "CTRL+O")
		menu_file.add_command(label = "Analyze", command = self.analyze_file, accelerator = "CTRL+A")
		menu_file.add_command(label = "Save as...", command = self.save_file, accelerator = "CTRL+S")
		menu_file.add_command(label ="Close", command = self.close_file, accelerator = "CTRL+F")
		menu_file.add_separator()
		menu_file.add_command(label = "Quit", command=self.quit, accelerator = "CTRL+C")
		menu_file.add_command(label = "Help", command=self.help, accelerator = "CTRL+H")
		menu_file.add_separator()
		menu_file.add_command(label = "About...", command=self.about)
		menu_bar.add_cascade(label="Menu", font = ("Arial",15), menu=menu_file)

		self.bind_all("<Control-o>", lambda x: self.open_file())
		self.bind_all("<Control-a>", lambda x: self.analyze_file())
		self.bind_all("<Control-s>", lambda x: self.save_file())
		self.bind_all("<Control-f>", lambda x: self.close_file())
		self.bind_all("<Control-h>", lambda x: self.help())
		self.bind_all("<Control-c>", lambda x: self.quit())

		menu_filter = Menu(menu_bar, tearoff = 0)
		menu_filter.add_command(label = "Info Trame", command = self.info_trame)
		menu_filter.add_separator()
		menu_filter.add_command(label = "Adresses IP", command = self.filtre_ip)
		menu_filter.add_command(label = "Ports", command = self.filtre_port)
		menu_filter.add_command(label = "TCP", command = self.filtre_tcp)
		menu_filter.add_command(label = "HTTP", command = self.filtre_http)
		menu_filter.add_separator()
		menu_filter.add_command(label = "Enlever les filtres", command = self.remove_filter)
		menu_bar.add_cascade(label="Filtre", font = ("Arial",15), menu=menu_filter)

		self.config(menu=menu_bar)

	def create_canva(self):
		global label
		global canva

		canva = Canvas(self, width=1980, height=1080, bg='lightgrey')
		canva.grid(row = 0, column = 0)
		label = canva.create_text(952.5, 480, fill = "black", font = "Arial 15", text = "Aucun fichier n'est ouvert", anchor ="center", justify = "center")
		
	def create_scrollbar(self):
		global canva

		sheight = lines * 24.5
		swidth = column * 20
		canva.config(scrollregion = (0,0, swidth, sheight), width = 1905, height = 960)
		xscroll = Scrollbar(self, orient = HORIZONTAL)
		yscroll = Scrollbar(self, orient = VERTICAL)
		xscroll.grid(row=1, column=0, sticky=E+W)
		yscroll.grid(row=0, column=1,  sticky=S+N)

		xscroll["command"]=canva.xview
		yscroll["command"]=canva.yview
		canva['xscrollcommand']=xscroll.set
		canva['yscrollcommand']=yscroll.set
	
	def update_scroll_region(self):
		global canva

		canva.update_idletasks()
		canva.config(scrollregion = (0, 0, column, lines*24.5), width = 1905, height = 960)

	def open_file(self):

		global content
		global analyzed
		global lines
		global column

		if content is not None:
			answer = messagebox.askyesno("Ouverture", "Un fichier a été déjà été ouvert, voulez-vous vraiment ouvrir un autre fichier ?")
			if answer == False:
				return
			self.close_file()

		file_name = askopenfilename(title="Choisissez le fichier à ouvrir", filetypes=[("txt files", ".txt")])
		
		if type(file_name) is tuple:		
			return

		file = open(file_name, "r")

		if file is None:
			mes = messagebox.showerror("Erreur", "Problème lors de l'ouverture du fichier")
			return

		lines = file.readlines()
		lines = len(lines)

		file.seek(0)
		content = file.read()
		file.close()

		if len(content) == 0:
			content = None
			messagebox.showerror("Erreur","Le fichier est vide")
			return
		canva.itemconfig(label, text = content, justify ="left")
		canva.moveto(label, 10, 10)
		self.create_scrollbar()

	def close_file(self):
		global content
		global analyzed
		global lines 
		global column
		global label

		if content is not None and analyzed == False:
			answer = messagebox.askyesno("Fermeture","Un fichier a été ouvert mais n'est pas analysé, voulez-vous vraiment fermé le fichier ?")
			if answer == False:
				return

		content = None
		analyzed = False
		canva.delete("all")
		label = canva.create_text(952.5, 480, fill = "black", font = "Arial 15", text = "Aucun fichier n'est ouvert", anchor ="center", justify = "center")
		lines = 1
		column = 1
		self.update_scroll_region()

	def analyze_file(self):
		global content
		global analyzed
		global en_cours

		if content is None:
			messagebox.showerror("Erreur", "Aucun fichier n'a été ouvert")
			return
			
		if analyzed == True:
			messagebox.showerror("Erreur", "Le fichier a déjà été analysé")
			return

		content = analyze_trames(content)
		en_cours = content
		self.print_analyzed_file()
		analyzed = True

	def save_file(self):

		global num

		if content == None:
			mes = messagebox.showerror("Erreur", "Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Erreur", "Vous ne pouvez pas enregistrer un fichier qui n'est pas analysé")
			return
		
		name = asksaveasfilename(title="Enregistrer sous", filetypes=[("pdf files", ".pdf")])
		canva.postscript(file=name, colormode='color', width = column, height = lines*24.5, pagewidth = column, pageheight = lines*24.5)
		messagebox.showinfo("","Bien enregistré")
		num += 1

	def print_analyzed_file(self):
		global content
		global canva
		global en_cours
		global lines
		global column

		canva.delete("all")

		if len(en_cours) == 0:
				canva.create_text(952.5, 480, fill = "black", font = "Arial 15", text = "Aucune trame ne correspond aux critères et/ou n'est exploitable", anchor ="center", justify = "center")
				return

		trames_ethernet, trames_non_ethernet = tri_trames(en_cours)		
		last = 0
		dico,j = recup_address(trames_ethernet)

		for i in range(len(trames_ethernet)):
			trame = trames_ethernet[i]
			color = "red"

			if trame.ipv4:
				source = trame.src_ip
				dest = trame.dest_ip
				color = "purple"
				if trame.tcp :
					if dico[source] > dico[dest]:
						src = dico[source] + 30
						dst = dico[dest] - 30
					else:
						src = dico[source] - 30
						dst = dico[dest] + 30
					canva.create_text(src, 75 + i*60, fill = "black", font = "Arial", text = str(trame.src_port))
					canva.create_text(dst,75 + i*60, fill = "black", font = "Arial", text = str(trame.dest_port))
					color = "green"
					if trame.http == False and trame.content_http == "":
						color = "darkblue"
						trame.mess_is = "TCP : " + str(trame.src_port) + " -> " + str(trame.dest_port) + " " + trame.flags + " Seq = " + str(trame.relative_sequence_number) + " ACK = " + str(trame.relative_ack_number)			
			else:
				source = trame.src_mac
				dest = trame.dest_mac
			canva.create_text(100, 75 + i*60 , fill = "black", font = "Arial", text = "Trame "+str(trame.index))
			canva.create_text((dico[source] + dico[dest])//2, 65 + i*60 , fill = "black", font = "Arial", text = trame.mess_is)
			canva.create_line(dico[source],75 + i*60,dico[dest],75 + i*60, fill = color, arrow="last",tag=trame.mess_is)

		for address in dico:
			canva.create_text(dico[address], 10, fill = "black", font = "Arial", text = address)
			canva.create_line(dico[address],20,dico[address], 75 + len(trames_ethernet)*60, fill = "grey", dash = (5,1))
			last = dico[address]

		if len(trames_non_ethernet) != 0:
			if len(trames_non_ethernet) == 1:
				non_ethernet = "La trame "
				fin = " n'est pas une trame Ethernet II"
			else:
				non_ethernet = "Les trames "
				fin = " ne sont pas des trames Ethernet II"
			for trame in trames_non_ethernet:
				non_ethernet += str(trame.index) + ", "
			non_ethernet = non_ethernet[:-2] + fin
			canva.create_text(250, 100 + len(trames_ethernet)*60, text = non_ethernet, fill = "black", font = "Arial")

		lines = (len(trames_ethernet)*2.75)//1
		column = 200 + last
		self.update_scroll_region()


	def filtre_ip(self):
		global en_cours

		if content == None:
			mes = messagebox.showerror("Erreur","Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Erreur", "Vous ne pouvez pas filtrer un fichier qui n'est pas analysé")
			return

		ip_res = simpledialog.askstring("Adresse IP","Avec quelle addresse IP voulez-vous filtrer ? (EX : 192.168.99.200)")
		ip_res = ip_res.replace(" ","")
		
		temp = []
		for i in range(len(en_cours)):
			if en_cours[i].src_ip == ip_res or en_cours[i].dest_ip == ip_res:
				temp.append(en_cours[i])

		if len(temp) == 0:
			messagebox.showerror("Erreur", "L'adresse IP n'existe pas ou est mal écrite")
			return

		en_cours = temp
		self.print_analyzed_file()
		
	def filtre_port(self):
		global en_cours

		if content == None:
			mes = messagebox.showerror("Erreur", "Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Erreur", "Vous ne pouvez pas filtrer un fichier qui n'est pas analysé")
			return

		port_res = simpledialog.askstring("Port","Avec quel port voulez-vous filtrer ? (EX : 80)")
		port_res = port_res.replace(" ","")
		port_res = int(port_res)
		
		temp = []
		for i in range(len(en_cours)):
			if en_cours[i].src_port == port_res or en_cours[i].dest_port == port_res:
				temp.append(en_cours[i])

		if len(temp) == 0:
			messagebox.showerror("Erreur", "Le port donné n'existe pas ou est mal écrit")
			return

		en_cours = temp
		self.print_analyzed_file()

	def filtre_http(self):
		global en_cours

		if content == None:
			mes = messagebox.showerror("Erreur", "Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Erreur","Vous ne pouvez pas filtrer un fichier qui n'est pas analysé")
			return

		temp=[]
		for i in range(len(en_cours)):
			if en_cours[i].http:
				temp.append(en_cours[i])
		en_cours = temp
		self.print_analyzed_file()

	def filtre_tcp(self):
		global en_cours

		if content == None:
			mes = messagebox.showerror("Erreur","Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Erreur","Vous ne pouvez pas filtrer un fichier qui n'est pas analysé")
			return

		temp = []
		for i in range(len(en_cours)):
			if en_cours[i].tcp:
				temp.append(en_cours[i])
		en_cours = temp
		self.print_analyzed_file()

	def remove_filter(self):
		global en_cours

		if content == None:
			messagebox.showerror("Erreur", "Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			messagebox.showerror("Erreur", "Le fichier n'est pas analysé")
			return

		if en_cours != content:
			en_cours = content
			self.print_analyzed_file()
		else:
			messagebox.showerror("Erreur","Aucun filtre n'est appliqué")

	def info_trame(self):

		if len(en_cours) == 0:
			messagebox.showerror("Erreur", "Aucune trame à afficher")
			return

		num = simpledialog.askstring("Trame", "Numero de la trame dont vous voulez les informations\n(Attention : la trame doit apparaître dans l'interface actuelle)")
		num = num.replace(" ","")
		num = int(num)

		trame = None
		for t in en_cours:
			if t.index == num:
				trame = t

		if trame == None:
			messagebox.showerror("Erreur", "La trame demandée n'existe pas. Si vous pensez qu'elle existe, enlever les filtres.")
			return

		win = Toplevel(self)
		win.geometry("960x540")
		win.resizable(width=False, height=False)
		c = Canvas(win, height = 540, width = 960, bg='lightgrey')
		c.grid(row = 0, column = 0)

		if not trame.ethernet:
			c.create_text(5, 5, fill = "black", font = "Arial", text = "La trame n'est pas ethernet. Aucune donnée à afficher", justify = "center", anchor= N+W)
			return
				
		s = "Trame "+ str(num) +"\n\n"

		s += "Ethernet :\n\n"

		s += "Adresse Mac Source : " + trame.src_mac
		s += "\nAdresse Mac Destination : "+ trame.dest_mac
		s += "\nType : " + str(trame.type)

		if not trame.ipv4:
			s += " (" + trame.mess_is +")"
			c.create_text(5, 5, fill = "black", font = "Arial", text = s, justify = "left", anchor= N+W)
			return

		s += "\n\nIPv4 : \n\n"
		s += "Adresse IP Source : " + trame.src_ip
		s += "\nAdresse IP Destination : " + trame.dest_ip
		s += "\nHeader length : " + str(trame.header_length*4)
		s += "\nTotal length : " + str(trame.total_length)
		s += "\nProtocole : " + trame.protocol
		
		if not trame.tcp:
			s += " (" + trame.mess_is +")"
			c.create_text(5, 5, fill = "black", font = "Arial", text = s, justify = "left", anchor= N+W)
			return

		s += "\n\nTCP : \n\n"
		s += "Port Source : " + str(trame.src_port)
		s += "\nPort Destination : " + str(trame.dest_port)
		s += "\nSequence Number : " + str(trame.sequence_number)
		s += "\nAcknowledgment Number : " + str(trame.ack)
		s += "\nWindow : " + str(trame.window)
		s += "\nTCP Flags : " + trame.flags

		if  trame.http:
			s += "\n\nHTTP :\n\n" + trame.content_http
			taille = trame.content_http.splitlines()
			sheight = (27 + len(trame.content_http.splitlines())) * 24.5
			swidth = 1
			for t in taille:
				if len(t) * 10 > swidth:
					swidth = len(t) * 10
			c.config(scrollregion = (0,0, swidth, sheight), width = 945, height = 525)
			xscroll = Scrollbar(win, orient = HORIZONTAL)
			yscroll = Scrollbar(win, orient = VERTICAL)
			xscroll.grid(row=1, column=0, sticky=E+W)
			yscroll.grid(row=0, column=1,  sticky=S+N)

			xscroll["command"]=c.xview
			yscroll["command"]=c.yview
			c['xscrollcommand']=xscroll.set
			c['yscrollcommand']=yscroll.set

		c.create_text(5, 5, fill = "black", font = "Arial", text = s, justify = "left", anchor= N+W)

		logo = PhotoImage(file = "logo.png")
		win.iconphoto(False, logo)


	def help(self):
		messagebox.showinfo("Help", "Menu :\n\nOpen -> Ouvre un fichier et l'affiche\nAnalyze -> Analyse le fichier ouvert et affiche sa représentation \"flow_graph\"\nSave as... -> Sauvegarde la représentation flow_graph dans un fichier pdf\nClose -> Ferme le fichier\nQuit -> Ferme l'application\n\nFiltres :\n\nAdresse Ip -> Affiche les trames utilisant l'adresse ip donnée (attention au format)\nPort -> Affiche les trames utilisant le port donné\nTCP -> Affiche uniquement les trames ayant comme protocole TCP\nHTTP -> Affiche uniquement les trames ayant comme protocle HTTP\n\nCouleurs :\n\nRouge -> Ethernet\nViolet -> IPv4\nBleu -> TCP\nVert -> HTTP")

	def about(self):
		messagebox.showinfo("About", "LU3IN033 - Projet de Réseaux\n\nPar Léa Movsessian et Maïna Laurent\n\nLe logo a été fait par l'AI DALL-E\nLe nom Fireshark est inspiré de Wireshark et est une référence au mythe de Prométhée\n\nTkinter nous a donné du fil à retordre, j'espère qu'il marchera correctement sur mac... Sinon je vous offre un tacos contre quelques points ?")