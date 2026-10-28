#! /usr/bin/env python3

"python3 UI.py IP [Port] [Binding Port]"

from socket     import *
from Proxy      import Proxy
from threading  import Thread
from Maj.Sh     import GetSize, dThread, ERR
from os         import system as call
#from Maj.Tk     import Tk, Label
#from PIL        import ImageTk
#from random     import randint
#from Maj.Oscope import Oscope
from time       import sleep
from sys        import (
	argv,
	platform as OS,
	exit ## py2exe bug: NameError(exit, quit)
)

class Proxy(Proxy): IO = IOps = 0
class FailCloseServer(Exception): pass

def Exit():
	Proxy._Exit = True
	sleep(1)
	try: Server.close()
	except: Logger(FailCloseServer, None)

def Config(e): L1.X, L1.Y = e.width, e.height

@dThread
def GUI(): ## re fail ##
	img = Oscope()
	img.Create(800, 5000)
	i=1
	while 1:
		for i2, ((IP, Port), Prox) in enumerate(sorted(Clients.copy().items())):
			if not hasattr(Prox, "History"): Prox.History = [[], []]
			if not hasattr(Prox, "Color"): Prox.Color     = (randint(0, 255), randint(0, 255), randint(0, 255))
			Prox.History[1].append(Prox.IOps)
			while len(Prox.History[1]) > 800: Prox.History[1].pop(0)
			img.Update(Prox.History[1], Prox.Color)
		L1.img = ImageTk.PhotoImage(img.Get().resize((L1.X, L1.Y)))
		L1["image"] = L1.img  #.save("img/%s.png" % i)
		print(i)
		i += 1

@dThread
def Login():
	while not Proxy._Exit:
		try:
			Client, ID          = Server.accept()
			Clients[ID]         = Proxy((IP, Port), Client, ID, Logger)
#			Clients[ID].Color   = (randint(0, 255), randint(0, 255), randint(0, 255))
#			Clients[ID].History = [[], []]
			Clients[ID].IO      = 0 # bug
			VelocityTimer(ID)()
		except Exception as e: Logger(e, Server)

def Logger(i, ID):
	if i is False:
		sleep(5)
		Clients.pop(ID, None)

	elif isinstance(i, int):
		Clients[ID].IO += i
		Proxy.IO       += i

	else:
		print("{} {}: {}".format(ID, i.__class__.__name__, i), file = ERR)

def UI():
	while not Proxy._Exit:
		D = ["\n\tProxyMC {}\n\n"
		     "0    0.0.0.0         {}{}{}",
		     "#    IP              Port    IO         IO/s"]
#		      1234 255.255.255.255 123456  1234.56 xB 1234.56 xB/s

		for i, ((IP, Port), Prox) in enumerate(sorted(Clients.copy().items())):
			D.append(
				str(i+1).            ljust(5)  + \
				IP.                  ljust(16) + \
				str(Port).           ljust(8)  + \
				GetSize(Prox.IO).    ljust(11) + \
				GetSize(Prox.IOps) + "/s"
			)
			Proxy.IOps += Prox.IOps

		D[0] = D[0].format(
			__version__,
			str(Bind).ljust(8),
			GetSize(Proxy.IO).ljust(11),
			GetSize(Proxy.IOps) + "/s".ljust(13),
		)
		Proxy.IOps = 0
		print("\n".join(D))
		sleep(1 / 5) # FPS
		call("cls || clear")

@dThread
def VelocityTimer(ID):
	while 1:
		Bps = Clients[ID].IO
		sleep(1)
		Clients[ID].IOps = Clients[ID].IO - Bps

global Clients
__version__            = "v2.5"
if __name__ == "__main__":
	if not argv[1:]:
		print(__doc__)
		exit()
	if not argv[2:]: argv.append(25565)
	if not argv[3:]: argv.append(25565)
	IP, Port, Bind = argv[1], int(argv[2]), int(argv[3])
	Clients        = {}
	Server         = socket()
#	Server.settimeout(60)
	Server.bind(("", Bind))
	Server.listen(16)

	Login(_daemon = True)()

	"""
	w = Tk()
	with Label(w) as L1:
		L1.bind("<Configure>", Config)
		L1.X = L1.Y = 0
	L1.pack(expand = 1, fill = "both")
	GUI()()
	w.mainloop()
	"""

	try: UI()
	except KeyboardInterrupt: pass
	finally: Exit()
