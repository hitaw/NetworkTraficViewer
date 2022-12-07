from tkinter import *
from interface import *
from PIL import ImageGrab, Image

def impression_pdf():
	img = ImageGrab.grab()
	img.save('screen_fireshark.pdf',save_all=True)