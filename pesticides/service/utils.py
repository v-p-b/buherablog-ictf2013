#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

# Standard importations
import sys
import os
import subprocess
import re
import string
import random
import math
from xml.sax import make_parser, handler
from xml.sax._exceptions import *

# Personnal importations
from output import Output

DIRPATH_SCRIPT = os.path.dirname(sys.argv[0])

def ParseAnswer(szData):
	# Extract the command
	lstData = szData.split('\n')
	if len(lstData[0]) == 0:
		return None
	#dicData = {"CODE":lstData[0]}
	#del lstData[0]

	# Parse the data
	dicData = {}
	for szLine in lstData:
		if len(szLine) == 0:
			continue
		m = re.search("([^=]+)=(.+)", szLine)
		if m == None:
			Output.debug("Invalid line \"%s\"" % szLine)
			break
		else:
			dicData[m.group(1)] = m.group(2)

	return dicData

def GenRandomString(iSize=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for x in range(iSize))

# cserélgetjük S tagjait
def ri(szKey, S):
	j=0
	for i in range(0,256):
		j = (j+S[i]+ord(szKey[i%len(szKey)]))%256
		t = S[i]
		S[i] = S[j]
		S[j] = t

def rec(c, S, index):
	i = index[0]
	j = index[1]
	i = (i+1)%256
	j = (j+S[i])%256
	t = S[i]
	S[i] = S[j]
	S[j] = t
	index[0] = i
	index[1] = j
	return chr(S[(S[i]+S[j])%256]^ord(c))


def rea(szKey, szData):
	x = 0
	box = range(256)
	for i in range(256):
		x = (x + box[i] + ord(szKey[i % len(szKey)])) % 256
		box[i], box[x] = box[x], box[i]
	x = 0
	y = 0
	out = []
	for c in szData:
		x = (x + 1) % 256
		y = (y + box[x]) % 256
		box[x], box[y] = box[y], box[x]
		out.append(chr(ord(c) ^ box[(box[x] + box[y]) % 256]))

	return ''.join(out)

def PrintHex(szTitle, szData):
	print "-"*80
	print szTitle
	for i in range(len(szData)):
		sys.stdout.write("%.2x " % ord(szData[i]))
		if ((i+1) % 16) == 0:
			sys.stdout.write("\n")
		sys.stdout.flush()
	print "\n"
	print "-"*80

def ReadTextFile(szFilePath):
	try:
		f = open(szFilePath, "r")
		try:
			return f.read()
		finally:
			f.close()
			Output.debug('File "%s" successfully loaded' % szFilePath)
	except:
		Output.exception('Exception while trying to read file "%s"' % szFilePath)
		return None

