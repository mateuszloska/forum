from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from forum.models import UserProfile


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
        um = get_user_model()
        usrn = form.cleaned_data['username']
        form.save()

        #creating a user profile
        new_user=um.objects.get(username = usrn)
        print(new_user)
        UserProfile.objects.create(user = new_user)
        print(UserProfile.objects.all())
        print("HAli HALOoo")
        
        
        return redirect('/login')

    context = {'form':form}

    return render(request, 'accounts/register.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required
def password_change_view(request):
    form = PasswordChangeForm(request.user)
    
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()

            return redirect('/forum')
    
    context = {'form':form}
    return render(request, 'accounts/password_change.html', context)