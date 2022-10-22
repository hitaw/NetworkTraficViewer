#Projet Réseaux
from tkinter import *
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import ttk

content = None
analyzed = False
label = None

class Interface(Tk):

	def __init__(self):
		Tk.__init__(self)
		global label
		label = Label(self, text = "Aucun fichier n'est ouvert", font = ("Arial", 15), justify = "left", width = 1900, wraplength = 1900)
		label.pack()
		self.create_menu_bar()
		self.geometry("1920x1080")
		self.title("Network traffic viewer")


	def create_menu_bar(self):
		menu_bar = Menu(self)

		menu_file = Menu(menu_bar, tearoff = 0)
		menu_file.add_command(label = "Open", command = self.open_file, accelerator = "CTRL+O")
		menu_file.add_command(label = "Analyze", command = self.analyze_file, accelerator = "CTRL+A")
		menu_file.add_command(label ="Close", command = self.close_file, accelerator = "CTRL+C")
		menu_file.add_separator()
		menu_file.add_command(label = "Help", command=self.help, accelerator = "CTRL+H")
		menu_bar.add_cascade(label="Menu", font = ("Arial",15), menu=menu_file)

		self.bind_all("<Control-o>", lambda x: self.open_file())
		self.bind_all("<Control-a>", lambda x: self.analyze_file())
		self.bind_all("<Control-c>", lambda x: self.close_file())
		self.bind_all("<Control-h>", lambda x: self.help())

		self.config(menu=menu_bar)

	def open_file(self):

		global content
		global analyzed
		global label

		if (content != None and analyzed == False):
			answer = messagebox.askyesno("Ouverture", "Un fichier a été déjà été ouvert et n'est pas analysé, voulez-vous vraiment réouvrir un autre fichier ?")
			if answer == False:
				return

		file_name = askopenfilename(title="Choose the file to open", filetypes=[("txt files", ".txt")])
		
		if (file_name == None):
			return

		file = open(file_name, "r")

		if (file == None):
			mes = messagebox.showerror("Erreur", "Problème lors de l'ouverture du fichier")
			return

		content = file.read()
		file.close()

		label.configure(text = content)


	def close_file(self):
		global content
		global analyzed
		global label

		if (content != None and analyzed == False):
			answer = messagebox.askyesno("Fermeture","Un fichier a été ouvert mais n'est pas analysé, voulez-vous vraiment fermé le fichier ?")
			if answer == False:
				return

		content = None
		analyzed = False
		label.configure(text =  "Aucun fichier n'est ouvert")



	def analyze_file(self):
		global content
		if (content == None):
			messagebox.showerror("Erreur", "Aucun fichier n'a été ouvert")

			

	def help(self):
		h = messagebox.showinfo("Help", "xxx")

window = Interface()
window.mainloop()