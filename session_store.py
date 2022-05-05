import os
import base64

class SessionStore:
    #METHOD
    def __init__(self):
        #DATA
        #dictionary of dictionaries
        #keyed by: session ID
        self.sessions={}

    #METHODS:


    def createSessionId(self): # to create a UNIQUE and HARD TO GUESS / UNGUESSABLE
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def createSession(self):
        sessionId= self.createSessionId()
        self.sessions[sessionId]={}
        return sessionId
    
    def getSessionData(self,sessionId):
        if sessionId and self.sessions:
            return self.sessions[sessionId]
        else:
            return None
