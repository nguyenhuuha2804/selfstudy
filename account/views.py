from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def login_view(request):
    template = 'pages/login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,template)


def register_view(request):
    template='pages/register.html'
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'tài khoản này đã tồn tại')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email đã tồn tại')
                return redirect('register')
            else:
                new_user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                new_user.save()
                messages.info(request,'Đăng ký tài khoản thành công!')
                return redirect('login')
        else:
            messages.info(request,'mật khẩu không đúng...')
            return redirect('register')
        return redirect('home')
    else: 
        return render(request,template)

def logout_view(request):
    auth.logout(request)
    return redirect('home')