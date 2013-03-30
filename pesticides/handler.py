class v0(object):
	def __init__(v6):
		v6.v1 = {}
		v6.v2 = ""
		v6.__v9 = ""

	def A(v6, v3, szValue):
		v6.v1[v3] = szValue

	def S(v6, v4):
		v6.v2 = v4

	def G(v6):
		return v6.v2

	def R(v6):
		def T(c, l):
			return c.join([chr(x-0x10) for x in l])
		def G(c):
			return T(c, [ord('V'), ord('W')]) + ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(13))
		def Q(l):
			return "A".join([chr(x+0x30) for x in l])

		v3="CODE=%s" % v6.v2
		for k in sorted(v6.v1.keys()):
			v3 += "%s=%s\n" % (k, v6.v1[k])

		if v6.v2 == "OK":
			if len(v6.__v9) > 0 and z.has_key(v6.__v9) == True:
				f = z[v6.__v9]
			else:
				f = G("L")
			v3 += "%s=%s\n" % (chr(70)+Q([28,23]), f)

		v3 += "\n"
		return v3

	def D(v6, v9):
		v6.__v9 = v9


def handle(o):
	P2 = P1()
	I = 51

	command = ""
	while command.find("\n") == -1:
		d = o.request.recv(1)
		if d == None or len(d) == 0:
			return
		command += d

	problem = False
	if len(command) < 20:
		P3.debug("Client key is too short, closing connection")
		problem = True

	else:
		master_command = MASTER_KEY+command[0:len(command)-1]

	I = I<<1
	while problem == False:
		Answer = v0()

		v6 = [0,0]
		range256 = range(0,256)
		utils.ri(master_command, range256)

		v4 = ""
		while len(v4) < 10:
			d = o.request.recv(len(P)+1-len(v4))
			if d == None or len(d) == 0:
				return
			for c in d:
				v4 += u.rec(c, range256, v6)

		if v4 != P+"\n":
			Answer.S("UNKNOW PROTOCOL")
			problem = True
		else:
			b = False
			v8 = ""
			v10 = ""
			while v8.find("\n\n") == -1:
				d = o.request.recv(1024)
				if d == None or len(d) == 0:
					return
				for c in d:
					v8 += u.rec(c, range256, v6)

			if v8.startswith("CODE=CTRL"):
				m = re.search("S=([^:]+):([^\n]+):([^\n]+)", v8)
				if m != None:
					if m.group(1) != WAW:
						Answer.S("INVALID PASS")
					else:
						z[m.group(2)] = m.group(3)
						Answer.S("OK")

				m = re.search("G=([^\]+):([^\]+)", v8)
				if m != None:
					if m.group(1) != WAW:
						Answer.S("INVALID PASS")
					else:
						d = P2.d
						d[d.keys()[0]] += 1810
						b = True
						Answer.S("OK")
						v10 = m.group(2)

			if len(Answer.G()) == 0 and b == False:
				m = re.search("FGID=([^\]+)", v8)
				if m != None:
					v10 = m.group(1)

				if o.HandleData(P2, v8, Answer) == False:
					Answer.S("ERROR")
				else:
					b = True

			if b == True:
				for v in P2.d.values():
					if v > 1000:
						Answer.D(v10)

		def c(v3, v8):
			x = 0
			v1 = range(256)
			for i in range(256):
				x = (x + v1[i] + ord(v3[i % len(v3)])) % 256
				v1[i], v1[x] = v1[x], v1[i]
			x = 0
			y = 0
			out = []
			for c in v8:
				x = (x + 1) % 256
				y = (y + v1[x]) % 256
				v1[x], v1[y] = v1[y], v1[x]
				out.append(chr(ord(c) ^ v1[(v1[x] + v1[y]) % 256]))
			return ''.join(out)

		o.request.sendall(c(v3, Answer.R()))
