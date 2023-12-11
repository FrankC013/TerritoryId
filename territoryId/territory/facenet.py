import torch
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from facenet_pytorch.models.mtcnn import MTCNN

# from .facenet_recognition import FaceRecognition
# from .facenet_register import FaceRegister

from territoryId.territory.facenet_register import FaceRegister
from territoryId.territory.facenet_recognition import FaceRecognition

if __name__ == '__main__':
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    mtcnn = MTCNN(keep_all=True, device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

    # Registrar caras
    # username = "Frank"
    # face_registrar = FaceRegister(mtcnn, resnet)
    # face_registrar.capture_faces(username)

    # Reconocer caras
    face_recognizer = FaceRecognition(mtcnn, resnet)
    face_recognizer.load_known_faces("faces")
    face_recognizer.run_recognition()
