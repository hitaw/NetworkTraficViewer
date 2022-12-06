from win32gui import *
from tkinter import *

def impression_pdf():
	master = Tk()
	cv = Canvas(master, width=200, height=100)
	cv.pack()
	cv.create_rectangle(50, 25, 150, 75, fill="blue")
	l = Label(cv, text='Label', bd=0, padx=3, pady=1)
	cv.create_window(20, 20, window=l)
	b = Button(cv, text='draw', command=lambda :cv.postscript(file="ecran.ps", colormode='color'))
	cv.create_window(100, 48, window=b)
	mainloop()