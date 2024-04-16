'''
Code that we first used to get the face dectection up and running
'''
import cv2
import face_recognition
from tensorflow.keras.models import load_model
import numpy as np

model = load_model('best_model-3.h5')
# emotion_labels = ['Angry', 'Happy', 'Sad', 'Surprise', 'Neutral','','']

emotion_labels = ['Angry', 'Disgust', 'Fear',
                  'Happy', 'Sad', 'Surprise', 'Neutral']

video_capture = cv2.VideoCapture(0)

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0
skip_frames = 5

last_top = 0
last_bottom = 1
last_left = 0
last_right = 1

while True:
    ret, frame = video_capture.read()
    if frame_count % skip_frames == 0:
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        for top, right, bottom, left in face_locations:
            last_top = top
            last_bottom = bottom
            last_left = left
            last_right = right

    # Get the face image from points
    face_img = frame[last_top:last_bottom, last_left:last_right]

    # Make into gray scale image
    gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    # resize the image for our model
    resized_face_img = cv2.resize(gray_face, (48, 48))
    normalized_face_img = resized_face_img / 255.0
    reshaped_face_img = np.reshape(normalized_face_img, (1, 48, 48, 1))

    # Plug into model and get result
    emotion_prediction = model.predict(reshaped_face_img)
    emotion = emotion_labels[np.argmax(emotion_prediction)]
    if emotion == 'Disgust' or emotion == 'Fear':
        emotion = 'Angry'
    elif emotion == 'Neutral':
        emotion = ''
    # emotion = "cool"

    cv2.rectangle(frame, (last_left, last_top),
                  (last_right, last_bottom), (0, 0, 255), 2)
    cv2.putText(frame, emotion, (last_left, last_top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_count += 1

video_capture.release()
cv2.destroyAllWindows()
