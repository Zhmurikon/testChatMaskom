from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Messages, Profile, UserLogs
from django.views import View
from django.contrib.auth.models import User
from datetime import datetime


# Create your views here.


def register(request):
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('chat')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                Profile.objects.create(
                    user=user,
                )
                user_name = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт создан для ' + user_name)
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                )
                login(request, user)
                new_log = UserLogs.objects.create(user=user, dateLoged=datetime.now())
                new_log.save()
                return redirect('settings')

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
                new_log = UserLogs.objects.create(user=user, dateLoged=datetime.now())
                new_log.save()
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
    form = MessageForm()
    context = {'form': form}
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            form.save()
            return redirect('chat')
    return render(request, 'main/index.html', context)


@login_required(login_url='login')
def settings(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    logs = UserLogs.objects.filter(user=request.user)
    context = {'form': form, 'logs': logs}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('chat')
    return render(request, 'main/settings.html', context)


@login_required(login_url='login')
def sendmessage(request):
    text = request.POST['text']
    user = request.user
    new_message = Messages.objects.create(user=user, text=text)
    new_message.save()
    return HttpResponse('message sent')


class getmessage(View):
    def get(self, request):
        messages_all = Messages.objects.all()  # Get all book objects from the database

        messages_serialized_data = []  # to store serialized data
        for m in messages_all:
            user_id = User.objects.get(id=m.user_id)
            username = user_id.username
            profile_id = Profile.objects.get(user=m.user_id)
            profilePic = profile_id.profilePic.url
            messages_serialized_data.append({
                'id': m.id,
                'user_id': m.user_id,
                'text': m.text,
                'username': username,
                'user_profile': profilePic,
                'date_created': m.dateCreated.strftime('%Y-%m-%d %H:%M'),
                'changed': m.changed,
                'dateChanged': m.dateChanged.strftime('%Y-%m-%d %H:%M'),
                'textChanged': m.textChanged,
            })

        data = {
            'messagesList': messages_serialized_data
        }
        return JsonResponse(data)


@login_required(login_url='login')
def deletemessage(request):
    message_id = request.POST['id']
    user = request.user.id
    user_message = Messages.objects.filter(id=message_id, user=user)
    user_message.delete()
    return HttpResponse('message sent')


@login_required(login_url='login')
def updatemessage(request):
    text = request.POST['text']
    message_id = request.POST['id']
    user = request.user
    update_message = Messages.objects.get(id=message_id, user=user)
    update_message.textChanged = text
    update_message.changed = True
    update_message.dateChanged = datetime.now()
    update_message.save()
    return HttpResponse('message saved')

