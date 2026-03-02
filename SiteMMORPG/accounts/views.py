from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
from forums.models import Author
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import LoginForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import OneTimeCode
import random
import string
from django.core.mail import send_mail
from django.conf import settings


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # login(request, user)
                # return redirect('posts')
                code = ''.join(random.choices(string.digits, k=5))
                send_mail(
                    subject='Ваш одноразовый код',
                    message=f'Ваш код для входа: {code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                
                OneTimeCode.objects.update_or_create(user=user, defaults={'code': code})
                # Отправляем код пользователю (например, по SMS или email)
                # Для демонстрации просто выведем в консоль
                print(f"Код для {user.username}: {code}")
                # Сохраняем username в сессии для следующего шага
                request.session['preauth_user'] = user.username
                return redirect('enter_code')  # страница ввода кода
            else:
                # Неверные данные
                messages.error(request, 'Неверное имя пользователя или пароль')
            # else:
             
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def enter_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        username = request.session.get('preauth_user')
        if not username:
            messages.error(request, 'Сессия истекла. Пожалуйста, войдите заново.')
            return redirect('login')
        try:
            user = User.objects.get(username=username)
            one_time_code = OneTimeCode.objects.get(user=user, code=code)
            if one_time_code.is_valid():
                login(request, user)
                # Удаляем использованный код
                one_time_code.delete()
                # Очищаем сессию
                del request.session['preauth_user']
                return redirect('posts')  # или куда нужно
            else:
                messages.error(request, 'Код просрочен. Запросите новый.')
                one_time_code.delete()  # удаляем просроченный код
        except (User.DoesNotExist, OneTimeCode.DoesNotExist):
            messages.error(request, 'Неверный код')
        return redirect('enter_code')
    else:
        # GET-запрос — показываем форму ввода кода
        return render(request, 'accounts/enter_code.html') 


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(user=user)

            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')