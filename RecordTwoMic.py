import pyaudio, sys, threading, time

def getId(channel):
	info = p.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')

	print("List of input devices available")
	for i in range(0, numdevices):
		if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
			print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

	print()
	i = input("Please write the input device id: ")

	try: i = int(i)
	except:
		print("ValueError: Incorrect parameter.")
		exit()

	print("Use the input device '" + str(i) + "' for channel " + channel + ".")

	return i

p       = pyaudio.PyAudio()
i1      = getId("R")
i2      = getId("L")
RATE    = 96000
BUFF    = 1024 * 16
FORMAT  = pyaudio.paInt16
Exit    = False
Starter = threading.Event()
frames1 = []
frames2 = []

def Record(i, frames):
	Starter.wait()

	stream = p.open(
		format             = FORMAT,
		channels           = 1,
		rate               = RATE,
		input              = True,
		frames_per_buffer  = BUFF,
		input_device_index = i,
	)

	while not Exit:
		frames.append(stream.read(BUFF))

print()
print("Press Ctrl + C to stop record.")
print("Recording...", end = "")
sys.stdout.flush()

threading.Thread(daemon = True, target = Record, args = (i1, frames1)).start()
threading.Thread(daemon = True, target = Record, args = (i2, frames2)).start()
time.sleep(0.1)
Starter.set()

try:
	while 1: time.sleep(1)
except KeyboardInterrupt: print("OK\nSaving...", end = "")
finally: Exit = True

with open("OUT R.wav", "wb") as O1, \
     open("OUT L.wav", "wb") as O2:
	O1.writelines(frames1)
	O2.writelines(frames2)

print("OK")