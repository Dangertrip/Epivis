from xml.etree import ElementTree as ET
from xml.dom import minidom
import os
from .GetNode import *

#Check legality of computational nodes.
def _check_node(node):
    nodes = GetNode()
    for n in node:
        if not n in nodes:
            return False
    return True


#Check legality of cache path.
def _check_cache(path):
    if os.path.exists(path):
        return False #The web should tell people why it can not
    #Get permission of the path
    prepath = path[:path.rfind('/')]
    permission=oct(os.stat(prepath).st_mode)[-3:]
    if permission=='755':
        os.mkdir(path)
    else: 
        return False
    return True


'''
Get meta info from metasetting and parse it to the web application
Raise Exceptions to alert Errors
Get nothing and return  1. Metainfo completion(True/False) 2.node list 3.cache_path
'''
def getmetainfo():
    try:
        with open('metasetting.xml') as f:
            metadata = f.read()
    except IOError as err:
        print('Missing meta data file "metasetting.xml".')
    #print(metadata) 
    root = ET.fromstring(metadata)    
    #r = tree.getroot()
    node=[]
    if root[0].tag!='cache_path' or root[1].tag!="nodes":
        raise Exception('Wrong tags in metasetting.xml !')
    cache_path=root[0].text
    nodes = root[1]
    for i in range(1,len(nodes)):
        child = nodes[i]
        if child.tag!='node':
            raise Exception('Wrong tags in metasetting.xml !')
        node.append(node)
    mark=True
    if not _check_node(node) or not _check_cache(cache_path):
        mark=False
    return mark,node,cache_path

def SetMeta(cache_path,nodes):
    xml = minidom.Document()
    root = xml.createElement('meta')
    xml.appendChild(root)
    cache = xml.createElement('cache_path')
    root.appendChild(cache)
    text = xml.createTextNode(cache_path)
    cache.appendChild(text)
    #print(xml.toprettyxml(encoding='utf-8'))
    for node in nodes:
        n = xml.createElement('node')
        root.appendChild(n)
        text = xml.createTextNode(node)
        n.appendChild(text)

    with open('metasetting.xml','w') as f:
        f.write(xml.toprettyxml(encoding='utf-8').decode('utf-8'))

if __name__=="__main__":
    #SetMeta('aaa',['1','2'])
    print(getmetainfo())
