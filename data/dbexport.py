import csv
import sqlite3

DATABASE = '/home/minsubsim/jeonp/database.db'

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

like = '가짜'
cur.execute('SELECT * FROM ARTICLE WHERE BODY LIKE ?', like)

with open("out.csv", "wb") as csv_file:              # Python 2 version
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cur.description]) # write headers
    csv_writer.writerows(cur)
