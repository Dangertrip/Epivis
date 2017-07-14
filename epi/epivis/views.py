from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def checklogin(request):
    if 'login' in request.session:
        if request.session['login']==1:
            return True
    return False

def index(request):
    name=''
    returnstring=''
    if 'login' in request.session:
        if not checklogin(request):
            returnstring = 'Wrong username or wrong password!'
            if request.session['login'] == 2:
                returnstring = 'Please login first!'
            request.session.pop('login')
        else:
            username = request.session['username']
    return render(request,'epivis/index.html',{'login':checklogin(request),'returnstring':returnstring, 'name': username})

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    account=User.object.filter(username = username, password=password)
    if len(account)!=1:
        request.session['login']=3
        return index(request)
    else:
        request.session['username']=username
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
