
from Majhrs import *
from sys import exit
from threading import Thread
from time import sleep

class App(Tk):
	def __init__(self):
		Tk.__init__(self,title="BinaryTranslator",ver="v1.8.6")

		self._AC=True # AC = Convert to binary
		with ttk.Frame(self) as F1:
			with ttk.Label(F1,text="Texto") as self.L1:
				with Text(F1,width=50,wrap=WORD) as self.T1:
					self.T1.focus()
					def MC(e):
						MC=Menu(self,tearoff=0)
						MC.add_command(label="Pegar",command=lambda: (self.T1.delete(0.0,END),self.T1.insert(0.0,self.Paste())) if self.Paste() else None)
						MC.post(e.x_root,e.y_root)
					self.T1.bind("<3>",MC)
					self.T1.grid(row=1,column=0)
				self.L1.grid(row=0,column=0)

			Button(F1,text="<->",width=3,relief=FLAT,command=self.AC).grid(row=0,column=1)

			def MC(e):
				MC=Menu(self,tearoff=0)
				MC.add_command(label="Copiar todo",command=lambda: self.Copy(self.T2.get(0.0,END)))
				MC.post(e.x_root,e.y_root)
			with ttk.Label(F1,text="Binario") as self.L2:
				with Text(F1,width=50) as self.T2:
					self.T2.bind("<3>",MC)
				self.T2.grid(row=1,column=2)
			self.L2.grid(row=0,column=2)

		F1.pack(expand=1)

		self.MenuBar()

		Thread(daemon=1,target=self.CheckT1).start()

	def Paste(self):
		try: return self.clipboard_get()
		except: pass

	def Copy(self,s):
		self.clipboard_clear()
		self.clipboard_append(s)
		return len(s)

	def CheckT1(self):
		while 1:
			self.Convertor()
			sleep(.5)

	def AC(self):
		L1=self.L1["text"]
		L2=self.L2["text"]
		self.L1["text"]=L2
		self.L2["text"]=L1

		T2=self.T2.get(0.0,END)
		self.T1.delete(0.0,END)
		self.T2.delete(0.0,END)
		self._AC=not self._AC
		sleep(1)
		self.T1.insert(0.0,T2)
		# osea T1,T2=T2,T1

	def Encript(self,str):
		return "".join(bin(ord(s))[2:].rjust(8,"0") for s in str).upper()

	def Decript(self,s):
		try: return "".join(chr(eval("0b"+s[i:i+8],{"__builtins__":None},{})) for i in range(0,len(s),8))
		except: return "¡Error!"

	def Convertor(self,E=None):
		self.T2.delete(0.0,END)
		D=self.T1.get(0.0,END).rstrip("\r").rstrip("\n")
		if self._AC: self.T2.insert(END,self.Encript(D))
		else: self.T2.insert(END,self.Decript(D))

	def Exit(self): Tk.Exit(self) and Tk.Exit(self)

	def MenuBar(self):
		with Tk.MenuBar(self) as MB:
			with Menu(MB,title="Archivo") as SB:
				SB.add_command(label="Cerrar",command=self.Exit)

			with Menu(MB,title="Ayuda") as SB:
				SB.add_command(label="Acerca de...",command=self.About)
	def About(self):
		MsgInfo("Acerca de ...",
"""Binary Translator
Desarrolladores: Majhrs16 y Yowen
Version: {Ver}

Licencia:
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
""".format(Ver=self.__ver__))

if __name__=="__main__":
	with App(): pass
