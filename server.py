from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer #These are parent classes
from urllib.parse import urlparse, parse_qs
from articles_db import ArticlesDB
from users_db import UsersDB
from passlib.hash import bcrypt
from http import cookies #read the doc for this lib
from session_store import SessionStore
import json
import sys

#instantiate the sessionStore class:
gSessionStore = SessionStore() # declare here so it won't be recreate all the time when the code run

class MyRequestHandler(BaseHTTPRequestHandler): #this class will be recreated every request

#======================================COOKIES=============================================
    def loadCookie(self):
        #read the Cookie hear FROM client        
        if "Cookie" in self.headers:
            self.cookie=cookies.SimpleCookie(self.headers["Cookie"])#using http lib
            # print("here is your cookie:"+self.headers["Cookie"])
        else:
            # self.cookie = self.headers["Cookie"] #normal way
            self.cookie = cookies.SimpleCookie()
            # print("No cookie for ya")
        #save for later
    
    def sendCookie(self):
        #send one or more Set-Cookie headers TO client
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSession(self):
        self.loadCookie() # to find cookie data inside self.cookie
        #step 1: check to see if the sessionID is in the cookie, if not =>error
        #if sessionId does exist:
        if "sessionId" in self.cookie:       
            sessionId = self.cookie["sessionId"].value
            print("session is already existed: "+sessionId)  
            #load session data from session store using session ID
            self.sessionData= gSessionStore.getSessionData(sessionId) # it lives as long as a request
            #IF SESSION DATA DOES NOT EXIST - OR EXPIRED:     
            if self.sessionData == None:
                #create new sessionId and create new entry in session store
                sessionId = gSessionStore.createSession()
                self.sessionData= gSessionStore.getSessionData(sessionId) # it lives as long as a request
                #assign the new session ID into the cookie
                self.cookie["sessionId"] = sessionId
        else:
            print("create new session")
            #create new sessionId and create new entry in session store
            sessionId = gSessionStore.createSession()
            self.sessionData= gSessionStore.getSessionData(sessionId) # it lives as long as a request
            #assign the new session ID into the cookie
            self.cookie["sessionId"] = sessionId

    #overwriten method from HTTPRequestHandler
    def end_headers(self):
        self.sendCookie()#send cookie to client first
        self.send_header("Access-Control-Allow-Origin",self.headers["Origin"]) #CORS
        self.send_header("Access-Control-Allow-Credentials","true") #CORS
        BaseHTTPRequestHandler.end_headers(self)#call/hijack the original end_headers()
#=======================================END COOKIES============================================

