#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

import random
from output import Output

lstIngredients = [
	"Acephate", 
	"Arsenic", 
	"Bifenthrin", 
	"Boric Acid", 
	"Capsaicin", 
	"Chlorpyrifos", 
	"Chromium", 
	"Copper", 
	"Creosote", 
	"Cyproconazole", 
	"d-Phenothrin", 
	"DEET", 
	"Deltamethrin", 
	"Diazinon", 
	"Dicamba", 
	"Fipronil", 
	"Glyphosate", 
	"Imidacloprid", 
	"Malathion", 
	"Methoprene", 
	"Naphthalene", 
	"Neem Oil", 
	"Permethrin", 
	"Picaridin", 
	"Propiconazole", 
	"Resmethrin", 
	"Zinc", 
]

class CPesticide(object):
	def __init__(self):
		self.d = {}
		for szIngredient in random.sample(lstIngredients, 10):
			self.d[szIngredient] = random.randint(10, 100)

	def GetIngredients(self):
		return self.d

	def IncIngredient(self, szIngredient, iValue):
		if self.d.has_key(szIngredient) == False:
			Output.debug("Ingredient %s not present" % szIngredient)
			return False
		if self.d[szIngredient] + iValue >= 1000:
			Output.debug("Impossible to increment %s of %d mg; Amount would be higher than critical threshold" % (szIngredient, iValue))
			return False

		self.d[szIngredient] += iValue
		Output.debug("Ingredient %s is now at %d mg" % (szIngredient, self.d[szIngredient]))
		return True

	def DecIngredient(self, szIngredient, iValue):
		if self.d.has_key(szIngredient) == False:
			Output.debug("Ingredient %s not present" % szIngredient)
			return False
		if self.d[szIngredient] <= iValue:
			Output.debug("Impossible to decrement %s of %d mg" % (szIngredient, iValue))
			return False

		self.d[szIngredient] -= iValue
		Output.debug("Ingredient %s is now at %d mg" % (szIngredient, self.d[szIngredient]))
		return True

	def __str__(self):
		szString = ""
		for szIngredient in sorted(self.d.keys()):
			szString += "%s = %d mg\n" % (szIngredient, self.d[szIngredient])
		return szString


