import re
import os
from CRC import CRC


def Process(folder):
	total = 0
	if (os.path.exists(folder)):
		for file in os.listdir(folder):
			hash = ""
			try:
				providedHash = re.search("\[([A-Z0-9]{8})\]", file).group(1)
			except AttributeError:
				continue
			if providedHash is None:
				continue

			else:
				total += 1
				print(file, providedHash)
				# Calculate hash
				hash = CRC(os.path.join(folder, file))
				if hash == providedHash:
					print("File name matches CRC32 hash:", file)
				else:
					print("Invalid file: ..." + file[-30:] + ". Calclated hash is", providedHash)
		print("\nFinished:", total, "files processed.")

	else:
		print("Directory does not exist")


if __name__ == "__main__":
	Process("D:/test")