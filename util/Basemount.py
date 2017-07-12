import subprocess
import os

class Basemount():

    def __init__(self,path):
        self._path = path
'''
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
'''
    def Mount(self):
        out = subprocess.call("basemount "+self._path,shell=True)

    def Unmount(self):
        out = subprocess.call("basemount --unmount "+self._path,shell=True)

    def GetProjects(self):
        if self._path[-1]!='/':
            self._path+='/'
        projects = os.listdir(path+'Projects/')
        dic={}
        for p in projects:
            dic[p]=GetSamples(path+p)
        return dic
        #return projects list

    def GetSamples(self):
        path =self._path '/Samples/'
        samples = os.listdir(path)
        dic={}
        for s in samples:
            files = os.listdir(path+s+'/Files/')
            dic[s]=files
        return dic

    def getPath(self):
        return self._path

    def setPath(self,path):
        self._path = path

    def reload(self):
        self.unmount()
        self.mount()



if __name__=="__main__":
    print("Test")

