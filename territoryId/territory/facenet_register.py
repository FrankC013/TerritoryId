import os
import time

from PIL import Image

import cv2


class FaceRegister:
    def __init__(self, mtcnn, resnet, save_folder="faces"):
        self.mtcnn = mtcnn
        self.resnet = resnet
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)

    def capture_faces(self, username, num_images=10, capture_duration=10):
        user_folder = os.path.join(self.save_folder, username)
        os.makedirs(user_folder, exist_ok=True)

        cap = cv2.VideoCapture(0)
        count = 0
        start_time = time.time()
        interval = capture_duration / num_images

        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                break

            elapsed_time = time.time() - start_time
            if elapsed_time > interval * count:
                frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                boxes, _ = self.mtcnn.detect(frame_pil)
                if boxes is not None:
                    for box in boxes:
                        face = frame_pil.crop(box).resize((160, 160))
                        face.save(os.path.join(user_folder, f'{username}{count}.jpg'))
                        count += 1
                        if count >= num_images:
                            break

            remaining_time = capture_duration - elapsed_time
            cv2.putText(frame, f'Time left: {int(remaining_time)}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2, cv2.LINE_AA)

            cv2.imshow("Face Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
