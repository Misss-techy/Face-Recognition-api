import os
import sqlite3
import face_recognition as facerecg

#making a sql file
conn = sqlite3.connect("Image.db")
#cursor to enter commands in sql 
cur = conn.cursor()

#create sql table
cur.executescript("""
    CREATE TABLE IF NOT EXISTS ImageDB(
        Person TEXT,
        Person_Img BLOB,
        Face_Encoding TEXT
    );
""")

print ("Created SQL file")

#def to conv image file to binary
def convert_binary(file):
    with open(file,"rb") as img_read:
        img = img_read.read()
        return img

print ("Label the Images properly")
#input folder path, checks the folder for .jpg file
path = input("Folder Path: ")
print ("Scanning for image files")

for files in os.listdir(path):
    if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".jpeg"):
        print (f"Encoding {files}")
        #extract the name of file
        name = files.split(".")[0]
        # print (name)
        #extract the path of img file
        file_path = os.path.join(path,files)
        # print(file_path)
        #converts img to binary
        img_binary = convert_binary(file_path)
        # print(img_binary)
        # #load the image file
        face = facerecg.load_image_file(file_path)
        # #encoding the image file
        face_encoding = facerecg.face_encodings(face)[0]
        # print (type(face_encoding))

        #entering values in SQL
        cur.execute("""
            INSERT INTO ImageDB (Person, Person_Img, Face_Encoding)
            VALUES (?, ?, ?)""", (name, img_binary, face_encoding) )

#writing all the values in DB
conn.commit()
cur.close()
print("Suceffully created Image DB")
