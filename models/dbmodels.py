import psycopg2
from psycopg2.extras import RealDictCursor
import os
from flask import Flask

# app = Flask(__name__)

class DatabaseAccess:
    def __init__(self):
        if os.getenv('APP_SETTINGS') == "testing":
            self.dbname = "test_db"

        else:
            self.dbname = "stackoverflow-lite"

        try: 
            self.conn = psycopg2.connect(dbname="{}".format(self.dbname), user="postgres", password="1234567890", host="localhost")
            self.conn.autocommit = True
            
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("database Connected")

        except psycopg2.Error:
            print("can not establish a database connection")

    # def dbtest(self):
    #     print ("we got this")


# if __name__ == '__main__':
#     db = DatabaseAccess()
#     db.dbtest()
#     app.run(debug=True)
            