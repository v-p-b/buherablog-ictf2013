import socket
from utils import GenRandomString
from myutils import Rc4Crypt,Rc4CryptChar,Rc4InitTable

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

		self._sock.sendall(Rc4Crypt(self._szKey, szData), False)

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

		return szData

Client = CClient("10.13.37.49", 6699, "ca117c284312a3a933255746c2362a70")
Client._OpenConnection()
print Client.SendCommandGetAnswer("LIST")