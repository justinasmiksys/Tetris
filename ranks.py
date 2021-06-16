import sqlite3
import os


class Ranks():

    def __init__(self, game):
        self.create_database()
        self.items = self.get_data()

    def create_database(self):

        if not os.path.exists('rankings.db'):

            conn = sqlite3.connect('rankings.db')
            c = conn.cursor()

            c.execute("""CREATE TABLE best_scores (
                    name text,
                    score integer
                    )""")

            conn.commit()
            conn.close()

    def get_data(self):

        try:
            conn = sqlite3.connect('rankings.db')
            c = conn.cursor()
            c.execute("SELECT * FROM best_scores ORDER BY score DESC")
            items = c.fetchall()
            conn.commit()
            conn.close()
        except:
            print('Database error')

        return items

    def insert_score(self, score):
        #score is tuple ('name', score)
        try:
            conn = sqlite3.connect('rankings.db')
            c = conn.cursor()
            c.execute("INSERT INTO best_scores VALUES (?,?)", score)
            conn.commit()
            conn.close()
        except:
            print('Database error')
