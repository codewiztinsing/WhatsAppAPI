from django.shortcuts import render, redirect
from chat.services.accounts_form import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
       
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.filter(username=username)
                print(user,"user found here")
            except User.DoesNotExist as e:
                raise e
            print(user," user")
            if not user:
                 return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
            if user:
               
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)
