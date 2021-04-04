from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import requests as r_s

users = get_user_model()
number = [52608088, 0]
aa = ['amir', 'amir', 0, 'amir', 'amir']


#############################################################################
def check(request):
    global number, aa
    number[1] = number[1]+1
    if number[1] <= 2:
        number[0] = 52608088
        return HttpResponse('your try is up please try again and set current email')
    if request.method == "POST":
        code = request.POST.get('code')
        print('code is :', code)
        print('number is:', number[0])
        code = int(code)
        if code == number[0]:
            new = User.objects.create_user(username=aa[0], password=aa[2], email=aa[1])
            new.first_name = aa[3]
            new.last_name = aa[4]
            new.save()
            print('yes')
            return redirect('/home')

    return render(request, "security.html")


#############################################################################

def mail(subject, text, g_mail, sec=None):
    from random import randrange
    if sec is not False:
        numbere = randrange(10000, 100000)
        text = '{} your code is {}'.format(text, numbere)
        send_mail(subject, text, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[g_mail])
        return numbere
    else:
        send_mail(subject, text, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[g_mail])
        return


#############################################################################

def singup(request):
    if request.user.is_authenticated is True:
        return redirect('/home')
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        print(name, lastname, email, password, password2)
        name_info = users.objects.filter(username=username)
        email_info = users.objects.filter(email=email)
        a = {'log_in': 'your email or pass is not ture'}
        if '@gmail.com' not in email or password != password2:
            email = None
            password = None
            return render(request, "login.html", a)
        if name_info.exists():
            a['log_in'] = "your username is exists"
            return render(request, "login.html", a)
        if email_info.exists():
            a['log_in'] = 'your email is exists'
            return render(request, "login.html", a)
        subject = "welcome to the Drlight site"
        text = "به سایت دکتر لایت خوش امدید\n یکی از بهترین سایت ها در زمنیه اسان سازی کارهای مردم\n برای فعال سازی " \
               "اکانت خود کد را در قمست مربوط قرار دهدید باتکشر تیم drlight "
        code = mail(subject=subject, text=text, g_mail=email)
        global number, aa
        number[0] = code
        aa[0] = username
        aa[1] = email
        aa[2] = password
        aa[3] = name
        aa[4] = lastname
        return redirect('/check')
    return render(request, "login.html")


#############################################################################

def home(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated is not True:
        return redirect('/login')

    if request.method == 'POST':
        '''if request.FILES['file']:
            file = request.FILES['file']
            print(file.name)
            print(file.size)
            FS = FileSystemStorage()
            A =FS.save(file.name, file)
            print(FS.url(A))
            return HttpResponse(FS.url(A))'''
        if request.POST.get('link') is not None:
            link = request.POST.get('link')
            file_Link = r_s.get(link)
            from random import randrange
            z = request.POST.get('format')
            x = randrange(12334, 23426356)
            if z is None:
                z = 'zip'
            y = '{}.{}'.format(x, z)
            open('upload_f_ROOT/{}'.format(y), 'wb').write(file_Link.content)
            FS = FileSystemStorage()
            return HttpResponse(FS.url(y))
    return render(request, 'home.html')


#############################################################################

def login_(request):
    if request.user.is_authenticated is True:
        return redirect('/home')
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(username, email, password)

        cheack = authenticate(request, username=username, password=password)
        print(cheack)
        if cheack is not None:
            login(request=request, user=cheack)
            mail("welcome", "به سایت دکتر لایت خوش امدید شما رسما عضو سایت ما شده اید و میتوانید از دانش ما استفاده "
                            "کنید \n با تشکر امیرحسین حسنی روشن طراح سایت", g_mail=email, sec=False)
            return redirect('/home')
        else:
            return HttpResponse("go to the singup http://127.0.0.1:8002/")
    return render(request, "main_login.html")


#############################################################################

def out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
#############################################################################
