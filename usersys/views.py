from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect

from .forms import UserForm, LoginForm


# decorator that checks if user is logged if is redirect to different page
def redirect_authenticated_users(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('already_logged')
        return view_func(request, *args, **kwargs)

    return wrapped_view


@redirect_authenticated_users
def home(request):
    return render(request, 'index.html')


@redirect_authenticated_users
def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'registration_form': form}

    return render(request, 'register.html', context=context)


def already_logged(request):
    return render(request, 'already_logged_in.html')


@redirect_authenticated_users
def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('user_settings')

    context = {'loginform': form}
    return render(request, 'login.html', context=context)


@login_required(login_url='login')
def user_settings(request):
    return render(request, 'user_settings.html')


def user_logout(request):
    auth.logout(request)
    return redirect('home')
