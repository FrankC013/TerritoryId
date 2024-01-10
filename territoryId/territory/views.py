import json
import subprocess

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, CustomLoginForm

import torch
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from facenet_pytorch.models.mtcnn import MTCNN

from .facenet_recognition import FaceRecognition
from .facenet_register import FaceRegister

def face_register(request):
    if request.method == 'POST':
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        mtcnn = MTCNN(keep_all=True, device=device)
        resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

        data = json.loads(request.body)
        username = data.get('username')
        face_registrar = FaceRegister(mtcnn, resnet)
        face_registrar.capture_faces(username)
        command = [
            "./target/release/node-template",
            "--base-path", "/nodes",
            "--chain", "local",
            "--name", "nodeFrank",
            "--validator"
        ]
        subprocess.run(command)
    return JsonResponse({'status': 'success'})

def login_view(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('login_success')
        else:
            messages.error(request, 'The username or password is incorrect')

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Agregar indicador de éxito
            return render(request, 'sign_up.html', {'form': form, 'registration_success': True})
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def success(request):
    if request.method == 'POST':
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        mtcnn = MTCNN(keep_all=True, device=device)
        resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

        face_recognizer = FaceRecognition(mtcnn, resnet)
        face_recognizer.load_known_faces("faces")
        username = request.POST.get('username')
        face_recognizer.run_recognition(username)
        return render(request, 'login_success.html', {'registration_success': True})
    return render(request, 'login_success.html')

@login_required
def user_profile(request):
    # Obtienes el objeto User del usuario actual
    user = request.user

    # Aquí no es necesario buscar un perfil adicional,
    # ya que usaremos los datos directamente del modelo User.

    # Si estás utilizando un formulario para actualizar el perfil,
    # aquí procesarías el formulario y actualizarías el objeto User.
    if request.method == 'POST':
        # Aquí iría la lógica para manejar los datos del formulario, por ejemplo:
        # user.first_name = request.POST['first_name']
        # user.save()
        pass

    # Pasamos el objeto User al contexto para usarlo en el template
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)
