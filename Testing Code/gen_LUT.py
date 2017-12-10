#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 03:13:34 2016

@author: aman
"""

import numpy as np
import matplotlib.pyplot as plt
t = np.linspace(0,512)

sine =     np.zeros(512)
square =   np.zeros(512)
triangle = np.zeros(512)


sine = np.round(512+512*np.sin(t))
sine = np.array(sine,dtype=np.int)

print(sine)


