#!/bin/env python

import os

for line in os.popen('ps -auxf').readlines():
    print line
