import subprocess
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

def Unmount(path)

if __name__=="__main__"

