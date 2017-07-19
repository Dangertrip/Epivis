#! /usr/bin/env python
import sys, glob, os, time, subprocess, threading, pprint
import argparse
from queue import Queue
from Models import Jobs

#====================================Resource_Monitor============================================
def Single_Job_Process(job,node):
    cmd = job.cmd
    fullcmd = "ssh %s '%s'" %(node,cmd)
    job.fullcmd=fullcmd
    p = subprocess.Popen(fullcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    job.out = out
    job.err = err


def singleton(cls):
    instances = {}
    def _singleton(*args,**kws):
        if cls not in instances:
            instances[cls]=cls(*args,**kws)
        return instances[cls]
    return _singleton

@singleton
class Job_Queue(Queue):

    class _job():

        def __init__(self,cmd,priority):
            self.cmd=cmd
            self.priority=priority
            self.status=0
            self.fullcmd="Haven't run yet"
            self.out="Haven't run yet"
            self.err="Haven't run yet"
            '''
            Job Status:
            0: Waiting
            1:Processing
            2:Done
            '''

            @classmethod
            def recordjob(job,updateMark=False):
                if updateMark:
                    pass
                else:
                    self.id = Jobs.id
                    pass
                #store job in self.model
                #import model.job and record all these stuff in job table
                #if updateMark: update else: insert

    def __init__(self,Model):
        Queue.__init__(self,1000)
        self.t = threading.Thread(self.process())
        #process the jobs in queue one by one.
        self.t.start()
        self.threadpool=[]
        self.processing_job_queue=[]
        #store all the threads of processing tasks, when thread.is_alive is False, join the thread.
        self.close_tag=False
        self.model=Model

    def newJob(self,cmd,priority=1):
        job = _job(cmd,priority)
        self.push(job)
        _job.recordjob(job)

    #For each job in job_queue, we select a best node to run the task.
    def process(self,rm):
        while True:
            if self.empty() and self.close_tag: break #In case of closing operation by user
            while self.empty():#Make sure that there is at least one job in queue
                time.sleep(60)#check queue status every 60s

            #Get a usable node and ready to run the job on it.
            job = self.get()
            status,node = rm.GetBestNode()
            while not status:
                time.sleep(300)
                status,node = rm.GetBestNode()

            #Get another thread to run the single job
            MaxThreadPool=8
            while len(threadpool)>MaxThreadPool:
                continue

            j = threading.Thread(Single_Job_Process,job,node)
            self.threadpool.append(j)
            self.processing_job_queue.append(job)
            job.status = 1
            _job.recordjob(job,True)
            j.start()
            del_task=[]
            for i in range(len(threadpool)):
                if not self.threadpool[i].is_alive():
                    self.threadpool[i].join()
                    del_task.append(i)                   #delete jobs that has been finished
            for i in range(len(del_task)):                  #Need to add a update job status function
                del self.threadpool[del_task[i]-i]
                self.processing_job_queue[del_task[i]-i].status=2
                _job.recordjob(self.processing_job_queue[del_task[i]-i],True)
        for tt in self.threadpool:
            tt.join()

    def close():            #In case of shutting down the system manually
        self.close_tag = True
        self.t.join()




@singleton
class Resource_Monitor():

    def __init__(self,nodes=None):
        #Create a new thread and stop it when every user close their window
        self._user_number=1
        self._nodes = nodes
        self._node_info=None
        self.t = threading.Thread(target=self._get_cluster_info)
        self.t.daemon=True
        self.t.start()

#    def close(self):
#        if self.t.is_alive():

    #User number operation
    def getuser(self):
        return self._user_number

    def adduser(self):
        self._user_number+=1

    def dropuser(self):
        self._user_number-=1

    #Nodes setting
    def setNodes(self,nodes):
        self._nodes = nodes
        print(self._nodes)

    def getNodes(self,nodes):
        return self._nodes

    #Cluster information operation
    def _get_cluster_info(self):
        while True:
            self._cluster_info() #Get cluster information every 60s
            time.sleep(60)
            if self._user_number==0:
                break

    def _cluster_info(self): #Get cluster information
        nodes = self._nodes

        #Get all the cpu and memory information through ssh
        proc,node_info={},[]
        mem={}
        for nd in nodes:
            cmd = "ssh %s '%s'" %(nd,'cat /proc/loadavg /proc/meminfo /proc/cpuinfo')
            #print(cmd)
            proc[nd] = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            #mem[nd] = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        time.sleep(0.5)

        #Process the result and extract useful numbers
        for nd in nodes:
            info = proc[nd].stdout.readlines()
            for i in range(len(info)):
                info[i]=info[i].decode('utf-8')
            if any(info):
                node_mem = int(info[2].split()[1])+int(info[3].split()[1])+int(info[4].split()[1])
                node_ncpu = len([x for x in info if 'processor\t:' in x])
                node_load = float(info[0].split()[0])
                node_info.append([nd,node_mem,node_ncpu,node_load,node_ncpu-node_load])
        self._node_info=node_info

    def show_cluster_info(self):#now it's only for the stdout.
        while self._node_info==None:
            pass
        return self._node_info
    #Name   Node_Memory Node_ncpu   Node_load   Node_ncpu-Node_load

    def GetBestNode(self,job):
        good_node_list=[]
        cpu=job.cpu
        mem=job.memory
        chosen_node=None
        status=False
        for node in self._node_info:
            if node[1]>mem and node[-1]>cpu:
                status=True
                chosen_node=node
        return status,chosen_node

import operator
from ParseMetaInfo import getmetainfo

mark,node,cache_path = getmetainfo()
if not mark:
    raise Exception('Error in meta info!')

'''
After checking the mera information, we could get the resource_monitor and job_queue
'''
_cluster_manager = None#Resource_Monitor(node)
_job_queue = None#Job_Queue() #
sys.path.append('../')
#develop a setup page so user can set up the basemount path, nodes, cache_path first.

def cluster_manager():
    return _cluster_manager

def job_queue():
    return _job_queue

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-n','--node',help='',type=int)
    parser.add_argument('-p','--ptable',help='',type=int)
    parser.add_argument('-m','--memory',help='',default=1024*1024)
    parser.add_argument('-c','--cpu',help='',type=float,default=2)
    parser.add_argument('-v','--verbose',action="store_false")
    parser.add_argument('-w','--wait',type=int)
    parser.add_argument('-i','--show',action="store_false")
    parser.add_argument('-x','--external_par',type=int)
    args=parser.parse_args()
    nodes = ['compute-0-0','compute-0-1','compute-0-2','compute-0-3','compute-0-5']#add by yyin for testing
    #echo('%s, getting cluster info ...' % time.asctime())
    rm = Resource_Monitor(nodes)
    #rm.setNodes(nodes)
    print(rm.show_cluster_info())
    #node_info = sorted(cluster_info(nodes), key=operator.itemgetter(1),reverse=True)
    #print(node_info)
    #exit()
#I think I need to change the program to a unstopabble listening class, which could know cpu and memory info
#any time. When people open the website, I should set a class there and make it Singleton. Every account in
#the same cluster can ask for information from this class. This class should be destoried after the last user close his window.
