from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def watchlater(request):
    if request.user.is_authenticated:
        watch = watch_later.objects.filter(user = request.user)
        

        ids = []
        id1 =[]
        for i in watch:
            ids.append(i.course_id)
            id1.append(i.watch_id)
        
        courses =[]
        # print(id1)
        for j in ids:
            try:
                value = Course.objects.get(id = j)
                # print(value.name)
                courses.append(value)
            except courses.DoesNotExist:
                courses = None
        
        
        return render(request,'cmsapp/watchlater.html',{'courses':courses,'id1':id1})
    else:
        return redirect('login')
def index(request):
    courses = None
    categories = category.objects.all()
    
    categoryID = request.GET.get('category')
    if categoryID:
        courses = Course.get_all_product_by_id(categoryID)
    else:
        courses = Course.objects.all()

    
    if request.method =="POST":
        user = request.user
        course_id = request.POST.get('course_id')
        watch = watch_later.objects.filter(user = user)
        for i in watch:
            if course_id == i.course_id:
                break
        else:

            watchlater = watch_later(user = user,course_id = course_id)
            watchlater.save()
            
        return redirect('home')
        
    
    return render(request,'cmsapp/index.html',{'courses':courses,'categories':categories,'categoryID':categoryID})
@login_required(login_url = 'login')
def course(request,slug):
    try:
        courses = Course.objects.get(slug = slug)
    except courses.DoesNotExist:
        courses = None
    
    lesson_number = request.GET.get('lecture')
    if lesson_number is None:
        lesson_number = 1
 
    try:
        lesson = lessons.objects.get(lesson_number = lesson_number,Course = courses)

    except lessons.DoesNotExist:
        lesson = None

    return render(request,'cmsapp/course.html',{'courses':courses,'lesson':lesson,'lessonnumber':lesson_number})
def signin(request):
    if  not request.user.is_authenticated:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username).first()
            if  user_obj is None:
                messages.success(request,'User not found!!! please signin with correct user')
                return redirect('/login')
            profile_obj = Person.objects.filter(user = user_obj).first()
            if not profile_obj.is_verified:
                messages.success(request,'Profile is not verified! check your email ')
                return redirect('/login')
            user = authenticate(username = username,password= password)
            if user is not None:
                login(request,user)
            else:
                messages.success(request,'Wrong password')
                return redirect('/login')
            return redirect('/')
            

        return render(request,'cmsapp/login.html')
    else:
        return redirect('home')
def user_logout(request):
    logout(request)
    
    return redirect('home')


def register(request):
    if not request.user.is_authenticated:
            
        try:
                
            if request.method =='POST':
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                
                if User.objects.filter(username = username).first():
                    messages.success(request,'User is taken')
                    return redirect('register')
                if User.objects.filter(email = email).first():
                    messages.success(request,'Email is taken')
                    return redirect('register')
                user_obj = User.objects.create_user(username = username,email = email,password=password,first_name = fname,last_name = lname)
                user_obj.save()
                auth_token =  str(uuid.uuid4())
                profile_obj = Person.objects.create(user = user_obj,auth_token = auth_token )
                profile_obj.save()
                currentsite = get_current_site(request) 
                subject = 'Your account need to be verified'
                message  = f'Hello {fname} ! Welcome to sikshyasala ,please verify you account {currentsite.domain}/verify/{auth_token}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject,message,email_from,recipient_list)
                return redirect('/token_send')
        except Exception as e:
            print(e)

            
        return render(request,'cmsapp/register.html')
    else:
        return redirect('home')
def success(request):
    return render(request,'cmsapp/success.html')
def token_send(request):
    return render(request,'cmsapp/tokensend.html')
def verify(request,auth_token):
    try:
        profile_obj = Person.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your account is already verified! Please Sign in')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account is verified')
            return redirect('/login')
            
        else:
            return redirect('/error')
            
    except Exception as e:
        print(e)
def error(request):
    return render(request,'cmsapp/error.html')


def delete_watchlater(request,pk):
    print(pk)
    print(request.user)
    get_watch = watch_later.objects.get(user = request.user,course_id = pk)
    get_watch.delete()
    return redirect('readlater')
    





