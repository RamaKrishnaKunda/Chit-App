from django.views import View
from django.shortcuts import redirect, render
from chit_app.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chit_app:chitlist')
        form = LoginForm()
        return render(request = request, template_name='login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request = request,
                                username = form.cleaned_data['username'],
                                password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('chit_app:chitlist')
            else:
                return redirect('chit_app:login')

def Logout(request):
    logout(request)
    return redirect('chit_app:firstpage')

class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request=request, template_name='signup.html', context={'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            user = authenticate(request,
                                username = form.cleaned_data['username'],
                                password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('chit_app:chitlist')
            else:
                return redirect('chit_app:firstpage')