from django.shortcuts import render,redirect
from django.http import HttpResponse
from .Test.module import *
from .util.ParseMetaInfo import *
from .util.GetNode import GetNode
from .models import *
from .util.Basemount import FS

# Create your views here.

def checklogin(request):
    if 'login' in request.session:
        if request.session['login']==1:
            return True
    return False

def refresh_basemount(request):
    if not checklogin(request):
        return index(request)
    filesystem = FS()
#account password path
    username = request.session['username']
    info = User.objects.filter(username = username)[0]
    account = info.username_linux
    password = info.password_linux
    path = info.basemount_point
    #print('Before return')
    #filesystem.refresh(account,password,path)
    #filesystem.GetProjects(path)
    try:
        filesystem.refresh(account,password,path)
    except Exception:
        return False
    return redirect('/epivis/menu')
    

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
    account=User.objects.filter(username = username, password=password)
    if len(account)!=1:
        request.session['login']=3
        return redirect('/epivis')
    else:
        request.session['login']=1
        request.session['username']=username
        try:
            FS().check_available()
        except Exception as e:
            print(e)
            if username!='root':
                print('error')
                return redirect('/epivis')
            else:
                return render(request,'epivis/set_meta.html',{'nodes':GetNode(),'cache_path':cache_path})#redirect(setting_meta)

        return redirect('/epivis/menu')

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
    if not checklogin(request):
        return index(request)
    username=request.session['username']
    return render(request,'epivis/menu.html',{'username':username})

def download_files(request):
    pass

def file_detail(request):
    #Here we should pass the fileid using url
    fileid=0
    f = File.objects.get(id=fileid)
    sample = f.sampleid
    project = sample.projectid
    return render(request,'epivis/file_detail.html',{'project':project.name \
            ,'sample':sample.name,'filename':f.name,'mate':f.mate,'feature':f.feature})
    #return Project,Sample,filename,mate,feature


def show_files_page(request):
    if not checklogin(request):
        return index(request)
    username = request.session['username']
    return render(request,'epivis/show_files.html',{'username':username})


#CHANGE JSON FILE FORMAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_files_info(request):
#Get file information from sql and form json for javascript
    if not checklogin(request):
        return index(request)
    username = request.session['username']
    info = User.objects.filter(username = username)[0]
    #account = info.username_linux
    #password = info.password_linux
    path = info.basemount_point
    filesystem = FS()
    filesinfo = filesystem.GetProjects(path)#json
    #{Projects name:{Samples name:{filename:path}}}
    #Now it should be changed into:
    #{"Projects":[{"name":"projectname","Samples":["name":"samplename","Files":[{"name":"filename","path":"filepath"}]]}]}
    return filesinfo


