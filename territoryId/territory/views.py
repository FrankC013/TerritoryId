from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .facenet import FaceRecognition

@csrf_exempt  # Solo para pruebas, en producción maneja CSRF de manera segura
def login_view(request):
    if request.method == 'POST':
        # Aquí se ejecutaría el código de reconocimiento facial
        fr = FaceRecognition()
        fr.run_recognition()
        # Redirigir a la página de signup después de ejecutar el script
        return redirect('signup')
    return render(request, 'login.html')  # Nombre de tu template de login

def sign_up_view(request):
    return render(request, 'sign_up.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            login(request, user)
            return redirect('some-view')
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

