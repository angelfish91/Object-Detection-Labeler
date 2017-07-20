# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 18:59:18 2017

@author: 69390
"""
import cv2,os,sys,codecs,copy
import numpy as np
import pandas as pd
import argparse
from pprint import pprint
import pickle

def init(base_path):
    listdir = os.listdir(base_path)
    full_path = [os.path.join(base_path, x) for x in listdir]
    return full_path


def extract_each_frame(path):
    
    data = {}

    for count, i in  enumerate(range(n_class)):
        data[str(count+1)] = []
    

    count = 0
    while count < n_class: 

        def roi(event, x, y, flags, param):
            global posx1, posy1, posx2, posy2, drawing
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                posx1, posy1 = x, y
                print posx1, posy1
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing == True:
                    img[:,:,:] = img2[:,:,:]
                    cv2.rectangle(img,(posx1,posy1),(x,y),(255,0,0), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                posx2, posy2 = x, y
                print posx2, posy2
                cv2.rectangle(img, (posx1, posy1), (posx2, posy2), (0, 0, 255), 2) 
                    

        print "You are processing:", path
        print "You're labeling the %d Object" %(count+1) 
            
            
        img = cv2.imread(path)
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = str(count+1)+classname[count]
        cv2.putText(img, str(text), (20,100), font, 1,(0,0,255),2,cv2.LINE_AA)

        img2 = copy.deepcopy(img)
        cv2.namedWindow('xPos', cv2.WND_PROP_FULLSCREEN)
        cv2.setMouseCallback('xPos', roi)
        while(1):
            cv2.imshow('xPos',img)
            k = cv2.waitKey(1) & 0xFF
                
            if k == ord('c'):
                count +=1
                if count == n_class:
                    pprint(data)
                    return data
                print 'move to next object'                    
                break
            if k == ord('r'):
                count = 0
                data = {}
                for tem1, tem2 in  enumerate(range(n_class)):
                    data[str(tem1+1)] = []
                print "Data has been refresh!!!"
                pprint(data)

                break

            if k == 32:
                print '==============>>', posx1,posy1,posx2,posy2
                data[str(count+1)].append([posx1,posy1,posx2,posy2])

            if k == ord('q'):
                exit()

            if k == 27:
                return None         

def main(base_path):
    full_path = init(base_path)
    num_imgs = len(full_path)

    data = {}

    for n , i in enumerate(full_path):
        data[i] = extract_each_frame(i)
        print "=================>>>    <<<==================="
        print "You are processing:", i
        print "There are still {:d} left".format(num_imgs-n-1)
        print "=================>>>    <<<==================="
    return data        



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = 'Welcome to use xPos!')
    parser.add_argument('--img-path', type=str, default=None, 
                        metavar='/path/to/imgs', help='input image path')
    parser.add_argument('--out-path', type=str, default=str(os.getcwd()), 
                        metavar='/path/to/out/file', help='XML output path (default: Working Directory)')
    parser.add_argument('--nclass', type=int, default=2, 
                        metavar='N', help='nclass object to classify (default: 2)')
    args = parser.parse_args()

    classname = ['ball', 'basket']

    if args.img_path is not None:
        base_path = args.img_path
        out_path = args.out_path
        n_class = args.nclass


        drawing = False    
        data = main(base_path)
        out_file = os.path.join(out_path,'xpos.pkl')


        f = open(out_file, 'w')
        pickle.dump(data, f)
        f.close()
        pprint(data)