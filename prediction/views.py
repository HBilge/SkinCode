from .forms import *
import arrow as arrow
from django.shortcuts import render, redirect
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
import boto3
from botocore.client import Config


def predict(request):

    fileObj = request.FILES.get('filePath', None)
    fs = FileSystemStorage()

    datetoday = arrow.now().format('YYYY-MM-DD')
    filedate = datetoday

    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)

    testimage = '.' + filePathName
    img = image.load_img(testimage, target_size=(img_height, img_width))

    img2 = open(testimage,'rb')

    AWS_ACCESS_KEY_ID = 'AKIAV2CCWSUXN2IHDHDR'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'skincode'
    S3_BASE_URL = "https://skincode.s3.eu-central-1.amazonaws.com/"
    AWS_S3_FILE_OVERWRITE = False

    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )

    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key = fileObj.name , Body=img2)

    url = f"{S3_BASE_URL}{fileObj.name}"
    request.session["url"] = url

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

    image2 = {
        'date': filedate,
        'label': predictedLabel,
        'url': url,
    }
    images = collection.insert_one(image2).inserted_id
    context = {'url':url, 'predictedLabel': predictedLabel, "prediction_probability": prediction_probability, "msg": msg, "message": message, "filedate": filedate}

    return render(request, 'image_upload.html', context)

@login_required(login_url='login')
def view_profile(request):

    context = {}
    images = []
    for p in collection.find({}):
        images.append(p)

    context["images"] = images
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
