#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

# Standard importations
import logging
import traceback
from logging.handlers import SysLogHandler

# Personnal importations

class COutput(object):
	""" Logger
		Public fields:
		Private fields:
		  - szFormat     = format of messages
		  - logger       = logger
		  - bIsDebugging = flag indicates if we are displaying debug trace
	"""
	def __init__(self):
		self.__szFormat = '[%(levelname)-8s] %(message)s'
		self.__logger = logging.getLogger("air-control")
		self.__logger.setLevel(logging.INFO)
		ch = logging.StreamHandler()
		ch.setFormatter(logging.Formatter(self.__szFormat))
		self.__logger.addHandler(ch)

	def __display(self, iLevel, szMessage):
		try:
			if iLevel >= logging.ERROR:
				print szMessage
			self.__logger.log(iLevel, szMessage)
		except:
			print 'Exception while sending message to logger : %s' % szMessage

	def exception(self, szMessage):
		try:
			self.__logger.log(logging.ERROR, szMessage)
			traceback.print_exc()
		except:
			print 'Exception while sending message to logger : %s' % szMessage

	def error(self, szMessage):
		self.__display(logging.ERROR, szMessage)

	def warning(self, szMessage):
		self.__display(logging.WARNING, szMessage)

	def info(self, szMessage):
		self.__display(logging.INFO, szMessage)

	def debug(self, szMessage):
		self.__display(logging.DEBUG, szMessage)

	def setLevel(self, iLevel):
		self.__logger.setLevel(iLevel)

Output = COutput()


