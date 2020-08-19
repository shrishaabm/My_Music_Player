
import mysql.connector
k=mysql.connector.connect(host='localhost',user='root',passwd='tiger',database='music')
cur = k.cursor()


musicdir = "D:/shrishaa/python project/songs/"

import os
fls = os.listdir(musicdir)

for n in fls:
    file = os.path.join(musicdir, n)
    
    cur.execute("insert into musiclist values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(n, file, "NULL", "NULL", "NULL"))
k.commit()
