__author__ = 'Liam'

import os
import sys
from CRC32 import CRC

def CRC32(directory):
	if not os.path.exists(directory):
		print("Directory doesn't exist.")
		sys.exit(0)

	else:
		files = []
		for file in os.listdir(directory):
			duplicates = False
			print("Scanning", file)
			checksum = CRC(os.path.join(directory, file))

			for fi in files:
				if fi[1] == checksum:
					print("\tDuplicate file:", fi[0])
					duplicates = True
			files.append([file, checksum])

			if duplicates: print()

	print("Processed", len(files), "files")


if __name__ == "__main__":
	if len(sys.argv) == 2: CRC32(sys.argv[1])
	else: print("1 argument expected: Directory")