from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form
        }

        return render(request, 'users/register.html', context)

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!!!')
            return redirect('users:login')

            # The code commented below works only for ModelForm
            # cd = form.save(commit=False)
            # password = cd['password']
            # username = cd['username']
            # user = User.objects.get(username=username)
            # user.set_password(password)
            # cd.save()
        else:
            context = {
                "form": form
            }
            return render(request, 'users/register.html', context)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!!!')
            return redirect('books:list')

        else:
            return render(request, 'users/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out!!!")
        return redirect('landing_page')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # This additional work is undertaken by LoginRequiredMixin
        # if not request.user.is_authenticated:
        #     return redirect('users:login')

        return render(request, 'users/profile.html', {'user': request.user})

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated your data.')
            return redirect('users:profile')

        return render(request, 'users/profile_edit.html', {'form': form})
