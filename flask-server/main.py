import cv2
import numpy as np
import os
import pickle
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facialrecognitionapp-e148f-default-rtdb.firebaseio.com/',
    'storageBucket': 'facialrecognitionapp-e148f.appspot.com'
})

cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)

print("Loading encoding file....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, ownerIds = encodeListKnownWithIds
print("Encoding file Completed")
error_message = "none" 

#Function to draw rectangles over the face detected
def draw_rectangles(image, face_locations, names, match_found=False):
    for (top, right, bottom, left), name in zip (face_locations, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if match_found:
            cv2.putText(image, "Match Found", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Function to verify card details using facial recognition and database data
def verify(card_number, cvv):
    #flag variable for retrieving data from database
    counter = 0 
     #for displaying on the frontend
    verification_result = False 
    message = ""

    # Starts capturing images from the frame
    while True:
        success, img = cam.read()
        
        imgSmall = cv2.resize(img, (0,0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
        
        faceCurrentFrame = face_recognition.face_locations(img)
        encodeCurrFrame = face_recognition.face_encodings(img, faceCurrentFrame)

        names = []

        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDistance)
            if matches[matchIndex]:
                match_found=True
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                img = cvzone.cornerRect(img, bbox, rt=0)
                id = ownerIds[matchIndex]
                if counter == 0:
                    counter = 1

                ownerInfo = db.reference(f'Accounts/{id}').get()
                name = str(ownerInfo['name'])
                names.append(name)

        if counter != 0:
            draw_rectangles(img, faceCurrentFrame, names, match_found)
            if counter == 1:
                
                if card_number == str(ownerInfo['card_details']):
                    # for admin to verify the working
                    print("Card Verified")
                    print("Name:", str(ownerInfo['name']))
                    
                    if cvv == str(ownerInfo['cvv']):
                        print("CVV Verified")
                        verification_result = True
                        print(cvv)
                    else:
                        print("CVV Not Verified")
                        message = "CVV is wrong"
                        return False
                else:
                    # Card details do not match
                    print("Card Not Verified")
                    message = "Card is wrong"
                    verification_result = False
                     
                if verification_result:
                    counter += 1
            
        cv2.imshow('Facial ID Verification', img)
        if cv2.waitKey(1) == ord('q'):
            break  # Wait for 1 millisecond
            
    cam.release()
    cv2.destroyAllWindows()     
    print("After verification",success)
    return verification_result, message
    

@app.route('/receive_card_details', methods=['POST'])
def receive_card_details():
    data = request.json
    card_number = data.get('card_number')
    cvv = data.get('cvv') 
    try:
        # Call the verify function
        verification_result, message = verify(card_number, cvv)
        print("Verification result:", verification_result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    else:
        if verification_result: 
            return jsonify({"success": True, "message": "Verification successful"})
        else:
            return jsonify({"success": False, "message": message})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