#=======================================Article handlers========================================

    def handleNotFound(self):        
            self.send_response(404) #success code
            self.send_header("Content-Type","text/plain") # send just text
            self.end_headers()
            self.wfile.write(bytes("Not found.","utf-8"))

    def handle401(self):        
            self.send_response(401) #success code
            self.send_header("Content-Type","text/plain") # send just text
            self.end_headers()
            self.wfile.write(bytes("No Authenciation.","utf-8"))

    def handle422(self):        
            self.send_response(422) #success code
            self.end_headers()

    def handleArticles(self):
        if "userId" not in self.sessionData:
            self.handle401()
            return
        else:
            # self.cookie["title"]="let's have fun"
            self.send_response(200) #success code
            self.send_header("Content-Type","application/json") # contentype as json
            self.end_headers()
            #send data to the client via response body
            db = ArticlesDB()
            allRecords = db.getAllArticles()
            self.wfile.write(bytes(json.dumps(allRecords),"utf-8"))

    def handleRetrieveAnArticle(self,id):
        if "userId" not in self.sessionData:
            self.handle401()
            return
        db = ArticlesDB()
        record = db.getOneArticle(id)
        if record!=None:
            self.send_response(200) #success code
            self.send_header("Content-Type","application/json") # contentype as json
            self.end_headers()
            self.wfile.write(bytes(json.dumps(record),"utf-8"))
        else:
            self.handleNotFound()

    def handleDeleteAnArticle(self,id):        
        if "userId" not in self.sessionData:
            self.handle401()
            return
        db = ArticlesDB()
        record = db.getOneArticle(id)
        if record!=None:
            # DELETE the Cookie here!:
            db.deleteArticle(id)
            self.send_response(200) #success code
            self.end_headers()
        else:
            self.handleNotFound()

    def handleCreateAnArticle(self):#POST function
        if "userId" not in self.sessionData:
            self.handle401()
            return
        #step 1: determine number of bytes to read from the request body
        length= int(self.headers["Content-Length"])
        #step 2: actually read the raw requet body
        request_body = self.rfile.read(length).decode("utf-8")
        #step 3: parse the urlencoded data
        parse_body = parse_qs(request_body)

        #step 4: access and store data
        title = parse_body['title'][0] # if you find the key-error : which mean the client did not send the right data type
        author = parse_body['author'][0] # if you find the key-error : which mean the client did not send the right data type
        code = parse_body['code'][0] # if you find the key-error : which mean the client did not send the right data type
        content = parse_body['content'][0] # if you find the key-error : which mean the client did not send the right data type
        # article = {'title':title,'author':author,'code':code,'content':content}
        #save data to the database:
        db= ArticlesDB()
        # record= article #
        db.createArticle(title,author,code,content)

        #respond to the client when done; no response body needed
        self.send_response(201)
        self.end_headers()

    def handleUpdateAnArticle(self,id):#PUT function
        if "userId" not in self.sessionData:
            self.handle401()
            return
        #TODO: read data from the request and insert a new cookie
        #step 1: determine number of bytes to read from the request body
        length= int(self.headers["Content-Length"])
        
        # article = {'title':title,'author':author,'code':code,'content':content,'id':id}
        #save data to the database:
        db= ArticlesDB()
        # record= article #
        
        record = db.getOneArticle(id)
        if record!=None:
            #step 2: actually read the raw requet body
            request_body = self.rfile.read(length).decode("utf-8")
            #step 3: parse the urlencoded data
            parse_body = parse_qs(request_body)
            #step 4: access and store data
            title = parse_body['title'][0] # if you find the key-error : which mean the client did not send the right data type
            author = parse_body['author'][0] # if you find the key-error : which mean the client did not send the right data type
            code = parse_body['code'][0] # if you find the key-error : which mean the client did not send the right data type
            content = parse_body['content'][0] # if you find the key-error : which mean the client did not send the right data type
            
            db.updateArticle(title,author,code,content,id)

            #respond to the client when done; no response body needed
            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()

    #this is the prefly
    def do_OPTIONS(self):
        self.loadSession()
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods","GET,PUT,POST,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    
    def do_GET(self):
        self.loadSession()
        # print("the request path is: ", self.path)
        path_parts= self.path.split("/")
        collection = path_parts[1]
        if len(path_parts)>2:
            article_id = path_parts[2]
        else:
            article_id=None

        if collection=="articles":
            if article_id:
                self.handleRetrieveAnArticle(article_id)
            else:
                print("handler for articles")
                self.handleArticles()
        else:
            self.handleNotFound()

    def do_POST(self):
        self.loadSession()
        print("the request path is: ", self.path)
        if self.path =="/articles":
            self.handleCreateAnArticle()
        elif self.path =="/users":
            self.handleCreateAUser()
        elif self.path =="/sessions":
            self.handleAuthenticateUser()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.loadSession()
        path_parts= self.path.split("/")
        collection = path_parts[1]
        if len(path_parts)>2:
            member_id = path_parts[2]
        else:
            member_id=None

        if collection=="articles":
            if member_id:
                self.handleDeleteAnArticle(member_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()
          
    def do_PUT(self):
        self.loadSession()
        print("the request path is: ", self.path)
        path_parts= self.path.split("/")
        collection = path_parts[1]
        if len(path_parts)>2:
            article_id = path_parts[2]
        else:
            article_id=None

        if collection=="articles":
            if article_id:
                self.handleUpdateAnArticle(article_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()

#===========================================User=============================================#=======================================AUTHENTICATE============================================
    def handleAuthenticateUser(self):
        length= int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        parse_body = parse_qs(request_body)
        username = parse_body["username"][0]
        password = parse_body["password"][0]
        #1: find user in DB Email
        db = UsersDB()
        user = db.getOneUserByUsername(username)
        #if user Exists:
        if user !=None:
            #2: verify password
            if bcrypt.verify(password,user["password"]):
            #if match:
                #SUCCESS!
                #201 status response                
                self.send_response(201) #success code
                self.end_headers()
                #save user ID into the session data
                self.sessionData["userId"] = user["id"]
            else:
                self.handle401()
        else:     
            self.handle401()

    def handleRetrieveAUser(self,id):
        db = ArticlesDB()
        record = db.getOneUser(id)
        if record!=None:
            self.send_response(200) #success code
            self.send_header("Content-Type","application/json") # contentype as json
            self.end_headers()
            self.wfile.write(bytes(json.dumps(record),"utf-8"))
        else:
            self.handleNotFound()
            print("handleRetrieveAUser")

    def handleCreateAUser(self):#POST function
    #TODO: read data from the request and insert a new cookie
    #step 1: determine number of bytes to read from the request body
        length= int(self.headers["Content-Length"])
        #step 2: actually read the raw requet body
        request_body = self.rfile.read(length).decode("utf-8")
        print("the request body: ", request_body)
        #step 3: parse the urlencoded data
        parse_body = parse_qs(request_body)
        print("the parse body: ", parse_body)
        #step 4: access and store data
        first_name = parse_body['firstname'][0] # if you find the key-error : which mean the client did not send the right data type
        last_name = parse_body['lastname'][0] # if you find the key-error : which mean the client did not send the right data type
        username = parse_body['username'][0] # if you find the key-error : which mean the client did not send the right data type
        password = parse_body['password'][0] # if you find the key-error : which mean the client did not send the right data type
        password = bcrypt.hash(password)
        #save data to the database:
        db= UsersDB()
        #===================================================
        #TODO: check if the username is already created!!!!!
        user = db.getOneUserByUsername(username)
        if user== None:
            #===================================================
            # record= article #
            db.createAUser(first_name,last_name,username,password)
            #respond to the client when done; no response body needed
            self.send_response(201)
            self.end_headers()
        else:
            self.handle422()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass #nothing to see here
    
def run(): # main function

    #create DB tables then disconnect from the DB
    adb= ArticlesDB()
    adb.createArticlesTable()
    udb= UsersDB()
    udb.createUsersTable()
    adb= None
    udb = None

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen=("0.0.0.0", port) #look at all interfaces
    server = ThreadedHTTPServer(listen,MyRequestHandler) # HTTPServer class needs 2 inputs
    # server = HTTPServer(listen,MyRequestHandler) # HTTPServer class needs 2 inputs
    print("the server is running!")
    server.serve_forever()

run()