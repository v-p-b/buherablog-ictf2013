#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# DESC:
# Entry point of air-control
#
# TODO:
#

# Standard importations
import sys
import logging
import getopt
import os
import re
import random
import string
import subprocess
import traceback
import socket
import threading
import SocketServer

# Personnal importations
from output import Output
import utils
from cairplane_database import CAirplaneDatabase
from handle import handle,z

# ==============================================================================
#
#   Entry point of air-control
#
# ==============================================================================

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def __init__(self, request, clientaddress, o):
		SocketServer.BaseRequestHandler.__init__(self, request, clientaddress, o)

	def __HandleList(self, AirplaneDatabase, dicData, Answer):
		Answer.S("OK")
		d = AirplaneDatabase.GetAirplanes()
		for szName in sorted(d.keys()):
			Answer.A(szName, d[szName])
		return True

	def __HandleSetPos(self, AirplaneDatabase, dicData, Answer):
		if dicData.has_key("ID") == False:
			Output.debug("Missing id")
			return False
		if dicData.has_key("POSX") == False:
			Output.debug("Missing posx")
			return False
		if dicData.has_key("POSY") == False:
			Output.debug("Missing posy")
			return False

		Airplane = AirplaneDatabase.GetAirplane(dicData["ID"])
		if Airplane == None:
			return False
		
		if Airplane.SetPosition(int(dicData["POSX"]), int(dicData["POSY"])) == False:
			return False

		Answer.S("OK")
		return True


	def HandleData(self, AirplaneDatabase, szData, Answer):
		szAnswer = ""
		dicData = {}

		dicData = utils.ParseAnswer(szData)
		if dicData == None:
			return False

		# If the request contains an ID, all communication must be signed
		if dicData.has_key("ID") == True:
			Airplane = AirplaneDatabase.GetAirplane(dicData["ID"])
			if Airplane == None:
				return False
		
			# Get the shared key
			szKey = Airplane.GetKey()

			# Activate signature in the answer
			Answer.Z(szKey)
			
			# Check signature in the request
			if dicData.has_key("SIGN") == False:
				Output.debug("Missing signature")
				return False

			szSign = dicData["SIGN"]

			del dicData["SIGN"]
			if utils.ComputeSign(dicData, szKey) != szSign:
				Output.debug("Invalid signature")
				return False

		# Analyze command
		if dicData["CODE"] == "LIST":
			Output.debug("Command LIST received")
			if self.__HandleList(AirplaneDatabase, dicData, Answer) == False:
				return False
		elif dicData["CODE"] == "SETPOS":
			Output.debug("Command SETPOS received")
			if self.__HandleSetPos(AirplaneDatabase, dicData, Answer) == False:
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

