from os import walk
from sys import argv
from json import load
from os import makedirs
from os.path import dirname, exists
from urllib.request import urlopen
from Maj.Sh import ProgressBar

def getPathAsset(hash): return hash[:2] + "/" + hash

def downloadAsset(hash, PathSave = "assets/objects/"):
	for i in range(4):
		try:
			I = urlopen("https://resources.download.minecraft.net/" + getPathAsset(hash))
			makedirs("assets/objects/" + hash[:2], exist_ok = True)
			with open(PathSave + getPathAsset(hash) , "wb") as O: O.write(I.read())
			return True
		except Exception as e:
			print("  Reintento #" + str(i + 1) + "...")
	return False

if __name__ == "__main__":
	if not argv[1:]: exit()

	with open(argv[1]) as I: JSON = load(I)["objects"]
	PB = ProgressBar(len(JSON))
	for Path2, D in JSON.items():
		hash = D["hash"]
		print("Intentando descargar asset " + hash + "...", end="")
		if exists("assets/objects/" + hash[:2] + "/" + hash):
			print(" ok, usando copia local.")
			PB.step()
			continue
		if downloadAsset(hash): print(" ok.")
		else: print(" fail.")
		PB.step()