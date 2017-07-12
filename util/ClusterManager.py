#! /usr/bin/env python
import sys, glob, os, time, subprocess, threading, pprint
import argparse
from queue import Queue
##xrund -v perl -p -i -n -e 's/\./0/' 'export2/*.txt.bed'         RUNS OK!!!!
##xrund -v  cat 'export2/*.txt.bed' '| grep chrM >$(hostname).$$.log.chrM'


#====================================Resource_Monitor============================================
def Single_Job_Process(job,node):
    pass

def singleton(cls):
    instances = {}
    def _singleton(*args,**kws):
        if cls not in instances:
            instances[cls]=cls(*args,**kws)
        return instances[cls]
    return _singleton

@singleton
class Job_Queue(Queue):

    def __init__(self):
        Queue.__init__(self,1000)
        self.t = threading.Thread(self.process())
        #process the jobs in queue one by one.
        self.t.start()
        self.threadpool=[]
        #store all the threads of processing tasks, when thread.is_alive is False, join the thread.
        self.close_tag=False

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
            j = threading.Thread(Single_Job_Process,job,node)
            self.threadpool.append(j)
            del_task=[]
            for i in range(len(threadpool)):
                if not self.threadpool[i].is_alive():
                    self.threadpool[i].join()
                    del_task.append(i)                   #delete jobs that has been finished
            for i in range(len(del_task)):                  #Need to add a update job status function
                del self.threadpool[del_task[i]-i]
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
#the same cluster can ask for information from this class. This class should be destoried after the last
#person closed his window.
'''
    good_nodes = [x for x in node_info if x[1]>=args.memory and args.x[4]>args.cpu]
    while len(good_nodes)==0:
        echo('No avaliable node with sufficient resource.')
        if not wait: exit(1)
        time.sleep(wait)
        echo('%s, retry getting node info ...' % time.asctime())
        node_info = sorted(cluster_info(nodes), key=operator.itemgetter(4))
        good_nodes = [x for x in node_info if x[1]>=memory and x[4]>cpu]


pprint.pprint(good_nodes, sys.stderr)

ncommand, sleep, command_list, expanded_names = 1, 0.001, [], []

for opt in command:

    filenames = sorted(glob.glob(opt))

    if len(filenames) == 0: command_list.append([opt])
    else:
        echo("Your input %s is epanded to %s" %(opt, filenames) )
        expanded_names = filenames
        command_list.append(filenames)
        ncommand *= len(filenames)


allthreads=[]
for i in xrange(ncommand):
    command, ii = [], i
    for arg in command_list:
        command.append(arg[ii%len(arg)])
        ii /= len(arg)

    command = escape( command )
    commandline = ' '.join(command)


    node, free_mem, n_cpu, cpu_load, idle_cpu = good_nodes[0]
    good_nodes.append( good_nodes[0])
    del good_nodes[0]

    seed = ''
    if( len(expanded_names) > 0 ):
        seed = expanded_names[ i ]
        seed = seed.rsplit('/')[-1]

    echo('')
    print >> sys.stderr, 'Running command %s on %s (free_mem:%dMB, idle_cpu/total_cpu:%.1f/%d)' % (commandline, node,free_mem/1024,idle_cpu,n_cpu)

    mythread = MyThread(node, os.getcwd(), commandline, seed, ptable, external_par)

    mythread.start()

    allthreads.append(mythread)
    time.sleep(sleep)

print >> sys.stderr, "\nAll threads started.............................................................................\n"



import signal
def signal_handler(signal, frame):
    print >> sys.stderr, "Ooops, you pressed ctrl + c"
    raise KeyboardInterrupt

##stupid python thread
##method 1: os.kill( os.getpid() , signal )
##method 2: thread.interrupt_main() from inside child thread
##method 3: sigal.signal call here with raise of exception.
try:                        ##it's interesting that first ctrl+c kills all child threads and second ctrl+c kills the main thread.
    while(True):
        signal.signal(signal.SIGINT, signal_handler)
        for athread in allthreads:
            athread.join(1)
        time.sleep(1)
        if( threading.activeCount() == 1): # 1 for main thread
            all_exit = 0
            for athread in allthreads:
                if ( athread.get_exit_code() != 0 ):
                    print >> sys.stderr, "%s is exiting with code %s. please check seed %s node %s!" %( athread.getName(), athread.exit_code, athread.seed, athread.node)
                    all_exit = 1

            if(all_exit == 0):
                print >> sys.stderr, 'OK. All threads exit with code 0.........................................................................'
            sys.exit(all_exit)

except KeyboardInterrupt:

    for athread in allthreads:
        print >> sys.stderr, "%s: exit code %s. seed %s node %s!" %( athread.getName(), athread.exit_code, athread.seed, athread.node)
        fields = os.popen("grep %s %s" %(athread.seed, ptable) ).readline().rsplit(':')
        node_kill = fields[1]
        pid_kill    = fields[2]
        os.system("ssh %s 'kill -9 %s'" % ( node_kill, pid_kill ) )

    sys.exit(1)
'''
##
##xrund -v cat 'export2/*.txt.bed' '>log.$(hostname).$$.log && echo log.$$.$(hostname).log'
##[deqiangs@selenium RXRa]$ xrund -v perl -p -i -n -e 's/\./0/' 'export2/*.txt.bed'
##XRUND item # -v
##XRUND item # perl
##XRUND item # -p
##XRUND item # -i
##XRUND item # -n
##XRUND item # -e
##XRUND item # s/\./0/
##XRUND item # export2/*.txt.bed
##XRUND# Fri May 14 22:21:11 2010, getting cluster info ...
##XRUND# Running command perl -p -i -n -e '\'s/\\./0/\'' export2/Input_export.txt.bed on selenium002 (free_mem:31692MB, idle_cpu/total_cpu:8.0/8)
##XRUND# Actually the full commandline is : ssh selenium002 'cd /pillar_storage/pillar00/deqiangs/data/RXRa && perl -p -i -n -e '\'s/\\./0/\'' export2/Input_export.txt.bed'
##XRUND# Exit code: 0 from on node selenium002
##on the actual node:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
##deqiangs 18502  0.0  0.0  63796  1216 ?        Ss   21:18   0:00 bash -c cd /pillar_storage/pillar00/deqiangs/data/RXRa && perl -p -i -n -e s/\\./0/ export2/PMWT_315.export.txt.bed
##deqiangs 18523 99.0  0.0  77808  1472 ?        R    21:18   0:00 perl -p -i -n -e s/\./0/ export2/PMWT_315.export.txt.bed
