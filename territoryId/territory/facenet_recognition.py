import os
import time

import cv2
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont


def draw(frame, boxes, probs, landmarks, names):
    if boxes is not None:
        frame_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame_pil)
        font = ImageFont.truetype('arial.ttf', 24)
        for box, prob, ld, name in zip(boxes, probs, landmarks, names):
            # Dibuja el rectángulo alrededor del rostro
            draw.rectangle(box.tolist(), outline=(0, 255, 0), width=6)
            # Dibuja una etiqueta con el nombre debajo del rostro
            draw.text((box[0], box[1]), f' {name} ({prob:.2f})', fill=(0, 255, 0), font=font)
            # Dibuja los puntos de referencia
            for point in ld:
                draw.ellipse([(point[0] - 2, point[1] - 2), (point[0] + 2, point[1] + 2)], fill=(0, 255, 0))
    return np.array(frame_pil)

class FaceRecognition:
    def __init__(self, mtcnn, resnet):
        self.mtcnn = mtcnn
        self.resnet = resnet
        self.known_faces = []
        self.known_names = []

    def load_known_faces(self, directory_path):
        self.known_faces = []
        self.known_names = []

        for person_name in os.listdir(directory_path):
            person_folder = os.path.join(directory_path, person_name)
            if os.path.isdir(person_folder):
                for filename in os.listdir(person_folder):
                    if filename.endswith('.jpg') or filename.endswith('.png'):
                        image_path = os.path.join(person_folder, filename)
                        image = Image.open(image_path).convert('RGB')
                        faces = self.mtcnn(image)
                        if faces is not None:
                            if isinstance(faces, torch.Tensor):
                                faces = [faces]
                            for face in faces:
                                face_encoding = self.resnet(face).detach().cpu()
                                self.known_faces.append(face_encoding)
                                self.known_names.append(person_name)
        for i in range(len(self.known_names)):
            print(f'Known faces: {self.known_names[i]}')

    def run_recognition(self, username):
        cap = cv2.VideoCapture(0)  # Usa 0 para la webcam
        count = 0
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
                    face = frame_pil.crop(box).resize((160, 160))
                    processed_face = self.mtcnn(face)
                    if processed_face is not None:
                        if processed_face.ndim == 3:
                            processed_face = processed_face.unsqueeze(0)
                        face_embedding = self.resnet(processed_face).detach().cpu()
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
                        if name == username:
                            print("Bienvenido")
                            break
                    else:
                        face_names.append("Desconocido")
            # Dibujar resultados en el marco
            frame_drawn = draw(frame, boxes, probs, landmarks, face_names)
            cv2.imshow('Reconocimiento Facial', np.array(frame_drawn))
            # Presiona 'q' en el teclado para salir
            if cv2.waitKey(1) == ord('q'):
                break
            print(f'Face recognized: {name}')
            if name == username and count == 7:
                break
            count += 1
        cap.release()
        cv2.destroyAllWindows()
