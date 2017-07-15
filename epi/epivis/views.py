from django.shortcuts import render,redirect
from django.http import HttpResponse
from .Test.module import *
from .util.ParseMetaInfo import *

# Create your views here.

def checklogin(request):
    if 'login' in request.session:
        if request.session['login']==1:
            return True
    return False

def index(request):
    #cal1()
    #print(cal1())
    #cm=cluster_manager()
    getmetainfo('1.txt')
    #jq=job_queue()
    #if cm==None: redirect('/epivis/settings') 
    name=''
    returnstring=''
    if 'login' in request.session:
        if not checklogin(request):
            returnstring = 'Wrong username or wrong password!'
            request.session.pop('login')
        else:
            menu(request)
    return render(request,'epivis/index.html',{'returnstring':returnstring})

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    account=User.object.filter(username = username, password=password)
    if len(account)!=1:
        request.session['login']=3
        return index(request)
    else:
        request.session['login']=1
        request.session['username']=username
        #full_info,info = getmetainfo()
        if username=='root':
            pass#Set metainfo when metainfo is not enouth to run the system
                #If metainfo is completed, run redirect(menu)
        else:
            pass #Set personal info when personal info is not setup. If it's completed, redirect(menu)
        #if account.basemount_point=='-' and account.cache_path=='-'
        return menu(request)


    #User.objects.filter()
    #query = #get user information
    #if #No user has this username and password:
    #    request.session['login']=3
    #    return index(request)
    #else:
    #    request.session['login']=1
    #    request.session['username']=username
    #    return index(request)


def menu(request):
    if not checklogin(request):
        return index(request)
    username=request.session['username']
    return render(request,'epivis/menu.html',{'username':username})
