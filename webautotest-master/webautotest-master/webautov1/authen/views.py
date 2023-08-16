from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from .models import command_db,current_db,main_db
# Create your views here.

def insert(request):
    if(request.user.is_authenticated):
        if(request.method=="POST"):
            p=request.POST['voicedata']
            email=request.user.email
            q=main_db.objects.all()
            emails=[]
            for i in q:
                emails.append(i.email)
            if(email in emails):
                obj=main_db.objects.get(email=email)
                obj.messages+=(p+'$')
                obj.count+=1
                obj.save()
            else:
                obj=main_db.objects.create(email=email,count=1,messages=(p+'$'),current=p)
            q=obj.messages
            q=q.split('$')[:-1]
            cur=q[0]
            obj.current=cur
            obj.save()
            return render(request,'display.html',{'q':q,'cur':cur})


        else:
            email=request.user.email
            obj=main_db.objects.get(email=email)
            if(obj.count!=0):
                arr=obj.messages
                q=arr.split('$')
                q=q[:-1]
                cur=q[0]
                obj.current=cur
                obj.save()
            else:
                cur=1
                obj.current=1
                q=[]
                obj.save()

            return render(request,'display.html',{'q':q,'cur':cur})

    else:
        return render(request,'authen/home.html')


def checker(request):
    if(request.method=='POST'):
        email=request.user.email
        obj=main_db.objects.get(email=email)
        if(obj.count==0):
            cur=1
            obj.messages=''
            obj.save()
            q=[]
            return render(request,'display.html',{'q':q,'cur':cur})
        else:
            obj.count-=1
            if(obj.count==0):
                cur=1
                obj.messages=''
                obj.save()
                q=[]
                return render(request,'display.html',{'q':q,'cur':cur})
            else:
                q=obj.messages
                q=q.split('$')
                q=q[:-1]
                q=q[1:]
                cur=q[0]
                s=''

                for i in q:
                    s+=(i+'$')
                obj.messages=s
                obj.current=cur
                obj.save()
                return render(request,'display.html',{'q':q,'cur':cur})
    else:
        email=request.user.email
        obj=main_db.objects.get(email=email)
        if(obj.count!=0):
            arr=obj.messages
            q=arr.split('$')
            q=q[:-1]
            cur=q[0]
            obj.current=cur
            obj.save()
        else:

            obj.current=1
            q=[]
            cur=obj.current
            obj.save()

        return render(request,'display.html',{'q':q,'cur':cur})










def home(request):
    if(request.user.is_authenticated):
        return render(request,'authen/index.html')
    else:
        return render(request,'authen/home.html')

def profile(request):
    if(request.user.is_authenticated):
        return render(request,'profile.html',{"user":request.user})
    else:
        return render(request,'authen/login.html',{"error_msg":""})
def commands(request):
    if(request.user.is_authenticated):
        return render(request,'commands.html',{"user":request.user})
    else:
        return render(request,'authen/login.html',{"error_msg":""})



def logout(request):
    auth_logout(request)
    return render(request,'authen/login.html')






def register(request):
    if(request.user.is_authenticated):
        return render(request,'authen/index.html')
    if(request.method=='POST'):
        q=User.objects.filter(email=request.POST['email'])
        if(len(q)!=0):
            return render(request,'authen/register.html',{"error_msg":"EMAIL ALREADY EXISTS!"})
        q=User.objects.filter(username=request.POST['uname'])
        if(len(q)!=0):
            return render(request,'authen/register.html',{"error_msg":"USERNAME ALREADY EXISTS!"})

        user=User.objects.create_user(email=request.POST['email'],username=request.POST['uname'],password=request.POST['pass'])

        auth_login(request,user)

        return render(request,'authen/index.html')

    else:
        return render(request,'authen/register.html',{"error_msg":""})


#key--  482457838952539
#pass--  6a75d822af66cdcf1db2e856bb05f54f

def login(request):
    if(request.user.is_authenticated):
        return render(request,'authen/index.html')
    if(request.method=='POST'):
        q=User.objects.filter(email=request.POST['email'])
        if(len(q)==0):
            return render(request,'authen/login.html',{"error_msg":"EMAIL DOESNOT EXIST!"})
        else:
            uname=q[0].username
            user=authenticate(username=uname,password=request.POST['pass'])
        if(user is None):
            return render(request,'authen/login.html',{"error_msg":"INVALID CREDENTIALS!"})

        auth_login(request,user)

        return render(request,'authen/index.html')

    else:
        return render(request,'authen/login.html',{"error_msg":""})
