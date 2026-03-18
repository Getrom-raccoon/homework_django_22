from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class UserRegistrationView(CreateView):
    """Контроллер регистрации пользователя"""

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка приветственного письма после успешной регистрации"""
        response = super().form_valid(form)

        subject = 'Добро пожаловать в Skystore!'
        message = f'Здравствуйте, {self.object.email}!\n\nСпасибо за регистрацию в нашем магазине Skystore. Мы рады приветствовать вас среди наших покупателей!\n\nС уважением, команда Skystore'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.object.email]

        send_mail(subject, message, from_email, recipient_list)

        return response


class UserLoginView(LoginView):
    """Контроллер авторизации пользователя"""

    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('home')