import os
import psycopg2
import psycopg2.extras
import urllib.parse

class UsersDB:
    def __init__(self):        
        ##-changes start here
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor, # this is like the dict_factory()
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        ##-changes stop here
        self.cursor=self.connection.cursor()
        return
        
    def __del__(self):
        self.connection.close()
        
    def createUsersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Users (id SERIAL PRIMARY KEY, first_namme VARCHAR(255), last_name VARCHAR(255), username VARCHAR(255), password VARCHAR(255))")
        self.connection.commit()

    def getAllUsers(self):
        #read from the table
        self.cursor.execute("SELECT * FROM Users")
        users= self.cursor.fetchall()
        return users

    def getOneUser(self, user_id):
        data=[user_id]
        self.cursor.execute("SELECT * FROM Users where id =%s",data)
        user =self.cursor.fetchone()
        return user # might return None if the result is empty

    def getOneUserByUsername(self, username):
        data=[username]
        self.cursor.execute("SELECT * FROM Users where username =%s",data)
        user =self.cursor.fetchone()
        return user # might return None if the result is empty

    def getHashById(self, id):
        data=[id]
        self.cursor.execute("SELECT password FROM Users where id =%s",data)
        user =self.cursor.fetchone()
        return user # might return None if the result is empty

    def createAUser(self,f_name,l_name,usn,psw):        
        # self.cursor.execute("insert into cookies (flavor,size, color,crust) values ('chocolate', 'small', 'chocolate/brown', 'oreo')") #sql injection is a risk#insert from the table
        #data binding to prevent sql injection!
        #Data binding
        data =[f_name,l_name,usn,psw] 
        self.cursor.execute("INSERT INTO Users (first_name,last_name,username,password) values (%s,%s,%s,%s)",data) #sql injection is a risk so dooing this waY IS BETTER
        self.connection.commit()

    def updateUser(self, f_name,l_name,usn,psw,id):
        data =[f_name,l_name,usn,psw,id] 
        self.cursor.execute("UPDATE Users set first_name=%s,last_name=%s, username=%s,password=%s WHERE id=%s",data) #sql injection is a risk so dooing this waY IS BETTER
        self.connection.commit()
        return

    def deleteAUser(self,id):        
        data=[id]
        self.cursor.execute("DELETE FROM Users where id =%s",data)
        self.connection.commit()
        return