
from pyaudio import paFloat32,PyAudio

BUFF=1024

class App():
	def __init__(self):
		f=PyAudio().open(format = paFloat32, channels = 2, rate = 48000, input = True, output = True, frames_per_buffer = BUFF)
		print("ListenMic - v1.4")
		print()
		i=1
		while i: # i = while 1: ...
			try:
				if i==1: print("\r[*     ] Grabando",end="\r")
				if i==2: print("\r[**    ] Grabando",end="\r")
				if i==3: print("\r[***   ] Grabando",end="\r")
				if i==4: print("\r[ ***  ] Grabando",end="\r")
				if i==5: print("\r[  *** ] Grabando",end="\r")
				if i==6: print("\r[   ***] Grabando",end="\r")
				if i==7: print("\r[    **] Grabando",end="\r")
				if i==1: print("\r[     *] Grabando",end="\r")
				if i>8: i=1

				f.write(f.read(BUFF), BUFF)
				i+=1
			except KeyboardInterrupt: break
		f.close()
		print("\r[  OK  ] Grabacion Terminada.",end="\r")
		input("\nPresione enter para terminar . . .")

if __name__=="__main__": App()
