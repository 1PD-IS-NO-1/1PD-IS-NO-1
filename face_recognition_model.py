import cv2
import numpy as np
import os

class FaceRecognitionModel:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_face_names = []
        self.train_model()  # Train the model when initializing

    def train_model(self):
        faces = []
        labels = []
        self.known_face_names = []  # Reset the list
        for i, filename in enumerate(os.listdir("student_images")):
            if filename.endswith(".jpeg") or filename.endswith(".jpg"):
                image = cv2.imread(f"student_images/{filename}", cv2.IMREAD_GRAYSCALE)
                faces.append(image)
                labels.append(i)
                self.known_face_names.append(os.path.splitext(filename)[0])
        
        if faces:  # Only train if there are faces to train on
            self.recognizer.train(faces, np.array(labels))
            print(f"Model trained with {len(self.known_face_names)} faces")
        else:
            print("No faces found in the student_images directory")

    def recognize_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        recognized_students = []
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            label, confidence = self.recognizer.predict(roi_gray)
            if confidence < 100:  # You may need to adjust this threshold
                recognized_students.append(self.known_face_names[label])
        
        return recognized_students

    def update_model(self):
        self.train_model()  # This will retrain the model with all images in student_images
        print("Face recognition model updated")

    def get_known_faces(self):
        return self.known_face_names