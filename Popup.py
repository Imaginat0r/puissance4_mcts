
from tkinter import *
from tkinter import messagebox
import tkinter as tk


class PopUp():
	"""Fenêtre de sélection du mode de jeu"""
	def __init__(self, title = 'My Title') -> None:
		self.choix = None
		self.root = tk.Tk()
		self.root.title(title)

		self.root.option_add('*Font', '35')
		self.root.geometry("200x80")
		top_frame = tk.Frame(self.root)
		bottom_frame = tk.Frame(self.root)
				
		self.radio_var = tk.IntVar()
				
		self.radio_var.set(0)

		rb1 = tk.Radiobutton(top_frame,
								text='HUMAIN VS IA',
								variable=self.radio_var,
								value=1)
		rb2 = tk.Radiobutton(top_frame,
								text='IA VS IA',
								variable=self.radio_var,
								value=2)

		rb1.pack()
		rb2.pack()

		ok_button = tk.Button(bottom_frame,
								text='OK',
								command=self.get_choice)

		ok_button.pack(side='left')

		top_frame.pack()
		bottom_frame.pack()

						
		self.root.mainloop()
	
	def get_choice(self):	
		self.root.destroy()
		self.choix = self.radio_var.get()

