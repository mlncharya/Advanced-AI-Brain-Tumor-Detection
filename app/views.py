from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


def register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        email1 = request.POST['mail']
        aage = request.POST['age']
        add = request.POST['add']
        password = request.POST['passw']
        confirmpassword = request.POST['cpassw']
        if password == confirmpassword:
            # Create an instance of the Register model
            a = Register(name=uname, email=email1, password=password, age=aage, address=add)
            a.save()
            msg = "Successfully Registered"
            return render(request, 'login.html', {"msg": msg})
        mssg = "Registration Failed, Try Again"

        return render(request, "register.html", {'msg': mssg})
    return render(request, "register.html")


def logins(request):
    if request.method=='POST':
        email=request.POST['lmail']
        password=request.POST['lpassw']
        d=Register.objects.filter(email=email, password=password).exists()
        print(d)
        print(email)
        print(password)
        if d:
            return redirect(upload)
        else:
            h="login failed"
            return render(request,"login.html",{"msg":h})
    return render(request,"login.html")


def upload(request):
    pathss = os.listdir(r"app\Data\Testing")
    classes = []

    for i in pathss:
        classes.append(i)

    if request.method == 'POST':
        file = request.FILES['hop']
        img = Oil(image=file)
        img.save()
        path = "app/static/saved/" + img.filename()
        path1 = "/static/saved/" + img.filename()
        m=int(request.POST['alg'])
        if m==1:
            models = load_model("app/models/CNN.h5")
            x = image.load_img(path, target_size=(256, 256))

        if m==2:
            models = load_model("app/models/LSTM.h5")
            x = image.load_img(path, target_size=(64, 64))

            
        
        x = image.img_to_array(x)
        x = np.expand_dims(x, axis=0)
        x /= 255
        results = models.predict(x)
        b = np.argmax(results)
        prediction = classes[b]
        return render(request,"result.html",{"res":prediction,"path":path1})

    return render(request, "upload.html") 