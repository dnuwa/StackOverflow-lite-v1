import psycopg2
from psycopg2.extras import RealDictCursor
import os
from flask import Flask

app = Flask(__name__)


class DatabaseAccess:
    def __init__(self):
        if os.getenv('APP_SETTINGS') == "testing":
            self.dbname = "test_db"

        else:
            self.dbname = "stackoverflow-lite"

        try:
            self.conn = psycopg2.connect(dbname="{}".format(
                self.dbname), user="postgres", password="1234567890", host="localhost")
            self.conn.autocommit = True

            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("database Connected")

        except psycopg2.Error:
            print("can not establish a database connection")

    def create_table_subscribers(self):
        sql_query = "CREATE TABLE IF NOT EXISTS subscribers(user_id serial PRIMARY KEY, display_name varchar(100) NOT NULL, email varchar(100) NOT NULL, password varchar(100) NOT NULL)"
        self.cursor.execute(sql_query)
        print('table created')

    def add_new_subscriber(self, display_name, email, password):
        query = "INSERT INTO subscribers (display_name, email, password) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (display_name, email, password))

    def query_all_subscribers(self):
        query = "SELECT * FROM subscribers"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(rows)
        return rows

    def no_name_duplicates(self, display_name):
        query = "SELECT * FROM subscribers WHERE display_name = %s"
        self.cursor.execute(query, (display_name, ))
        rows = self.cursor.fetchall()
        print(rows)
        return rows

    def no_email_duplicates(self, email):
        query = "SELECT * FROM subscribers WHERE email = %s"
        self.cursor.execute(query, (email, ))
        rows = self.cursor.fetchall()
        #print (rows)
        return rows

    def create_table_questions(self):
        sql_query = "CREATE TABLE IF NOT EXISTS questions(qn_id serial PRIMARY KEY, user_id varchar(100) NOT NULL, question varchar(1000) NOT NULL)"
        self.cursor.execute(sql_query)

    def post_a_question(self, user_id, question):
        sql_query = "INSERT INTO questions (user_id, question) VALUES (%s, %s)"
        self.cursor.execute(sql_query, (user_id, question,))

    def retrieve_all(self):
        dbquery = "SELECT * FROM questions"
        self.cursor.execute(dbquery)
        data = self.cursor.fetchall()
        return data

    def get_qn_by_id(self, qn_id):
        qnquery = "SELECT * FROM questions WHERE qn_id = %s"
        self.cursor.execute(qnquery, (qn_id, ))
        data = self.cursor.fetchall()
        print (data)
        return data

    def delete_question(self, qn_id):
        deletion_query = "DELETE FROM questions WHERE qn_id = %s"
        self.cursor.execute(deletion_query, (qn_id, ))

    def create_table_answer(self):
        sql_query = "CREATE TABLE IF NOT EXISTS answers(ans_id serial PRIMARY KEY, qn_id varchar(100) NOT NULL, user_id varchar(100) NOT NULL, answer varchar(200) NOT NULL, ans_state varchar(20))"
        self.cursor.execute(sql_query)

    def post_answer(self, qn_id, user_id, ans):
        ans_query = "INSERT INTO answers (qn_id, user_id, answer) VALUES (%s, %s, %s)"
        self.cursor.execute(ans_query, (qn_id, user_id, ans))

    def get_all_answers(self):
        get_all_query = "SELECT * FROM answers"
        self.cursor.execute(get_all_query)
        result = self.cursor.fetchall()
        print (result)
        return result



if __name__ == '__main__':
    db = DatabaseAccess()
    db.get_all_answers()
    # db.no_email_duplicates("danile.nuwa@gmail.com")
    app.run(debug=True)
