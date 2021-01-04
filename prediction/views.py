import base64
import pickle
from datetime import datetime

from PIL import Image

from .forms import *
import arrow as arrow
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm

from django.core.files.storage import FileSystemStorage

from keras.preprocessing import image
import json
import tensorflow as tf
from tensorflow import Graph

from keras.models import load_model
import matplotlib.pyplot as plt
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://skincodeuser:skincodepassword@cluster0.0lzc9.mongodb.net/skincodedb?retryWrites=true&w=majority")
db = cluster["skincodedb"]
collection = db["prediction_prediction"]


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
    count = collection.count_documents({})
    context = {'total_users': total_users, 'count': count}
    return render(request, 'home.html', context)

def image_upload(request):

    context = {'a': 1}
    return render(request, 'image_upload.html', context)


img_height, img_width = 75, 100
with open('./models/sample.json', 'r') as f:
    labelInfo = json.load(f)

labelInfo = json.loads(labelInfo)


model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('./models/mymodel.h5')

from numpy import asarray
from bson import Binary
import io

def predict(request):

    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()

    datetoday = arrow.now().format('YYYY-MM-DD')
    filedate = datetoday

    filePathName = fs.save(filedate, fileObj)
    filePathName = fs.url(filePathName)

    testimage = '.' + filePathName
    img = image.load_img(testimage, target_size=(img_height, img_width))

    x = asarray(img)
    x = x.astype('float32')
    mean, std = x.mean(), x.std()
    x = (x - mean) / std

    x = x.reshape(1, img_height, img_width, 3)
    with model_graph.as_default():
        with tf_session.as_default():
            predi = model.predict(x)

    import numpy as np

    predictedLabel = labelInfo[str(np.argmax(predi))]
    prediction_probability = np.max(predi)

    msg = "Result is: "
    message = "Please look at our recommendations for dermatologists"

    filedate = filedate

    imgByteArr = io.BytesIO()
    image2 = {
        #'data': imgByteArr.getvalue(),
        'date': filedate,
        'label': predictedLabel,
    }
    images = collection.insert_one(image2).inserted_id

    # pil_img = Image.open(io.BytesIO(image3['data']))


    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel, "prediction_probability": prediction_probability, "msg": msg, "message": message, "filedate": filedate}
    return render(request, 'image_upload.html', context)

@login_required(login_url='login')
def view_profile(request):

    import os
    context = {}
    listOfImages = os.listdir('./media/')
    listOfImagesPath = ['./media/' + i for i in listOfImages]
    myArray = []
    for p in collection.find({}):
        myArray.append(p)



    mylist = zip(listOfImagesPath, myArray)

    context["mylist"] = mylist
    #context["listOfImagesPath"] = listOfImagesPath
    return render(request, 'view_profile.html', context)


def about(request):
    return render(request, "about.html")

def system(request):
    return render(request, "system.html")

@login_required(login_url='login')
def doctors(request):
    return render(request, "doctors.html")

def skincancer(request):
    return render(request, "cancer.html")

def cancertypes(request):
    return render(request, "cancertypes.html")