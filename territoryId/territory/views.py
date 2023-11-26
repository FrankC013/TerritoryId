from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect

from .facenet import FaceRecognition
from .forms import SignUpForm, CustomLoginForm

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
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def success(request):
    if request.method == 'POST':
        fr = FaceRecognition()
        fr.run_recognition()
        return redirect('signup')
    return render(request, 'login_success.html')
