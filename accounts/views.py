from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


def login_view(request):
    context = {}

    if request.method == "POST":
        usr = request.POST.get("username")
        passwd = request.POST.get("password")

        user = authenticate(request, username=usr, password=passwd)
        if(user):
            print("Srutu")
            login(request, user)
            return redirect('/forum')
        else:
            context = { "login_failed" : True}
        
    
    return render(request, 'accounts/login.html', context)


def register_view(request):
    
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login')

    context = {'form':form}

    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/login')

def password_change_view(request):
    form = PasswordChangeForm(request.user)
    
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('/forum')
    
    context = {'form':form}
    return render(request, 'accounts/password_change.html', context)