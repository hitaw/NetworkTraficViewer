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
frame = None

class Interface(Tk):

	def __init__(self):
		global cont
		global canva
		global label
		global frame

		Tk.__init__(self)

		canva = Canvas(self)

		self.create_menu_bar()
		self.geometry("1920x1080")
		self.title("Fireshark")
		self.create_frame()
		self.create_canva()
		self.create_label()
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
		menu_file.add_command(label = "Help", command=self.help, accelerator = "CTRL+H")
		menu_file.add_command(label = "Quit", command=self.quit, accelerator = "CTRL+C")
		menu_bar.add_cascade(label="Menu", font = ("Arial",15), menu=menu_file)

		self.bind_all("<Control-o>", lambda x: self.open_file())
		self.bind_all("<Control-a>", lambda x: self.analyze_file())
		self.bind_all("<Control-s", lambda x: self.save_file())
		self.bind_all("<Control-f>", lambda x: self.close_file())
		self.bind_all("<Control-h>", lambda x: self.help())
		self.bind_all("<Control-c>", lambda x: self.quit())

		self.config(menu=menu_bar)

	def create_canva(self):
		global label
		global canva
		global frame
		global cont

		xscroll = Scrollbar(self)
		yscroll = Scrollbar(self)

		canva.config(xscrollcommand = xscroll.set, yscrollcommand = yscroll.set, bg = "lightgrey")
		xscroll.config(orient = HORIZONTAL, command = canva.xview)
		yscroll.config(orient = VERTICAL, command = canva.yview)

		xscroll.pack(fill = X, side = BOTTOM, expand = FALSE)
		yscroll.pack(fill = Y, side = RIGHT, expand = FALSE)
		canva.pack(fill = BOTH, side = LEFT, expand = TRUE)
		canva.create_window(0, 0, window = frame, anchor = NW)

	def create_frame(self):
		global frame
		frame = Frame(canva, bg = "lightgrey")

	def create_label(self):
		global label
		global cont
		cont = StringVar()
		cont.set("Aucun fichier n'est ouvert")
		label = Label(frame, textvariable = cont, font = "Arial", justify = "left", bg = "lightgrey").grid(row = 1, column = 1, pady = 10, padx = 10)
	
	def update_scroll_region(self):
		global canva 
		global frame

		canva.update_idletasks()
		canva.config(scrollregion = frame.bbox())

	def open_file(self):

		global content
		global analyzed

		if content is not None and analyzed == False:
			answer = messagebox.askyesno("Ouverture", "Un fichier a été déjà été ouvert et n'est pas analysé, voulez-vous vraiment ouvrir un autre fichier ?")
			if answer == False:
				return

		file_name = askopenfilename(title="Choisissez le fichier à ouvrir", filetypes=[("txt files", ".txt")])
		
		if type(file_name) is tuple:		
			return

		file = open(file_name, "r")

		if file is None:
			mes = messagebox.showerror("Erreur", "Problème lors de l'ouverture du fichier")
			return

		file.seek(0)
		content = file.read()
		file.close()

		cont.set(content)
		self.update_scroll_region()

	def close_file(self):
		global content
		global analyzed
		global frame
		global cont

		if content is not None and analyzed == False:
			answer = messagebox.askyesno("Fermeture","Un fichier a été ouvert mais n'est pas analysé, voulez-vous vraiment fermé le fichier ?")
			if answer == False:
				return

		content = None
		analyzed = False
		canva.delete("all")
		self.create_frame()
		self.create_label()
		canva.create_window(0, 0, window = frame, anchor = NW)
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

		if content == None:
			mes = messagebox.showerror("Aucun fichier n'est ouvert")
			return

		if analyzed == False:
			mes = messagebox.showerror("Vous ne pouvez pas enregistrer un fichier qui n'est pas analysé")
			return
		
		file_name = asksaveasfile("w", defaultextension = ".pdf")
		img = ImageGrab.grab()
		img.save('screen_fireshark.pdf',save_all=True)


	def print_analyzed_file(self):
		global content
		global canva
		global cont
		global frame
		global liste_label
		global liste_button

		(trames_ethernet, trames_non_ethernet) = tri_trames(content)

		dico,j = recup_address(trames_ethernet)
		for address in dico:
			l = Label(frame, text = address, font = "Arial", justify = "center", bg = "lightgrey")
			liste_label.append(l)
			l.place(x = dico[address]-40, y = 10)
			canva.create_line(dico[address],20,dico[address], 1000, fill = "grey", dash = (5,1))

		f = " "*(j//2)
		for i in range(len(trames_ethernet)):
			trame = trames_ethernet[i]

			if trame.ipv4:
				source = trame.src_ip
				dest = trame.dest_ip

				if trame.tcp :
					if not trame.http:
						trame.mess_is = str(trame.src_port) + " -> " + str(trame.dest_port) + " " + trame.flags + " Seq = " + str(trame.relative_sequence_number) + " ACK = " + str(trame.relative_ack_number)			
			
			b = Button(frame, text = "Trame "+str(trame.index))
			liste_button.append(b)
			b.place(x = 5, y = 60 + i*40)
			canva.create_line(dico[source],60 + i*40,dico[dest],60 + i*40,arrow="last",tag=trame.mess_is)
			#f += "\n"*40
		erreurs = "Les Trames "
		for t in trames_non_ethernet:
			erreurs += str(t.index) + ", "
		erreurs = erreurs[:-2]
		erreurs += " ne sont pas des trames Ethernet ou ne sont pas exploitables."

		#f += "\n"
		cont.set(f)
		self.update_scroll_region()
		#l = Label(frame, j)

	def help(self):
		h = messagebox.showinfo("Help", "xxx")