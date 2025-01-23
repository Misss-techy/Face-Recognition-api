# Face Recognition API
This is a Flask-based API that performs face recognition. The API allows you to upload images for facial recognition and will either match the face with an existing user or register a new user if no match is found.

## Endpoints
**1. `/home` GET**

This is a simple endpoint to check if the API is running.

Response:
`{
    "message": "Hello! Face recognition API running.",
    "status": 200
}`

**2. `/face/predict` POST**
   
This endpoint allows you to upload an image for face recognition. The API will compare the uploaded image against stored images in the database and return the ID of the matched user or create a new user if no match is found.

`curl -X POST -F "file=@path_to_image.jpg" http://127.0.0.1:5000/face/predict`

Response: `{
    "data": {
        "id": 1110
    },
    "message": "success",
    "status": 200
}`

## Setup and Running
1. Python 3.x
2. Required Python packages: Flask, numpy, sqlite3, and face_recognition.
3. Install packages by `pip install -r requirements.txt`
4. Run the application `flask run`    

The Flask application will start on http://127.0.0.1:5000/ by default.

## Database
The application uses an SQLite database called Image.db. This database stores the following information:
- Person: The ID of the person (an integer).
- Person_Img: The binary representation of the person's image.
- Face_Encoding: The face encoding (a serialized array) for the person's image.

You can inspect the database schema using any SQLite database viewer.

## Usecases
- **Customer Identification:** Detects and identifies repeat or existing customers and enhance customer experience.
- **Loyalty Integration:** Seamlessly track customer visits and rewards through loyalty programs.
- **Increased Retention:** Build stronger customer relationships with personalized interactions.
- **Public Area Use:** Deploy in high-traffic areas (malls, airports) for tailored services.
- **Security:** Enhance fraud prevention and transaction security through accurate identification.

## Notes
- The face_recognition library is used to perform the face detection and encoding.
- The API currently supports only JPEG, PNG, and JPG image formats.
- New users are assigned an ID that is incremented based on the highest existing ID in the database.
