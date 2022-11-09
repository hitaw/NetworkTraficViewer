#Projet Réseaux
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from analyze import *

content = None
analyzed = False
label = None
canva = None

class Interface(Tk):

	def __init__(self):
		Tk.__init__(self)
		self.create_menu_bar()
		self.geometry("1920x1080")
		self.title("Network traffic viewer")
		self.create_canva()


	def create_menu_bar(self):
		menu_bar = Menu(self)

		menu_file = Menu(menu_bar, tearoff = 0)
		menu_file.add_command(label = "Open", command = self.open_file, accelerator = "CTRL+O")
		menu_file.add_command(label = "Analyze", command = self.analyze_file, accelerator = "CTRL+A")
		menu_file.add_command(label ="Close", command = self.close_file, accelerator = "CTRL+F")
		menu_file.add_separator()
		menu_file.add_command(label = "Help", command=self.help, accelerator = "CTRL+H")
		menu_file.add_command(label = "Quit", command=self.quit, accelerator = "CTRL+C")
		menu_bar.add_cascade(label="Menu", font = ("Arial",15), menu=menu_file)

		self.bind_all("<Control-o>", lambda x: self.open_file())
		self.bind_all("<Control-a>", lambda x: self.analyze_file())
		self.bind_all("<Control-f>", lambda x: self.close_file())
		self.bind_all("<Control-h>", lambda x: self.help())
		self.bind_all("<Control-c>", lambda x: self.quit())

		self.config(menu=menu_bar)

	def create_canva(self):
		global label
		global canva

		canva = Canvas(self,  scrollregion =(0, 0, 2000, 1100), width=1905, height=960, bg='ivory')
		canva.grid(row = 0, column = 0)

		xscroll = ttk.Scrollbar(self, orient = HORIZONTAL)
		yscroll = ttk.Scrollbar(self, orient = VERTICAL)
		xscroll.grid(row=1, column=0, sticky=E+W)
		yscroll.grid(row=0, column=1,  sticky=S+N)

		xscroll["command"]=canva.xview
		yscroll["command"]=canva.yview
		canva['xscrollcommand']=xscroll.set
		canva['yscrollcommand']=yscroll.set

		label = canva.create_text(950, 10, fill = "black", font = "Arial 15", text = "Aucun fichier n'est ouvert")

	def open_file(self):

		global content
		global analyzed
		global label

		if (content != None and analyzed == False):
			answer = messagebox.askyesno("Ouverture", "Un fichier a été déjà été ouvert et n'est pas analysé, voulez-vous vraiment ouvrir un autre fichier ?")
			if answer == False:
				return

		file_name = askopenfilename(title="Choisissez le fichier à ouvrir", filetypes=[("txt files", ".txt")])
		
		if (type(file_name) is tuple):		
			return

		file = open(file_name, "r")

		if (file == None):
			mes = messagebox.showerror("Erreur", "Problème lors de l'ouverture du fichier")
			return

		content = file.read()
		file.close()
		canva.itemconfig(label, text = content)


	def close_file(self):
		global content
		global analyzed
		global label
		global canva

		if (content != None and analyzed == False):
			answer = messagebox.askyesno("Fermeture","Un fichier a été ouvert mais n'est pas analysé, voulez-vous vraiment fermé le fichier ?")
			if answer == False:
				return

		content = None
		analyzed = False
		canva.itemconfig(label, text = "Aucun fichier n'est ouvert")



	def analyze_file(self):
		global content
		global analyzed

		if (content == None):
			messagebox.showerror("Erreur", "Aucun fichier n'a été ouvert")
			return
			
		if (analyzed == True):
			messagebox.showerror("Erreur", "Le fichier a déjà été analysé")
			return

		content = analyze(content)
		self.print_analyzed_file()
		analyzed = True

	def print_analyzed_file(self):
		global content
		global label
		global canva
		canva.itemconfig(label, text = content)
		return

	def help(self):
		h = messagebox.showinfo("Help", "xxx")