import sqlite3
import numpy as np
import face_recognition as facerecg

#connect to existing image.db file
conn = sqlite3.connect("Image.db")
cur = conn.cursor()

#load & encode image
img_path = input("Enter Image Path to Compare: ")
img = facerecg.load_image_file(img_path)
img_enc = facerecg.face_encodings(img)[0]

#Extract face encoding data from DB
cur.execute("SELECT Face_Encoding FROM ImageDB")
rows = cur.fetchall()
#Extract names from DB
cur.execute("SELECT Person FROM ImageDB")
names = cur.fetchall()

#iterate through both name & encoding
for row,name in zip(rows,names):
    name = "".join(name)
    row = b''.join(row)
    # print (len(row))
    #converting the encoding from DB to numpy array
    db_enc = np.frombuffer(row)
    # print (db_enc)
    #comapiring both images
    match = facerecg.compare_faces([img_enc], db_enc, tolerance=0.5)
    # print (match)
    #0 referes to true
    i=0
    if match[0]:
        print (f"Match Found >>> {name}")
        i=1
        break

if i==0:
    print ("No Match")
print ("PROCESS COMPLETED")
    
