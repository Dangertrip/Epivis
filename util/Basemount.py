import subprocess
import os

def GetPath():
    out = subprocess.call("basemount",shell=True)
    if not "From:" in out:
        raise Exception("Haven't set basemount properly. You should set basemount properly and add it in to $PATH in ~/.bashrc or ~/.bash_profile")
    t = out.strip().split('\n')
    pos=0
    for i in range(len(t)):
        if "From:" in t[i]:
            pos=i
            break
    return t[pos+1].strip()
#Get the mount folder's postion

def Mount(path):
    out = subprocess.call("basemount "+path,shell=True)

def Unmount(path):
    out = subprocess.call("basemount --unmount "+path,shell=True)

def GetProjects(path):
    if path[-1]!='/':
        path+='/'
    projects = os.listdir(path+'Projects/')
    dic={}
    for p in projects:
        dic[p]=GetSamples(path+p)
    return dic
#return projects list

def GetSamples(path):
    path += '/Samples/'
    samples = os.listdir(path)
    dic={}
    for s in samples:
        files = os.listdir(path+s+'/Files/')
        dic[s]=files
    return dic




if __name__=="__main__":
    print("Test")

