#!/usr/bin/env python
# encoding: utf-8


import random
def singleton(cls,*args,**kw):
    instances={}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    return _singleton

@singleton
class MyClass4():
    a=1
    def __init__(self):
        self.x=random.random()
        print(self.x)

one = MyClass4()
two = MyClass4()
print(one.x,two.x)
