from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
from analyze import *
from affichage import *

content = None
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
		self.create_menu_2()
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
		menu_file.add_command(label = "Save", command = self.save_file, accelerator = "CTRL+S")
		menu_file.add_command(label ="Close", command = self.close_file, accelerator = "CTRL+F")
		menu_file.add_separator()
		menu_file.add_command(label = "Help", command=self.help, accelerator = "CTRL+H")
		menu_file.add_command(label = "Quit", command=self.quit, accelerator = "CTRL+C")
		menu_bar.add_cascade(label="Menu", font = ("Arial",15), menu=menu_file)

		self.bind_all("<Control-o>", lambda x: self.open_file())
		self.bind_all("<Control-a>", lambda x: self.analyze_file())
		self.bind_all("<Control-s>", lambda x: self.save_file())
		self.bind_all("<Control-f>", lambda x: self.close_file())
		self.bind_all("<Control-h>", lambda x: self.help())
		self.bind_all("<Control-c>", lambda x: self.quit())

		self.config(menu=menu_bar)

	def create_menu_2(self):
		menu_bar = Menu(self)

		menu_file = Menu(menu_bar, tearoff = 0)
		menu_file.add_command(label = "Open", command = self.open_file, accelerator = "CTRL+O")
		menu_file.add_command(label = "Analyze", command = self.analyze_file, accelerator = "CTRL+A")
		menu_file.add_command(label = "Save", command = self.save_file, accelerator = "CTRL+S")
		menu_file.add_command(label ="Close", command = self.close_file, accelerator = "CTRL+F")
		menu_file.add_separator()
		menu_file.add_command(label = "Help", command=self.help, accelerator = "CTRL+H")
		menu_file.add_command(label = "Quit", command=self.quit, accelerator = "CTRL+C")
		menu_bar.add_cascade(label="Menu", font = ("Arial",15), menu=menu_file)

		self.bind_all("<Control-o>", lambda x: self.open_file())
		self.bind_all("<Control-a>", lambda x: self.analyze_file())
		self.bind_all("<Control-s>", lambda x: self.save_file())
		self.bind_all("<Control-f>", lambda x: self.close_file())
		self.bind_all("<Control-h>", lambda x: self.help())
		self.bind_all("<Control-c>", lambda x: self.quit())

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

		if content is None:
			messagebox.showerror("Erreur", "Aucun fichier n'a été ouvert")
			return
			
		if analyzed == True:
			messagebox.showerror("Erreur", "Le fichier a déjà été analysé")
			return

		content = analyze_trames(content)
		self.print_analyzed_file()
		analyzed = True

	def save_file(self):

		global num

		if content == None:
			mes = messagebox.showerror("Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Vous ne pouvez pas enregistrer un fichier qui n'est pas analysé")
			return
		
		name = "screen_fireshark" + str(num) + ".pdf"
		canva.postscript(file=name, colormode='color', width = column, height = lines*24.5, pagewidth = column, pageheight = lines*24.5)
		messagebox.showinfo("","Bien enregistré")
		num += 1

	def print_analyzed_file(self):
		global content
		global canva
		global liste_label
		global liste_button
		global lines
		global column

		canva.itemconfig(label, text = "")
		trames_ethernet = tri_trames(content)
		last = 0
		dico,j = recup_address(trames_ethernet)

		for i in range(len(trames_ethernet)):
			trame = trames_ethernet[i]
			color = "darkred"

			if trame.ipv4:
				source = trame.src_ip
				dest = trame.dest_ip
				color = "darkpurple"
				if trame.tcp :
					color = "green"
					if trame.http == False and trame.content_http == "":
						color = "darkblue"
						trame.mess_is = "TCP : " + str(trame.src_port) + " -> " + str(trame.dest_port) + " " + trame.flags + " Seq = " + str(trame.relative_sequence_number) + " ACK = " + str(trame.relative_ack_number)			
			
			canva.create_text(100, 75 + i*60 , fill = "black", font = "Arial", text = "Trame "+str(trame.index))
			canva.create_text((dico[source] + dico[dest])//2, 65 + i*60 , fill = "black", font = "Arial", text = trame.mess_is)
			canva.create_line(dico[source],75 + i*60,dico[dest],75 + i*60, fill = color, arrow="last",tag=trame.mess_is)

		for address in dico:
			canva.create_text(dico[address], 10, fill = "black", font = "Arial", text = address)
			canva.create_line(dico[address],20,dico[address], 75 + len(trames_ethernet)*60, fill = "grey", dash = (5,1))
			last = dico[address]

		lines = (len(trames_ethernet)*2.5)//1
		column = 200 + last
		self.update_scroll_region()

	def help(self):
		h = messagebox.showinfo("Help", "xxx")

def liste_deroulante():
	root = Interface()
	liste_filtres = ["adresses IP", "ports", "protocoles"]
	res = ttk.Combobox(root, values = liste_filtres)
	res.current(0)

	res.bind("adresses IP",selection)
	res.bind("ports",selection)
	res.bind("protocoles",selection)
	
	root.mainloop()

def selection(event):
	select = res.get()
	if select == "adresses IP":
		ip_res = simpledialog.askstring("Adresse IP","Les messages liés à quelle adresse IP voulez-vous voir ?")
		print(filtre_ip(ip_res))
	elif select == "ports":
		port_res = simpledialog.askstring("Port","Les messages liés à quel port voulez-vous voir ?")
		print(filtre_ports(port_res))
	else :
		protocole_res = simpledialog.askstring("Protocole","Les messages liés à quel protocole voulez-vous voir ?")
		print(filtre_protocoles(protocole_res))


def filtre_ip(ip):
	res = []
	for i in range(len(content)):
		if content[i].src_ip == ip or content[i].dest_ip == ip:
			res.append(content[i])
	return res
	
def filtre_port(port):
	res = []
	for i in range(len(content)):
		if content[i].src_port == port or content[i].dest_port == port:
			res.append(content[i])
	return res

def filtre_http():
	res=[]
	for i in range(len(content)):
		if content[i].http:
			res.append(content[i])
	return res

def filtre_tcp():
	res=[]
	for i in range(len(content)):
		if content[i].tcp:
			res.append(content[i])
	return res
