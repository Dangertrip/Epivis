from ClusterManager import Job_Queue, Resource_Manager
import os,time
from Queue import Queue
import Threading
def Process_Job(jq,rm):
    q=Queue(1000)
    while True:
        while jq.empty():
            time.sleep(120)
        job=jq.get()
        Best_node=rm.GetBestNode()
        t=Threading.Thread(Job_Run(job,Best_node))
        t.start()
        q.put(t)

