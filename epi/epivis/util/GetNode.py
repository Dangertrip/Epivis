import subprocess

'''
Return all the nodes' name as a string slice from qhost command.
Ignore all nodes info if 'ARCH' attribute of nodes is '-'
'''
def GetNode():
    out = subprocess.Popen('qhost',shell=True,stdout=subprocess.PIPE)
    s=out.stdout.readlines()[3:]
#    lines = out.readlines()
#    print(out)
    #lines = s.decode('utf-8').split('\n')[3:]
    nodes=[]
    for line in s:
        t = line.decode('utf-8').strip().split()
        #print(t)
        if t[1]!='-':
            nodes.append(t[0])
    return(nodes)

if __name__=="__main__":
    print(GetNode())
