#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# DESC:
# Entry point of pesticides-control
#
# TODO:
#

# Standard importations
import sys
import logging
import getopt
import os
import re
import string
import subprocess
import traceback
import socket
import threading
import SocketServer
import random

# Personnal importations
from output import Output
import utils
from cpesticide import CPesticide
from handle import handle,z
from constants import *

# ==============================================================================
#
#   Entry point of pesticides-control
#
# ==============================================================================

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def __init__(self, request, clientaddress, o):
		SocketServer.BaseRequestHandler.__init__(self, request, clientaddress, o)

	def __HandleList(self, Pesticide, dicData, Answer):
		Answer.S("OK")
		d = Pesticide.GetIngredients()
		for szIngredient in sorted(d):
			Answer.A(szIngredient, "%d mg" % d[szIngredient])
		return True


	def __HandleInfo(self, szVersion, szProtocol, szDesc, szStatus, dicData, Answer):
		Answer.S("OK")
		Answer.A("VERSION", szVersion)
		Answer.A("PROTOCOL", szProtocol)
		Answer.A("DESC", szDesc)
		Answer.A("STATUS", szStatus)
		return True

	def __HandleInc(self, Pesticide, dicData, Answer):
		if dicData.has_key("INGREDIENT") == False:
			Output.debug("Missing ingredient")
			return False
		if dicData.has_key("VALUE") == False:
			Output.debug("Missing value")
			return False
		iValue = int(dicData["VALUE"])
		if Pesticide.IncIngredient(dicData["INGREDIENT"], iValue) == False:
			return False
		Answer.S("OK")
		return True

	def __HandleDec(self, Pesticide, dicData, Answer):
		if dicData.has_key("INGREDIENT") == False:
			Output.debug("Missing ingredient")
			return False
		if dicData.has_key("VALUE") == False:
			Output.debug("Missing value")
			return False
		iValue = int(dicData["VALUE"])
		if Pesticide.DecIngredient(dicData["INGREDIENT"], iValue) == False:
			return False
		Answer.S("OK")
		return True

	def HandleData(self, Pesticide, szData, Answer):
		szAnswer = ""
		dicData = {}

		dicData = utils.ParseAnswer(szData)
		if dicData == None:
			return False

		# Analyze command 
		if dicData["CODE"] == "LIST":
			Output.debug("Command LIST received")
			if self.__HandleList(Pesticide, dicData, Answer) == False:
				return False
		elif dicData["CODE"] == "INFO":
			Output.debug("Command INFO received")
			if self.__HandleInfo(VERSION, PROTOCOL, DESC, STATUS, dicData, Answer) == False:
				return False
		elif dicData["CODE"] == "INC":
			Output.debug("Command INC received")
			if self.__HandleInc(Pesticide, dicData, Answer) == False:
				return False
		elif dicData["CODE"] == "DEC":
			Output.debug("Command DEC received")
			if self.__HandleDec(Pesticide, dicData, Answer) == False:
				return False
		else:
			Output.debug("Unknown command \"%s\"" % dicData["CODE"])
			return False

		return True

	def handle(self):
		handle(self)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

OUTPUT_LEVEL=logging.WARNING
LISTEN="0.0.0.0"
PORT=8080
INTERACTIVE=False

# === Read arguments ===========================================================
try:
	opts, args = getopt.getopt(sys.argv[1:], 'l:p:ivh')
except getopt.GetoptError:
	Usage()

for o, a in opts:
	if o == '-l':
		LISTEN = a
	elif o == '-p':
		PORT = int(a)
	elif o == '-i':
		INTERACTIVE=True
	elif o == '-v':
		if OUTPUT_LEVEL == logging.INFO:
			OUTPUT_LEVEL = logging.DEBUG
		elif OUTPUT_LEVEL > 0:
			OUTPUT_LEVEL -= 10
	elif o == "-h":
		Usage()
	else:
		Output.error('Invalid option "%s"' % o)
		Usage(-1)

Output.setLevel(OUTPUT_LEVEL)

Output.debug("Starting server on %s:%s" % (LISTEN, PORT))
Server = ThreadedTCPServer((LISTEN, PORT), ThreadedTCPRequestHandler)
ServerThread = threading.Thread(target=Server.serve_forever)
ServerThread.daemon = True
ServerThread.start()
Output.debug("Server successfully started")
if INTERACTIVE == True:
	while True:
		sys.stdout.write("> ")
		szCmd = sys.stdin.readline().rstrip('\n')
		if len(szCmd) == 0:
			continue
		elif szCmd == "quit":
			break
		else:
			Output.error("Invalid command \"%s\"" % szCmd)

	Output.debug("Shutting down the server")
	Server.shutdown()
else:
	ServerThread.join()

sys.exit(0)
