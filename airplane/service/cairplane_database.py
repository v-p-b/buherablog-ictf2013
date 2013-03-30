#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

# Standard importations
import sys
import random

# Personnal importations
from output import Output
import utils
from cairplane import CAirplane
from worldmap import WorldMap

class CAirplaneDatabase(object):
	def __init__(self):
		self.__iCounter = 1
		self.__dicAirplanes = {}

	def GenAirplanes(self):
		iNbAirplanes = random.randint(10,15)
		i = 0
		Output.debug("Generating %d airplanes" % iNbAirplanes)
		lstCityNames = sorted(WorldMap.keys())
		while i < iNbAirplanes:
			szOrigin = random.choice(lstCityNames)
			j = random.randint(0, len(lstCityNames)-1)
			k = 0
			while k < len(lstCityNames):
				szDestination = lstCityNames[(j+k) % len(lstCityNames)]
				iDistance = (WorldMap[szDestination][0] - WorldMap[szOrigin][0])**2 + (WorldMap[szDestination][1] - WorldMap[szOrigin][1])**2
				if iDistance >= 100000 and (abs(WorldMap[szDestination][0] - WorldMap[szOrigin][0]) > 100):
					break
				k += 1

			if k < len(lstCityNames):
				szId = "A_%.4d" % random.randint(10*i, 10*i+9)
				self.__dicAirplanes[szId] = CAirplane(szId, szOrigin, szDestination)
				i += 1

		return True

	def GetAirplanes(self):
		return self.__dicAirplanes

	def GetAirplane(self, szId):
		if self.__dicAirplanes.has_key(szId) == False:
			Output.error("Unknow airplane %s" % szId)
			return None
		return self.__dicAirplanes[szId]



