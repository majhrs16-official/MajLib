
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime       import datetime, timedelta
from time           import sleep, localtime
from urllib.request import build_opener

Time=lambda: datetime(*localtime()[:-3])
class FMIP:
	def __init__(self, *Hosts):
		self.web            = build_opener()
		self.web.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]
		self.max            = timedelta(0, 180) #3min #300 = 5min
		self.URLs           = Hosts
		self._Exit          = False

	def Clock(self):
		T = Time()
		while not self._Exit:
			try:
				print("[ Wait ] %s" % (self.max - (Time() - T)), end="\r")
				if Time()-T > self.max:
					for i in range(len(self.URLs)):
						print("[ Wait ] Updating hostings...", end="\r")
						D=self.Update(self.URLs[i])
						if   b"OK"    == D:
							print("[  OK  ] Updating host #%s." % (i+1))
						elif b"ERROR" == D:
							print("[ FAIL ] Updating host #%s." % (i+1))
						else:
							print("[ERROR ] Updating host.\n"
                                    f"\t{D.__class__.__name__}: {D}")

					T = Time()
				sleep(1)
			except KeyboardInterrupt: return

	def Update(self, URL):
		try:
			sock = self.web.open(URL, timeout = 60)
			return sock.read()
		except Exception as e: return e
		finally: sock.close()

	def Stop(self): self._Exit = True
