import subprocess
import os
import paramiko
#from .ClusterManager import job_queue
from .ParseMetaInfo import getmetainfo
#This class mainly use for managing basemount files
#We still need another level to maintain the metadata. I think we need to use Django to
#save the metadata.
class FileSystem():

    def __init__(self,cwd):
       # self._path = mountpoint
       # if self._path[-1]!='/':
       #     self._path+='/'
        self._cwd = cwd
        if self._cwd[-1]!='/':
            self._cwd+='/'

    def refresh(self,account,password,path):
        pass
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname="127.0.0.1",port=22,username=account,password=password)
        s.exec_command("basemount "+path)
        s.exec_command("basemount --unmount "+path)
        s.close()

    def check_cwd(self):
        #check the permission
        #p = subprocess.Popen('mkdir %stest' %self._cwd,shell=True,stdout=subprocess.PIPE,stderr=    subprocess.PIPE)
        #err = p.stderr.readlines()
        #if 'Permission denied' in err[0].decode('utf-8'):
        #    return False #Maybe we could change it to exception later.
        #return True
        if oct(os.stat(self._cwd).st_mode)[-3:][0]!='7':
            return False
        return True

#{"Projects":[{"name":"projectname","Samples":["name":"samplename","Files":[{"name":"filenam    e","path":"filepath"}]]}]}
    def preset_folder(self,projects):
        if not self.check_cwd():#Now I think the checking operation should be done before system start.
            raise Exception("Please reset a correct cache path!")
        projectlist=set(os.listdir(self._cwd))

        for project in projects["Projects"]:
            pname = project["name"]
            if not pname in projectlist:
                os.system('mkdir %s%s' %(self._cwd,pname))
            sample_path = self._cwd+pname+'/'
            samplelist = set(os.listdir(sample_path))
            for sample in project["Samples"]:
                sname = sample["name"]
                if not sname in samplelist:
                    os.system('mkdir %s%s' %(sample_path,sname))

        #return True

    def download(self,downloadlist,path):
        #check whether file have been download
        tasks=[]

        for file in downloadlist:
            project = None
            sample = None
            filename = None
            original_filepath=path+'Projects/'+project+'/Samples/'+sample+'/Files/'+filename
            aim_path = _cwd+project+'/'+sample+'/'
            if not os.path.isfile(aim_path+filename):
                cmd='cp %s %s' %(original_filepath, aim_path)
    #        job_queue=job_queue()
    #        job_queue.newJob(cmd,5)
#Then form a job insert into job queue
            #p = subprocess.Popen('cp %s %s' %(original_filepath, aim_path),shell=True,stderr=subprocess.PIPE)
            #tasks.append(p)

        #download files which havn't been download
#We should set a status about file download

#{"Projects":[{"name":"projectname","Samples":["name":"samplename","Files":[{"name":"filenam    e","path":"filepath"}]]}]}
    def GetProjects(self,path):
        #if self._path[-1]!='/':
        #    self._path+='/'
        if path[-1]!='/':
            path+='/'
        projects = os.listdir(path+'Projects/')
        for i in range(len(projects)-1,-1,-1):
            if projects[i][0]=='.':
                del projects[i]
        #print(projects)
        dic={}
        dic['Projects']=[]
        path+='Projects/'
        for p in projects:
            project={}
            project['name']=p
            project['Samples']=self.GetSamples(path+p)
            dic['Projects'].append(project)
        self._project_info=dic
        return dic
        #return projects list

    @property
    def project_info(self):
        return self._project_info

#{"Projects":[{"name":"projectname","Samples":["name":"samplename","Files":[{"name":"filenam    e","path":"filepath"}]]}]}
    def GetSamples(self,path):
        path =path+'/Samples/'
        samples = os.listdir(path)
        for i in range(len(samples)-1,-1,-1):
            if samples[i][0]=='.':
                del samples[i]
        ans=[]
        for s in samples:
            onesample={}
            onesample['name']=s
            onesample['Files']=[]
            filepath = path+s+'/Files/'
            files = os.listdir(filepath)
            for i in range(len(files)-1,-1,-1):
                if files[i][0]=='.':
                    del files[i]
            filename_path={}
            for f in files:
                onefile = {}
                onefile['name']=f
                onefile['path']=filepath+f
                onesample['Files'].append(onefile)
            ans.append(onesample)
        return ans

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,path):
        self._path = path
        self.refresh()

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self,cwd):
        self._cwd = cwd

    def check_available(self):
        pass
'''
    def reload(self):
        self.unmount()
        self.mount()
'''
_,_,cwd = getmetainfo()
filesystem = FileSystem(cwd)

def FS():
    return filesystem


if __name__=="__main__":
    #filesystem.refresh()
    p=filesystem.GetProjects('/Users/yyin/github/basespace')
    filesystem.preset_folder(p)

