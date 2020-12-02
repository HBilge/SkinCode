from .forms import *
import arrow as arrow
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm

from django.core.files.storage import FileSystemStorage


def registerUser(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account is created. Please sign in!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')
            return render(request, 'login.html')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):

    users = User.objects.all()
    total_users = users.count()


    context = {'total_users': total_users}
    return render(request, 'home.html', context)

def image_upload(request):

    context = {'a': 1}
    return render(request, 'image_upload.html', context)

def predict(request):

    print(request)
    print(request.POST.dict())
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()

    datetoday = arrow.now().format('YYYY-MM-DD')
    filedate = datetoday

    filePathName = fs.save(filedate, fileObj)
    filePathName = fs.url(filePathName)


    context = {'filePathName': filePathName}
    return render(request, 'image_upload.html', context)


