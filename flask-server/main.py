import cv2
import os
import pickle
import numpy as np
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
cam.set(3, 640)
cam.set(4, 480)

print("Loading encoding file....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, ownerIds = encodeListKnownWithIds
print("Encoding file Completed")


def draw_rectangles(image, face_locations):
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)


# Function to verify card details using facial recognition and database data
def verify(card_number, cvv):
    counter = 0
    verification_result = False  

    while True:
        success, img = cam.read()

        imgSmall = cv2.resize(img, (0,0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

        faceCurrentFrame = face_recognition.face_locations(img)
        encodeCurrFrame = face_recognition.face_encodings(img, faceCurrentFrame)

        draw_rectangles(img, faceCurrentFrame)

        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDistance)
            if matches[matchIndex]:
                # y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                # bbox = 55+x1, 162+y1, x2-x1, y2-y1
                # img = cvzone.cornerRect(img, bbox, rt=0)
                id = ownerIds[matchIndex]
                if counter == 0:
                    counter = 1

                
        if counter != 0:
            if counter == 1:
                ownerInfo = db.reference(f'Accounts/{id}').get()
                if card_number == str(ownerInfo['card_details']):
                    print("Card Verified")
                    print("Name:", str(ownerInfo['name']))

                else:
                    print("Card Not Verified")
                    return False
                
                if cvv == str(ownerInfo['cvv']):
                    print("CVV Verified")
                    verification_result = True
                    print(cvv)
                else:
                    print("CVV Not Verified")
                counter += 1
              
            cv2.putText(img, str(ownerInfo['bank']), (1006, 550), 
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.putText(img, str(id), (1006, 493), 
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.putText(img, str(ownerInfo['name']), (808, 445), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
            
        cv2.imshow('Facial ID Verification', img)
        if cv2.waitKey(1) == ord('q'):
            break  # Wait for 1 millisecond

    cam.release()
    cv2.destroyAllWindows()    
    return verification_result
    

@app.route('/receive_card_details', methods=['POST'])
def receive_card_details():
    data = request.json
    card_number = data.get('card_number')
    cvv = data.get('cvv') 
    try:
        # Call the verify function
        verification_result = verify(card_number, cvv)
        print("Verification result:", verification_result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    else:
        if verification_result:
            return jsonify({"success": True, "message": "Verification successful"})
        else:
            return jsonify({"success": False, "message": "Verification failed"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
