import re
import hashlib
import sys

def digits2word(numbers):
	words = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
	string = ""
	for number in str(numbers):
		if not number.isnumeric(): continue
		string += words[int(number)]
	return string

def serialNumber(ssid):
	# Eliminate non-essential stuff from ssid

	ssid = re.match("(eircom)?\s?(\d{4}\s?\d{4})", str(ssid), re.IGNORECASE).group(2).replace(" ", "")

	binary = bin(int(ssid, 8)).replace("b", "")

	xor = hex(int(binary, 2) ^ int("0x000fcc", 16))
	serial = int(xor, 16) + int("0x01000000", 16)

	return serial

def WEP(serialNumber):
	serial = digits2word(serialNumber)
	string = serial + "Although your world wonders me, "
	sha1 = hashlib.sha1(string.encode("UTF-8")).hexdigest()
	return sha1[:26]

def main():
	ssid = input("Input your SSID (eircom???? ????): ")

	try:
		serial = serialNumber(ssid)
	except AttributeError:
		print("Invalid format")
		sys.exit(1)

	print()
	print("Serial: " + str(serial))
	key = WEP(serial)
	print("WEP Key: " + key)
	input()

if __name__ == "__main__":
	main()
