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

"""
    Если у тебя будет много вьюшек лучше создать отдельную папку views
    и раскидать их по файлам.

    По стилю кода +- нормально. Чекни ссылку:
        Чекни https://peps.python.org/pep-0008/
"""


def register(request):
    form = CustomUserCreationForm() # <- A?
    if request.user.is_authenticated:
        return redirect('chat')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST) # <- A?
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

                # Когда создаёшь объект через objects.create его не обязательно сохранять и присваивать переменной
                # если ты не планируешь с ним дальше работать
                UserLogs.objects.create(user=user, dateLoged=datetime.now())
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
                # Когда создаёшь объект через objects.create его не обязательно сохранять и присваивать переменной
                # если ты не планируешь с ним дальше работать
                UserLogs.objects.create(user=user, dateLoged=datetime.now())
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
    if request.method == 'POST':
        form = MessageForm(request.POST) # <- А?
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            form.save()
            return redirect('chat')
    form = MessageForm()  # <- А?
    context = {'form': form}
    return render(request, 'main/main.html', context)


@login_required(login_url='login')
def settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # <- А?
        if form.is_valid():
            form.save()
            return redirect('chat')
    form = ProfileForm()  # <- А?
    logs = UserLogs.objects.filter(user=request.user)
    context = {'form': form, 'logs': logs}
    return render(request, 'main/settings.html', context)


@login_required(login_url='login')
def sendmessage(request):
    text = request.POST['text']
    user = request.user
    # Когда создаёшь объект через objects.create его не обязательно сохранять и присваивать переменной
    # если ты не планируешь с ним дальше работать
    Messages.objects.create(user=user, text=text)
    # <- бесполезная строка
    return HttpResponse('message sent')


class getmessage(View):
    def get(self, request):
        messages_all = Messages.objects.all()  # ?? Get all book objects from the database ??

        messages_serialized_data = []  # ?? to store serialized data ??
        for m in messages_all:
            user_id = User.objects.get(id=m.user_id) # Но это же не user_id а user или нет??)
            username = user_id.username
            profile = Profile.objects.get(user=m.user_id) # Но это же не profile_id а profile или нет??)
            profile_pic_url = profile.profilePic.url # А это ссылка на картинку) Правильней было бы назвать profile_pic_url
            messages_serialized_data.append({
                'id': m.id,
                'user_id': m.user_id,
                'text': m.text,
                'username': username,
                'user_profile': profile_pic_url,
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
    # А может просто Messages.objects.filter(...).delete() ?
    Messages.objects.filter(id=message_id, user=user).delete()
    return HttpResponse('message sent')


@login_required(login_url='login')
def updatemessage(request):
    text = request.POST['text']
    message_id = request.POST['id']
    user = request.user
    # А может просто Messages.objects.get(...).update(...) ?
    Messages.objects.filter(id=message_id, user=user).update(
        textChanged=text,
        changed=True,
        dateChanged=datetime.now(),
    )
    return HttpResponse('message saved')

