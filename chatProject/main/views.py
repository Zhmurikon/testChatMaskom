from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('chat')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт создан для ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'main/register.html', context)


def login_user(request):
    form = CustomAuthenticationForm()
    context = {'form': form}
    if request.user.is_authenticated:
        return redirect('chat')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('chat')
            else:
                messages.info(request, 'Неверный логин или пароль')
                return render(request, 'main/login.html', context)

        return render(request, 'main/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    return render(request, 'main/index.html')