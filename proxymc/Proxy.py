from socket    import *
from threading import Thread
from Maj.Sh    import dThread

class FailConnectToServer(Exception): pass
class FailCloseClient(Exception): pass
class FailCloseSocket(Exception): pass

class Proxy:
	_Exit = False
	BUFF  = 1024 * 16

	def __init__(self, Server, Client, ID, logger = (lambda D, HOST: ...)):
		self.Proxy = socket()
		self.Proxy.settimeout(60)
		try: self.Proxy.connect(Server)
		except Exception as e:
			return logger(FailConnectToServer(Server, e), ID)

		self.Client = Client
		self.log    = logger
		self.ID     = ID

		self.Redirect(self.Proxy, Client, _daemon = True)()
		self.Redirect(Client, self.Proxy, _daemon = True)()

	def _Redirect(self, From, To):
		D = From.recv(self.BUFF)
		i = 0
		while i < len(D):
			i += To.send(D[i:])
			if not D: break
		self.log(i, self.ID)
	@dThread
	def Redirect(self, From, To):
		try:
			while not self._Exit: self._Redirect(From, To)
		except Exception as e: self.log(e, self.ID)
		self.Exit()

	def Exit(self):
		self._Exit = True
		try: self.Client.close()
		except: self.log(FailCloseClient(self.Client), self.ID)
		try: self.Proxy.close()
		except: self.log(FailCloseSocket(self), self.ID)

		self.log(False, self.ID)
