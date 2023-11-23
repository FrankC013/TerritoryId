# Importing the necessary libraries for using FaceNet with MTCNN in PyTorch
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import cv2
from PIL import Image, ImageDraw
import numpy as np

# Helper function to draw bounding boxes and add names
def draw(frame, boxes, probs, landmarks, names):
    frame_draw = frame.copy()
    frame_pil = Image.fromarray(frame)

    # Comprueba si 'boxes' es None antes de iterar
    if boxes is not None:
        draw = ImageDraw.Draw(frame_pil)
        for box, prob, ld, name in zip(boxes, probs, landmarks, names):
            # Dibuja el rectángulo alrededor del rostro
            draw.rectangle(box.tolist(), outline=(0, 255, 0), width=6)

            # Dibuja una etiqueta con el nombre debajo del rostro
            draw.text((box[0], box[1]), f'{name} ({prob:.2f})', fill=(0, 255, 0))

            # Dibuja los puntos de referencia
            for point in ld:
                draw.ellipse([(point[0] - 2, point[1] - 2), (point[0] + 2, point[1] + 2)], fill=(0, 255, 0))

    return np.array(frame_pil)

# Main class for Face Recognition
class FaceRecognition:
    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

        # Load known faces (this part should be customized to load your known faces)
        self.known_faces = []
        self.known_names = []

        # Example of loading known faces
        # for image_path in known_face_paths:
        #     image = Image.open(image_path)
        #     face_encoding = self.resnet(self.mtcnn(image).unsqueeze(0)).detach().cpu()
        #     self.known_faces.append(face_encoding)
        #     self.known_names.append('Name')

    def run_recognition(self):
        cap = cv2.VideoCapture(0)  # Usa 0 para la webcam

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convertir a imagen PIL
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Detectar rostros
            boxes, probs, landmarks = self.mtcnn.detect(frame_pil, landmarks=True)

            # Predecir nombres para los rostros detectados
            face_names = []
            if boxes is not None:
                for box in boxes:
                    # Extraer el rostro
                    face = frame_pil.crop(box).resize((160, 160))

                    # Asegurarse de que el rostro no sea None
                    if self.mtcnn(face) is not None:
                        # Calcular embedding (vector característico)
                        face_embedding = self.resnet(self.mtcnn(face)).detach().cpu()

                        # Comparar el rostro con rostros conocidos
                        distances = [torch.norm(e - face_embedding) for e in self.known_faces]
                        min_distance = min(distances) if distances else None
                        name = self.known_names[
                            distances.index(min_distance)] if min_distance and min_distance < 0.6 else "Desconocido"
                        face_names.append(name)
                    else:
                        face_names.append("Desconocido")

            # Dibujar resultados en el marco
            frame_drawn = draw(frame, boxes, probs, landmarks, face_names)
            cv2.imshow('Reconocimiento Facial', np.array(frame_drawn))

            # Presiona 'q' en el teclado para salir
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
