import os
from ClusterManager import singleton
from Basemount import Basemount

#@singleton
#Filesystem should be unique for every different user.
class Filesystem():

    def __init__(self):
        self.cache_cwd=None

    def setcwd(self,cwd):
        self.cwd = cwd

    def getcwd(self):
        return cwd

    def download(self,bm): #need a basemount object
        fileinfo = bm.GetProjects()


def download_from_basemount():
    pass


