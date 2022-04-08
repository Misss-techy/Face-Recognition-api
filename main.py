from flask import Flask
from flask import request
import sqlite3
import numpy as np
import face_recognition as facerecg

app = Flask(__name__)

#def to conv image file to binary
def convert_binary(file):
    with open(file,"rb") as img_read:
        img = img_read.read()
        return img

@app.route("/home")
def home():
    return "Face recog API running"

@app.route("/face/predict", methods=['POST'])
def facerecog():
    conn = sqlite3.connect("Image.db")
    cur = conn.cursor()

    #load & encode image
    # img_path = input("Enter Image Path to Compare: ")
    image = request.files['file']
    # facerecg.load_image_file(img_path)
    img = facerecg.load_image_file(image)
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
        user = ""
        i=0
        if match[0]:
            print (f"Match Found >>> {name}")
            user = name
            i=1
            break
    if i==0:
        user="Unknown"

    if user == "Unknown":
            cur.execute("SELECT MAX(Person) From ImageDB;")
            num = cur.fetchall()
            userid = num[0]
            for item in userid:
                str = item
            i = int(str)
            i=i+1
            # name = str(i)
        # if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".jpeg"):
            # print (f"Encoding {files}")
            #extract the name of file
            # name = files.split(".")[0]
            # print (name)
            #extract the path of img file
            # file_path = os.path.join(path,files)
            # print(file_path)
            #converts img to binary
            img_binary = image.read()
            #convert_binary(image)
            # print(img_binary)
            # #load the image file
            face = facerecg.load_image_file(image)
            # #encoding the image file
            face_encoding = facerecg.face_encodings(face)[0]
            # print (type(face_encoding))

            #entering values in SQL
            cur.execute("""
               INSERT INTO ImageDB (Person, Person_Img, Face_Encoding)
               VALUES (?, ?, ?)""", (i, img_binary, face_encoding) )

            #writing all the values in DB
            conn.commit()
            cur.close()        
        
    return user

    # if user == "Unknown":
    #     conn = sqlite3.connect("Image.db")
        


if __name__ == '__main__':
    app.run(port=2020)