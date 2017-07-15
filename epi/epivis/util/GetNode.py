import subprocess

def GetNode():
    out = subprocess.call('qhost',shell=True)
    lines = out.readlines()
    print(lines)

if __name__=="__main__":
    GetNode()
