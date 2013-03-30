
=== Description

The AutoServ DLF-17500 is the last generation of automation server.
It allows a fully automated preparation of chemical by mixing different ingredients.

=== Remote administration
The AutoServ DLF-17500 can be administrated remotely and the whole industrial process fully controlled: status can be check, composition of the mix can be changed,...
The protocol used to connect to server is a customized version of MODBUS over TCP/IP.
It relies on a simple request/answer mechanism. The following gives a quick overview of the protocol, in case you would need to write your own client

The structure of a request is the following:
<PROTOCOL>\n
CODE=<COMMAND>\n
<OPT>=<VAL>\n
<OPT>=<VAL>\n
\n

The structure of an answer is:
CODE=<CODE>\n
<OPT>=<VAL>\n
<OPT>=<VAL>\n
\n

For example, if the client sends:
MODBUS-v3\n
CODE=LIST\n
\n

The server will send back the current composition:
CODE=OK\n
Acephate=92 mg\n
Chlorpyrifos=17 mg\n
Chromium=15 mg\n
Cyproconazole=65 mg\n
Deltamethrin=87 mg\n
Dicamba=92 mg\n
Glyphosate=46 mg\n
Malathion=48 mg\n
Neem Oil=90 mg\n
Zinc=72 mg\n
\n

Another example, to increase the amount of an ingredient:
MODBUS-v3\n
CODE=INC\n
INGREDIENT=Bifenthrin\n
VALUE=71\n
\n

And the server will send back:
CODE=OK\n
\n

The following gives a list of allowed commands and their options:
- LIST: list the current composition
  no options
- INC: increment the amount of one ingredient
  INGREDIENT: <name of the ingredient to increment>
  VALUE: <value to increment the amount of>
- DEC: decrement the amount of one ingredient
  INGREDIENT: <name of the ingredient to decrement>
  VALUE: <value to decrement the amount of>
- INFO: return a list of parameters of the server. Use this information to check that the server is compliant with your client
  no options

=== Security considerations
The AutoServ DLF-17500 integrate several security mechanisms that makes it the most secure automated controler on the market.
The security mechanisms take place on two level: the protocol and the logic.

On the logic level, when a INC command is received, the controler will check that the requested increase will not make the amount higher than 1000mg. This would obvisouly be a mistake that could damage some equipment.

On the protocol level, the MODBUS-v3 use the very secure rc4 algorithm to authenticate and encrypt all communications.
The client and the controller have a shared secret; when the client want to connect to the server, it will first generate a random key and send it in clear to the server. The purpose of this key is only to make every encryption key unique.
Both the client and the server will then use the following key to encrypt all communication with rc4: shared_key || random_key whith || the concatenation operator.

When the server receive an encrypted packet, it will first decrypt it and check that the decrypted data starts with the correct procotol version. If not, either because the client uses an unappropriate protocol or because it uses a wrong key, the server sends back an error message and close the connection.

The following Python class is an example of code to open and close a new channel.
Some function are not implemented, but their names are pretty explicit.

class CClient(object):
	def __init__(self, szIp, iPort, szMasterKey):
		self._szIp = szIp
		self._iPort = iPort
		self._szMasterKey = szMasterKey
		self._sock = None
		self._szKey = ""

	def _OpenConnection(self):
		# Open connection
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sock.connect((self._szIp, self._iPort))

		self.__szClientKey = GenRandomString(40)
		self._szKey = self._szMasterKey+self.__szClientKey

		# Send client part of the key
		self._sock.sendall(self.__szClientKey+"\n")
		return True

	def _CloseConnection(self):
		self._sock.close()
		return True

	def SendCommandGetAnswer(self, szCommand, dicRequest={}):
		szData = "MODBUS-v3\nCODE=%s\n" % (szCommand)
		for k in dicRequest.keys():
			szData += "%s=%s\n" % (k, dicRequest[k])
		szData += "\n"

		sock.sendall(Rc4Crypt(self._szKey, szData), False)

		# Init rc4 to receive data
		index = [0,0]
		S = range(0,256)
		Rc4InitTable(self._szKey, S)

		# Receive the data
		szData = ""
		while szData.find("\n\n") == -1:
			d = self._sock.recv(1024)
			if d == None or len(d) == 0:
				return None
			for c in d:
				szData += Rc4CryptChar(c, S, index)
				print

		return szData

Client = CClient(IP, PORT, MASTER_KEY)
print Client.SendCommandGetAnswer("LIST")













