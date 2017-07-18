import subprocess
import os
import paramiko
from .ClusterManager import job_queue
#This class mainly use for managing basemount files
#We still need another level to maintain the metadata. I think we need to use Django to
#save the metadata.
class FileSystem():

    def __init__(self,mountpoint,cwd):
        self._path = mountpoint
        if self._path[-1]!='/':
            self._path+='/'
        self._cwd = cwd
        if self._cwd[-1]!='/':
            self._cwd+='/'
'''
    def Mount(self):
        out = subprocess.call("basemount "+self._path,shell=True)

    def Unmount(self):
        out = subprocess.call("basemount --unmount "+self._path,shell=True)
'''
    def reload(account,password):
        ssh = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname="127.0.0.1",port=22,username=account,password=password)
        s.exec_command("basemount "+self._path)
        s.exec_command("basemount --unmount "+self._path)
        s.close()

    def preset_folder(self,projects):

        #check the permission
        p = subprocess.Popen('mkdir %stest' %self._cwd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        err = p.stderr.readlines()
        if 'Permission denied' in err[0].decode('utf-8'):
            return False #Maybe we could change it to exception later.

        projectlist=os.listdir(self._cwd)
        for project in projects:
            if not project in projectlist:
                os.system('mkdir %s%s' %(self._cwd,project))
            sample_path = self._cwd+project+'/'
            samplelist = os.listdir(sample_path)
            for sample in project:
                if not sample in samplelist:
                    os.system('mkdir %s%s' %(sample_path,sample))

        return True

    def download(self,downloadlist):
        #check whether file have been download
        tasks=[]

        for file in downloadlist:
            project = None
            sample = None
            filename = None
            original_filepath=self._path+'Projects/'+project+'/Samples/'+sample+'/Files/'+filename
            aim_path = _cwd+project+'/'+sample+'/'
            cmd='cp %s %s' %(original_filepath, aim_path)
            job_queue=job_queue()
            job_queue.newJob(cmd,5)
#Then form a job insert into job queue
            #p = subprocess.Popen('cp %s %s' %(original_filepath, aim_path),shell=True,stderr=subprocess.PIPE)
            #tasks.append(p)

        #download files which havn't been download
#We should set a status about file download


    def GetProjects(self):
        #if self._path[-1]!='/':
        #    self._path+='/'
        projects = os.listdir(path+'Projects/')
        dic={}
        for p in projects:
            dic[p]=GetSamples(path+p)
        self._project_info=dic
        return dic
        #return projects list

    @property
    def project_info(self):
        return self._project_info

    def GetSamples(self):
        path =self._path '/Samples/'
        samples = os.listdir(path)
        dic={}
        for s in samples:
            filepath = path+s+'/Files/'
            files = os.listdir(filepath)
            filename_path={}
            for file in files:
                filename_path[file]=filepath+file
            dic[s]=filename_path
        return dic

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,path):
        self._path = path
        self.reload()

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self,cwd):
        self._cwd = cwd
'''
    def reload(self):
        self.unmount()
        self.mount()
'''


if __name__=="__main__":
    print("Test")

