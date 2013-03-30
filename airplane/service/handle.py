#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

import re
import math
import random as M1
import string as M2

import utils
from output import Output
from cairplane_database import CAirplaneDatabase as C1
from password import WAW


exec("class C0(object):\n\tdef __init__(v6):\n\t\tv6.__v10 = False\n\t\tv6.v1 = {}\n\t\tv6.__v3 = \"\"\n\t\tv6.__v9 = \"\"\n\n\tdef Z(v6, v3):\n\t\tv6.__v3 = v3\n\t\tv6.__v10 = True\n\n\tdef A(v6, v3, szValue):\n\t\tv6.v1[v3] = szValue\n\n\tdef S(v6, v4):\n\t\tv6.v1[\"CODE\"] = v4\n\n\tdef G(v6):\n\t\tif v6.v1.has_key(\"CODE\") == False:\n\t\t\treturn None\n\t\treturn v6.v1[\"CODE\"]\n\n\tdef R(v6):\n\t\tdef T(c, l):\n\t\t\treturn c.join([chr(x-0x10) for x in l])\n\t\tdef G(c):\n\t\t\treturn T(c, [ord('V'), ord('W')]) + ''.join(M1.choice(M2.ascii_uppercase + M2.digits + M2.ascii_lowercase) for x in range(13))\n\t\tdef Q(l):\n\t\t\treturn \"A\".join([chr(x+0x30) for x in l])\n\n\t\tif v6.__v10 == True:\n\t\t\tv6.v1[\"RAND\"] = utils.GenRandomValues(8)\n\t\t\tv6.v1[\"SIGN\"] = utils.ComputeSign(v6.v1, v6.__v3)\n\t\tv3=\"\"\n\t\tfor k in sorted(v6.v1.keys()):\n\t\t\tv3 += \"%s=%s\\n\" % (k, v6.v1[k])\n\n\t\tif v6.v1[\"CODE\"] == \"OK\":\n\t\t\tif len(v6.__v9) > 0 and z.has_key(v6.__v9) == True:\n\t\t\t\tf = z[v6.__v9]\n\t\t\telse:\n\t\t\t\tf = G(\"L\")\n\t\t\tv3 += \"%s=%s\\n\" % (chr(70)+Q([28,23]), f)\n\n\t\tv3 += \"\\n\"\n\t\treturn v3\n\n\tdef D(v6, v9):\n\t\tv6.__v9 = v9\n\nz = {}\ndef handle(o):\n\tR = 50\n\tf = 0.025\n\tv9 = C1()\n\tv9.GenAirplanes()\n\tf = f*4\n\tR = (R+1)<<1\n\twhile True:\n\t\tb = False\n\t\tv8 = \"\"\n\t\tv10=\"\"\n\t\twhile v8.find(\"\\n\\n\") == -1:\n\t\t\td = o.request.recv(1024)\n\t\t\tif d == None or len(d) == 0:\n\t\t\t\treturn\n\t\t\tv8 += d\n\n\t\tv5 = C0()\n\n\t\tif v8.startswith(\"CODE=CTRL\"):\n\t\t\tm = re.search(\"S=([^:]+):([^\\n]+):([^\\n]+)\", v8)\n\t\t\tif m != None:\n\t\t\t\tif m.group(1) != WAW:\n\t\t\t\t\tv5.S(\"INVALID PASS\")\n\t\t\t\telse:\n\t\t\t\t\tz[m.group(2)] = m.group(3)\n\t\t\t\t\tv5.S(\"OK\")\n\n\t\t\tm = re.search(\"G=([^\\n]+):([^\\n]+)\", v8)\n\t\t\tif m != None:\n\t\t\t\tif m.group(1) != WAW:\n\t\t\t\t\tv5.S(\"INVALID PASS\")\n\t\t\t\telse:\n\t\t\t\t\td = v9.GetAirplanes()\n\t\t\t\t\ta = d[d.keys()[0]]\n\t\t\t\t\twhile abs(math.atan(float(abs(a.Dy-a.Py))/float(abs(a.Dx-a.Px))) - a.angle) < f:\n\t\t\t\t\t\ta.Py += 1\n\t\t\t\t\tb = True\n\t\t\t\t\tv5.S(\"OK\")\n\t\t\t\t\tv10 = m.group(2)\n\n\t\tif v5.G() == None and b == False:\n\t\t\tm = re.search(\"FGID=([^\\n]+)\\n\", v8)\n\t\t\tif m != None:\n\t\t\t\tv10 = m.group(1)\n\t\t\tif o.HandleData(v9, v8, v5) == False:\n\t\t\t\tv5.S(\"ERROR\")\n\t\t\telse:\n\t\t\t\tb = True\n\n\t\tif b == True:\n\t\t\tfor a in v9.GetAirplanes().values():\n\t\t\t\tif abs(math.atan(float(abs(a.Dy-a.Py))/float(abs(a.Dx-a.Px))) - a.angle) >= f:\n\t\t\t\t\tv5.D(v10)\n\t\t\t\t\tbreak\n\n\t\to.request.sendall(v5.R())\n\n")
