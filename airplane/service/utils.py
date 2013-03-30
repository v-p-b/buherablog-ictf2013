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
import math
import string
import random
from xml.sax import make_parser, handler
from xml.sax._exceptions import *
import binascii

# Personnal importations
from output import Output

DIRPATH_SCRIPT = os.path.dirname(sys.argv[0])

def ParseAnswer(szData):
	# Extract the command
	lstData = szData.split('\n')
	if len(lstData[0]) == 0:
		return None

	# Parse the data
	dicData = {}
	for szLine in lstData:
		if len(szLine) == 0:
			continue
		m = re.search("([^=]+)=(.+)", szLine)
		if m == None:
			Output.debug("Invalid line \"%s\"" % szLine)
			print szData
			return None
		else:
			dicData[m.group(1)] = m.group(2)

	return dicData

def GenRandomString(iSize=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for x in range(iSize))

def GenRandomValues(iSize=20):
	s = ""
	while len(s) < iSize:
		c = chr(random.randint(0, 255))
		if c != '\n':
			s += c
	return s

def ComputeAngle(Xs, Ys, Xd, Yd):
	if Xd == Xs:
		if Yd > Ys:
			return 90
		else:
			return 270
	a = math.atan(float(abs(Yd-Ys))/float(abs(Xd-Xs)))
	if Xd < Xs:
		if Yd > Ys:
			a = math.pi-a
		else:
			a = math.pi+a
	else:
		if Yd < Ys:
			a = 2*math.pi-a

	return a*360/(2*math.pi)

def ComputeSign(d, szKey):
	s = ""
	for k in sorted(d.keys()):
		s += "%s:%s;" %(k, d[k])
	s = "%s%s" % (s, szKey)
	return "%.8x" % (binascii.crc32(s) & 0xffffffff)

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

