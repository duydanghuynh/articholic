# import sqlite3
import os
import psycopg2
import psycopg2.extras
import urllib.parse

# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

class ArticlesDB:
    def __init__(self):        #change here for postgres
        # self.connection=sqlite3.connect("articles.db")
        # self.connection.row_factory = dict_factory
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
        
    def createArticlesTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Articles (id SERIAL PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), code VARCHAR(255), content VARCHAR(255))")
        self.connection.commit()

    def getAllArticles(self):
        #read from the table
        self.cursor.execute("SELECT * FROM Articles")
        cookies= self.cursor.fetchall()
        return cookies

    def getOneArticle(self, cookie_id):
        data=[cookie_id]
        self.cursor.execute("SELECT * FROM Articles where id =%s",data)
        cookie =self.cursor.fetchone()
        return cookie # might return None if the result is empty

    def createArticle(self,title,author,code,content):        
        # self.cursor.execute("insert into cookies (flavor,size, color,crust) values ('chocolate', 'small', 'chocolate/brown', 'oreo')") #sql injection is a risk#insert from the table
        #data binding to prevent sql injection!
        #Data binding
        data =[title,author,code,content] 
        self.cursor.execute("INSERT INTO Articles (title,author,code,content) values (%s,%s,%s,%s)",data) #sql injection is a risk so dooing this waY IS BETTER
        self.connection.commit()

    def updateArticle(self, title, author, code, content, article_id):
        data =[title, author, code, content, article_id] 
        self.cursor.execute("update Articles set title=%s,author=%s, code=%s,content=%s WHERE id=%s",data) #sql injection is a risk so dooing this waY IS BETTER
        self.connection.commit()
        return

    def deleteArticle(self,id):        
        data=[id]
        self.cursor.execute("DELETE FROM Articles where id =%s",data)
        self.connection.commit()
        return