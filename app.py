from flask import Flask, jsonify
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
    data = {
            'status': 200,
            'message': "Hello! Face recognition API running.",
        }
    return jsonify(data), 200

@app.route("/face/predict", methods=['POST'])
def facerecog():

    if 'file' not in request.files:
        data = {
            'status': 400,
            'message': "No file uploaded."
        }
        return jsonify(data), 400

    #load image
    image = request.files['file']

    if image.mimetype not in ['image/jpeg', 'image/png', 'image/jpg']:
        data = {
            'status': 400,
            'message': "Invalid file type. Only image files are allowed."
        }
        return jsonify(data), 400
    
    #converts img to binary
    img_binary = image.read()

    #establish connection
    conn = sqlite3.connect("Image.db")
    cur = conn.cursor()

    #encode image from the request
    img = facerecg.load_image_file(image)
    img_enc = facerecg.face_encodings(img)[0]

    print(f"File uploaded: {image.filename}")

    #Extract face encoding data from DB
    cur.execute("SELECT Face_Encoding FROM ImageDB")
    rows = cur.fetchall()

    #Extract names from DB
    cur.execute("SELECT Person FROM ImageDB")
    pid = cur.fetchall()

    user = -1

    #iterate through both name & encoding
    for row, person_id in zip(rows, pid):
        name = person_id[0]
        row = b''.join(row)

        #converting the encoding from DB to numpy array
        db_enc = np.frombuffer(row)

        #comapiring both images
        match = facerecg.compare_faces([img_enc], db_enc, tolerance=0.5)

        if match[0]:
            print (f"Match Found >>> {name}")
            user = name
            break

    if user == -1:
        # Create a new user ID
        cur.execute("SELECT MAX(Person) From ImageDB;")
        num = cur.fetchall()
        newUser = num[0][0] + 1 if num[0] is not None else 1
        user = newUser
        print(f'newUser >>> {newUser}')

        #load and encode the image file
        face = facerecg.load_image_file(image)
        face_encoding = facerecg.face_encodings(face)[0]

        # Insert new user into the database
        cur.execute("""
            INSERT INTO ImageDB (Person, Person_Img, Face_Encoding)
            VALUES (?, ?, ?)""", (newUser, img_binary, face_encoding) )
        conn.commit()
        cur.close()   

    data = {
        'status': 200,
        'message': "success",
        'data': {
            'id': user,
        }
    }
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(port=2020)