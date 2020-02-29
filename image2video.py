# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:49:10 2020

@author: jadta
"""
import os
import glob
import subprocess
import urllib.request
import json
from urllib.error import URLError, HTTPError

#used to open subreddit JSON, can chooose which subreddit as well as quantity of pictures
def getSubreddit(subreddit='pics',quantity=20):
    #usually have to try twice in order to connect, cannot connect multiple times in short time period!!
    try:
        response = urllib.request.urlopen("https://www.reddit.com/r/{}/hot.json?limit={}".format(subreddit,quantity+1))
    #if cannot connect to url use backup file
    except (URLError,HTTPError):
        print("Connection timed out. Loading sample file.")
        backup = open('backup.json')
        obj = json.load(backup)
        backup.close()
        return obj
    else:
        print("Request successful!")
        obj = json.loads(response.read())
        return obj

#used to retrieve images from JSON file and create concat demuxer txt file
def getImages(obj,quantity = 20):
    print("Getting images...")
    
    #create images folder if not already present
    if not os.path.exists('images'):
        os.makedirs('images')
        
    queue = open('images/queue.txt','w')
    
    for i in range(1,quantity+1):
        
        #parse json for domain and image url
        domain = obj['data']['children'][i]['data']['domain']
        imageurl = obj['data']['children'][i]['data']['url']
        
        #write file names to queue.txt
        queue.write('file \'pic{}.jpg\'\n'.format(i))
        queue.write('duration 3\n')
        
        #clean up imgur.com links
        if(domain == 'imgur.com'):
            urllib.request.urlretrieve(imageurl+'.jpg','images/pic{}.jpg'.format(i))
        else:
            urllib.request.urlretrieve(imageurl,'images/pic{}.jpg'.format(i))

    queue.close()
    return 1

#used to process images with ffmpeg
def processImages(txt = 'images/queue.txt'):
    print("Processing...")
    
    #process images from queue.txt into summary.mp4 video, added padding in order to stop even pixel error
    try:
        convert = subprocess.check_call(['ffmpeg','-y','-f','concat','-i','{}'.format(txt),'-pix_fmt','yuvj422p','-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','summary.mp4'], capture_output = True)
    except subprocess.CalledProcessError:
        print("Oops something went wrong. Please try again.")
        return 0
    else:
        print("Complete!")
        return 1
    
#used to delete images folder
def cleanupImages():
    files = glob.glob('images/*')
    
    for f in files:
        os.remove(f)
    os.rmdir('images')
    
    return 1

#function calls
def main():
    obj = getSubreddit('pics',20)
    getImages(obj,20)
    processImages('images/queue.txt')
    cleanupImages()

if __name__ == "__main__":
    main()