#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

# Standard importations
import math
import random
import md5

# Personnal importations
from output import Output
import utils
from worldmap import WorldMap
#XXXKEY from airplane_keys import AirplaneKeys
from password import MASTER_KEY

class CAirplane(object):
	def __init__(self, szId, szOrigin, szDestination):
		self.__szId = szId
		self.__szOrigin = szOrigin
		self.__szDestination = szDestination
		self.Ox = WorldMap[szOrigin][0]
		self.Oy = WorldMap[szOrigin][1]
		self.Dx = WorldMap[szDestination][0]
		self.Dy = WorldMap[szDestination][1]
		self.__iFlightLenght = int(math.sqrt((self.Dx-self.Ox) ** 2 + (self.Dy-self.Oy) ** 2))
		self.angle = math.atan(float(abs(self.Dy-self.Oy))/float(abs(self.Dx-self.Ox)))
		i = random.randint(20, self.__iFlightLenght-20)
		j = 1
		if self.Dx < self.Ox: j = -1
		self.Px = int(self.Ox+j*math.cos(self.angle)*i)
		j = 1
		if self.Dy < self.Oy: j = -1
		self.Py = int(self.Oy+j*math.sin(self.angle)*i)
#XXXKEY		self.__szKey = AirplaneKeys["%s-%s" % (szOrigin, szDestination)]
		self.__szKey = md5.new("%s-%s-%s" % (MASTER_KEY, szOrigin, szDestination)).hexdigest()

	def GetKey(self):
		return self.__szKey

	def GetPosition(self):
		return [self.Px, self.Py]

	def SetPosition(self, X, Y):
		iDiff = int(math.sqrt((X-self.Px) ** 2 + (Y-self.Py) ** 2))
		if iDiff > 100:
			Output.debug("Trying to update position of a too big value: %d" % iDiff)
			return False

		Output.debug("Update position of value: %d" % iDiff)
		self.Px = X
		self.Py = Y
		Output.debug("Position of airplane %s is now [%d,%d]" % (self.__szId, self.Px, self.Py))
		angle = math.atan(float(abs(self.Dy-self.Py))/float(abs(self.Dx-self.Px)))
		Output.debug("Angle is %f (was %f)" % (angle, self.angle))
		return True

	def __str__(self):
		return "FLIGHT \"%s\": pos=[%d,%d] orig=\"%s\"([%d,%d]) dest=\"%s\"([%d,%d])" % (self.__szId, self.Px, self.Py, self.__szOrigin, self.Ox, self.Oy, self.__szDestination, self.Dx, self.Dy)


