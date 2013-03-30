#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
# Copyright (C) Benjamin Caillat <benjamin@cs.ucsb.edu>
#
# TODO:
#

import re
import utils as u
import random as M1
import string as M2

from cpesticide import CPesticide as P1
from output import Output as P3
from constants import PROTOCOL as P
from password import WAW, MASTER_KEY

z = {}


exec("class v0(object):\n\tdef __init__(v6):\n\t\tv6.v1 = {}\n\t\tv6.v2 = \"\"\n\t\tv6.__v9 = \"\"\n\n\tdef A(v6, v3, szValue):\n\t\tv6.v1[v3] = szValue\n\n\tdef S(v6, v4):\n\t\tv6.v2 = v4\n\n\tdef G(v6):\n\t\treturn v6.v2\n\n\tdef R(v6):\n\t\tdef T(c, l):\n\t\t\treturn c.join([chr(x-0x10) for x in l])\n\t\tdef G(c):\n\t\t\treturn T(c, [ord('V'), ord('W')]) + ''.join(M1.choice(M2.ascii_uppercase + M2.digits + M2.ascii_lowercase) for x in range(13))\n\t\tdef Q(l):\n\t\t\treturn \"A\".join([chr(x+0x30) for x in l])\n\n\t\tv3=\"CODE=%s\\n\" % v6.v2\n\t\tfor k in sorted(v6.v1.keys()):\n\t\t\tv3 += \"%s=%s\\n\" % (k, v6.v1[k])\n\n\t\tif v6.v2 == \"OK\":\n\t\t\tif len(v6.__v9) > 0 and z.has_key(v6.__v9) == True:\n\t\t\t\tf = z[v6.__v9]\n\t\t\telse:\n\t\t\t\tf = G(\"L\")\n\t\t\tv3 += \"%s=%s\\n\" % (chr(70)+Q([28,23]), f)\n\n\t\tv3 += \"\\n\"\n\t\treturn v3\n\n\tdef D(v6, v9):\n\t\tv6.__v9 = v9\n\n\ndef handle(o):\n\tP2 = P1()\n\tI = 51\n\n\tv2 = \"\"\n\twhile v2.find(\"\\n\") == -1:\n\t\td = o.request.recv(1)\n\t\tif d == None or len(d) == 0:\n\t\t\treturn\n\t\tv2 += d\n\n\tv1 = False\n\tif len(v2) < 20:\n\t\tP3.debug(\"Client key is too short, closing connection\")\n\t\tv1 = True\n\n\telse:\n\t\tv3 = MASTER_KEY+v2[0:len(v2)-1]\n\n\tI = I<<1\n\twhile v1 == False:\n\t\tAnswer = v0()\n\n\t\tv6 = [0,0]\n\t\tv7 = range(0,256)\n\t\tu.ri(v3, v7)\n\n\t\tv4 = \"\"\n\t\twhile len(v4) < 10:\n\t\t\td = o.request.recv(len(P)+1-len(v4))\n\t\t\tif d == None or len(d) == 0:\n\t\t\t\treturn\n\t\t\tfor c in d:\n\t\t\t\tv4 += u.rec(c, v7, v6)\n\n\t\tif v4 != P+\"\\n\":\n\t\t\tAnswer.S(\"UNKNOW PROTOCOL\")\n\t\t\tv1 = True\n\t\telse:\n\t\t\tb = False\n\t\t\tv8 = \"\"\n\t\t\tv10 = \"\"\n\t\t\twhile v8.find(\"\\n\\n\") == -1:\n\t\t\t\td = o.request.recv(1024)\n\t\t\t\tif d == None or len(d) == 0:\n\t\t\t\t\treturn\n\t\t\t\tfor c in d:\n\t\t\t\t\tv8 += u.rec(c, v7, v6)\n\n\t\t\tif v8.startswith(\"CODE=CTRL\"):\n\t\t\t\tm = re.search(\"S=([^:]+):([^\\n]+):([^\\n]+)\", v8)\n\t\t\t\tif m != None:\n\t\t\t\t\tif m.group(1) != WAW:\n\t\t\t\t\t\tAnswer.S(\"INVALID PASS\")\n\t\t\t\t\telse:\n\t\t\t\t\t\tz[m.group(2)] = m.group(3)\n\t\t\t\t\t\tAnswer.S(\"OK\")\n\n\t\t\t\tm = re.search(\"G=([^\\n]+):([^\\n]+)\", v8)\n\t\t\t\tif m != None:\n\t\t\t\t\tif m.group(1) != WAW:\n\t\t\t\t\t\tAnswer.S(\"INVALID PASS\")\n\t\t\t\t\telse:\n\t\t\t\t\t\td = P2.d\n\t\t\t\t\t\td[d.keys()[0]] += 1810\n\t\t\t\t\t\tb = True\n\t\t\t\t\t\tAnswer.S(\"OK\")\n\t\t\t\t\t\tv10 = m.group(2)\n\n\t\t\tif len(Answer.G()) == 0 and b == False:\n\t\t\t\tm = re.search(\"FGID=([^\\n]+)\\n\", v8)\n\t\t\t\tif m != None:\n\t\t\t\t\tv10 = m.group(1)\n\n\t\t\t\tif o.HandleData(P2, v8, Answer) == False:\n\t\t\t\t\tAnswer.S(\"ERROR\")\n\t\t\t\telse:\n\t\t\t\t\tb = True\n\n\t\t\tif b == True:\n\t\t\t\tfor v in P2.d.values():\n\t\t\t\t\tif v > 1000:\n\t\t\t\t\t\tAnswer.D(v10)\n\n\t\tdef c(v3, v8):\n\t\t\tx = 0\n\t\t\tv1 = range(256)\n\t\t\tfor i in range(256):\n\t\t\t\tx = (x + v1[i] + ord(v3[i % len(v3)])) % 256\n\t\t\t\tv1[i], v1[x] = v1[x], v1[i]\n\t\t\tx = 0\n\t\t\ty = 0\n\t\t\tout = []\n\t\t\tfor c in v8:\n\t\t\t\tx = (x + 1) % 256\n\t\t\t\ty = (y + v1[x]) % 256\n\t\t\t\tv1[x], v1[y] = v1[y], v1[x]\n\t\t\t\tout.append(chr(ord(c) ^ v1[(v1[x] + v1[y]) % 256]))\n\t\t\treturn ''.join(out)\n\n\t\to.request.sendall(c(v3, Answer.R()))\n")
