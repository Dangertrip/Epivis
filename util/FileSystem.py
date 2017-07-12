import os
from CLusterManager import singleton

#@singleton
#Filesystem should be unique for every different user.
class Filesystem():

    def __init__(self):
        self.cache_cwd=None

    def setcwd(self,cwd):
        self.cwd = cwd

    def getcwd(self):
        return cwd

    def download(self):


def download_from_basemount():
    pass


