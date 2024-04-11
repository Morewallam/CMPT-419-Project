import face_recognition
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from constants import EnemyType


class DectectModel():
    def __init__(self):
        # make the model
        self.model = None
        self.emotion_labels = ['angry', 'disgust', 'fear',
                               'happy', 'sad', 'surprise', 'neutral']
        self.face_pos = (0, 0, 1, 1)
        self.face_img = None
        self.current_prediction: EnemyType | None = None

    def load_model(self, modelpath):
        self.model = load_model(modelpath)

    def predict(self):
        prediction = self.model.predict(self.face_img, verbose=0)
        emotion = self.emotion_labels[np.argmax(prediction)]
        if emotion == 'disgust' or emotion == 'fear':
            emotion = 'angry'
        elif emotion == 'neutral':
            self.current_prediction = None
            return None
        self.current_prediction = EnemyType(emotion)
        return self.current_prediction

    def find_face(self, frame):
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        for top, right, bottom, left in face_locations:
            self.face_pos = (left, top, right, bottom)
        self.get_face_img_for_model(frame)

    def get_face_img_for_model(self, image):
        face_img = image[self.face_pos[1]:self.face_pos[3],
                         self.face_pos[0]:self.face_pos[2]]
        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        resized_face_img = cv2.resize(gray_face, (48, 48))
        normalized_face_img = resized_face_img / 255.0
        self.face_img = np.reshape(normalized_face_img, (1, 48, 48, 1))

    def draw_rec_with_label(self, frame):
        cv2.rectangle(frame, (self.face_pos[0], self.face_pos[1]),
                      (self.face_pos[2], self.face_pos[3]), (0, 0, 255), 5)
        return frame
