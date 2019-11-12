from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, redirect

# Create your views here.
def login_view(request):
    template='pages/login.html'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        login(request,user)
        return redirect('home')
    context = {'form':form}
    return render(request,template,context)

def register_view(request):
    template='pages/register.html'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password
        user.save()
        new_user = authenticate(username = user.username, password = password)
        login(request,new_user)
        return redirect('home')
    context={
        'form':form,
    }
    return render(request,template,context)

def logout_view(request):
    logout(request)
    return redirect("/")