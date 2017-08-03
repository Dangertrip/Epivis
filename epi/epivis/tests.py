from django.test import TestCase
from .util.Basemount import FS

fs = FS()
p=fs.GetProjects('/Users/yyin/github/basespace')
fs.preset_folder(p)
# Create your tests here.
