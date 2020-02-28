# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:06:39 2020

@author: jadta
"""
from image2video import getSubreddit
from image2video import getImages
from image2video import processImages
from image2video import cleanupImages

backup = open('backup.json')
obj = json.load(backup)
backup.close()

def test_getSubreddit():
    assert getSubreddit('0') == obj
    
def test_getImages():
    assert getImages() == 1
    
def test_processImages():
    assert processImages() == 0
    
def test_cleanupImages():
    assert cleanupImages() == 1
