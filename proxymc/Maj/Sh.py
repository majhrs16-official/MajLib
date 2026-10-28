
try: from ctypes    import WinDLL
except: WinDLL = None
from re             import match
from socket         import socket, AF_INET, SOCK_DGRAM
from threading      import Thread
from urllib.request import build_opener
from uuid           import getnode
from sys            import (
	stderr as ERR,
	stdout as OUT,
	stdin  as IN
)

class ProgressBar(object):
	def __init__(self, max, width=50):
		self._T = max
		self._X = width
		self.i  = 0
	def __iter__(self):
		return self

	step = __next__ = lambda self, i = +1: self.set(self.i + i)

	def get(self, _ = 100):
		return _ * self.i / float(self._T)

	def set(self,i):
		self.i  = i
		percent = "{0:.2f}".format(self.get())
		bar     = round(self.get(self._X))
		print("\r[{0}] {1}%\r".format("█" * bar + "-" * (self._X - bar), percent), end = "")
PB = ProgressBar

def FormatErr(Exc): return (str(Exc.__class__.__name__), str(Exc))
def PrintErr(Exc): print(*FormatErr(Exc), sep = ": ", file = ERR)

def MAC():
	MAC=hex(getnode())[2:].upper()
		# f'{getnode():02x}'.upper()
		# '{:02x}'.format(getnode()).upper()
		# "%x".upper() % x
	return ":".join([MAC[i:i+2] for i in range(0,len(MAC),2)])

def Percent(s): ## algo no me convence...ujummmm, lo veo algo inpotente y rebundante aunq, a veces es muy util....
	"""Percent(str) -> float
    >>> Percent("30%1200")
    360.0
    >>> Percent("30-%1200")
    330.0
    >>> Percent("30+%1200")
    330.0
"""
	if match("\d+\%\d+",s):
		v=s.split("%")
		v=float(v[0])*float(v[1])/100
	elif match("\d+\+\%\d+",s):
		v=s.split("+%")
		v=float(v[0])*float(v[1])/100+float(v[0])
	elif match("\d+\-\%\d+",s):
		v=s.split("-%")
		v=float(v[0])*float(v[1])/100-float(v[0])
	else: raise ValueError(Percent.__doc__)
	return v

def _GetSize(num, max, Bits):
	if not isinstance(num,(int,float)): raise TypeError("{!r} != float/int".format(num))
	if num<0: raise ZeroDivisionError("not {!r} > 0".format(num))
	if max is not None and max not in range(8 +1): raise IndexError("{!r} not in range(0, 8 +1)".format(max))

	Multiple = 1000 if Bits else 1024
	Sufijos  = {
		1024:["B","KB","MB","GB","TB","PB","EB","ZB","YB"],
		1000:["b","Kb","Mb","Gb","Tb","Pb","Eb","Zb","Yb"]
	}[Multiple]
	for Sufijo in Sufijos:
		if max and Sufijo==Sufijos[max]:
			return (num, Sufijo)
		elif num <= Multiple: return (num, Sufijo)
		num /= Multiple

	raise OverflowError("Max value: %s" % 1024**8)
def GetSize(num: "int or float", max: 8 = None, Bits: bool = False):
	"""
GetSize(int or float, int, bolean) -> float
    >>> GetSize(1024 ** 4)
    '1 TB'
    >>> GetSize(1024 ** 4, 2) # TB -> MB
    '1048576 MB'
    >>> GetSize(1024 ** 3, Bits = True) # GByte -> Gbit
    '1.07 Gb'
"""
	num, Sufijo = _GetSize(num, max, Bits)
	return "{0:.2f} {1}".format(int(num) if int(num) == num else num, Sufijo)

def NetIP():
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]
	finally: s.close()

def iNetIP(timeout=60):
	web = build_opener()
	web.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]

	sock=None
	try:
		sock = web.open(URL, timeout=timeout)
		return sock.read().decode()
	except Exception as e: return e
	finally: sock and sock.close()

class Class(object):
	def __init__(self,**Kw): self.__dict__.update(Kw)
	def __setitem__(self,k,v): self.__dict__[k]=v
	def __getitem__(self,k): return self.__dict__[k]
	def __delitem__(self,k): del self.__dict__[k]
	def __repr__(self): return str(self.__dict__)

def dThread(func):
	def start(*args, _daemon = None, _name = None, **kw):
		t = Thread(
			daemon = _daemon,
			target = func,
			args   = args,
			kwargs = kw,
			name   = _name
		)
		return t.start
	return start

if WinDLL:
	def _windowsConsole(state):
		WinDLL('user32').ShowWindow(WinDLL('kernel32').GetConsoleWindow(), state)
	def minimize(): _windowsConsole(6)
	def hide(): _windowsConsole(0)
