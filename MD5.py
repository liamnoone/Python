#!/usr/bin/env 
import hashlib

def function():
	md5 = hashlib.md5()
	md5.update("Whoo")
	md5.digest()

	md5.hexdigest()

function()