#!/usr/bin/env python
# encoding: utf-8

import subprocess
p=subprocess.Popen('mcall',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(p.stdout.readlines())
p.wait()
