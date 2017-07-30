from django.shortcuts import render,redirect
from django.http import HttpResponse
from .Test.module import *
from .util.ParseMetaInfo import *
from .util.GetNode import GetNode
from .models import *

# Create your views here.

def checklogin(request):
    if 'login' in request.session:
        if request.session['login']==1:
            return True
    return False

def refresh_basemount(request):
    if not checklogin(request):
        return index(request)
    #base_path = request.session['basemount_path']
    #linux_account = request.session['linux_account']
    #linux_password = request.session['linux_password']
    username = request.session['username']
    try:
        FileSystem.refresh(username)
    except Exception:
        return False
    return True
    

def index(request):
    #cal1()
    #print(cal1())
    #cm=cluster_manager()
    getmetainfo()
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
        try:
            from ClusterManager import cluster_manager,job_queue
        except Exception:
            if username!='root':
                print('error')
                return redirect(index)
            else:
                return render(request,'epivis/set_meta.html',{'nodes':GetNode(),'cache_path':cache_path})#redirect(setting_meta)

        return menu(request)

def get_meta(request):
    print('Get_meta')
    cache_path = request.POST['cache_path']
    nodes = request.POST['nodes']
    SetMeta(cache_path,nodes)
    return redirect(login)


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
    pass
    if not checklogin(request):
        return index(request)
    username=request.session['username']
    return render(request,'epivis/menu.html',{'username':username})
