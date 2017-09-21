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


def extract_each_frame(path, full_path):
    global h1,h2,h3,h4

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
        # add caption        
        [height, width, depth] = img.shape
        img = np.concatenate((np.zeros((50, width, depth),dtype = np.uint8), img ), axis = 0)
        # add labeling infomation
        font = cv2.FONT_HERSHEY_TRIPLEX
        text = 'You are labeling {count}-{name}'.format(count = count +1,name = classname[count])  
        cv2.putText(img, str(text), (5,30), font, 1,(0,0,255),2,cv2.LINE_AA)
        # main part
        img2 = copy.deepcopy(img)
        cv2.namedWindow('xPos', cv2.WND_PROP_FULLSCREEN)
        cv2.setMouseCallback('xPos', roi)
        
        while(1):
            cv2.imshow('xPos',img)
            k = cv2.waitKey(1) & 0xFF
            
            if k == ord('q'):
                with open('tem.pkl', 'r') as f:
                    data = pickle.load(f)
                labeled_imgs_path = data.keys()
                unlabeled_imgs_path = list(set(full_path)-set(labeled_imgs_path))
                with open("config.cfg", 'w') as f:
                    for _ in unlabeled_imgs_path:
                        f.writelines(_+"\n")
                exit()
                
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
            if k == ord(' '):
                x1 = min([posx1, posx2]) 
                y1 = min([posy1, posy2]) - 50
                x2 = max([posx1, posx2])
                y2 = max([posy1, posy2]) - 50               
                local_height = y2-y1
                local_width = x2-x1
                if x1< 0 or y1 <0:
                    print "Exception: bbox over limit"
                elif (h1==x1 and h2==y1 and h3==x2 and h4==y2) or ( x2 >width or y2 > height):
                    print "Exception: get same parameters"
                else:
                    print '==============>> {x1}-{y1}-{x2}-{y2} : {width}-{height}'.format(
                            x1=x1,y1=y1,x2=x2,y2=y2, width=local_width, height=local_height)
                    data[str(count+1)].append([x1,y1,x2,y2])
                    h1,h2,h3,h4 = x1,y1,x2,y2
                    
            if k == 27:
                return None         

def main(base_path, args):
    if not args.config:
        full_path = init(base_path)
        num_imgs = len(full_path)

        data = {}
    else:
        with open("./config.cfg", "r") as f:
            full_path = f.read().split("\n")
            full_path = full_path[:-1]
        num_imgs = len(full_path)
        with open("./tem.pkl", "r") as f:
            data = pickle.load(f)
        print data

    n = 0
    while n < num_imgs:
        i = full_path[n]
        result = extract_each_frame(i, full_path)
        if result is None:
            if n-1 >= 0:
                del data[full_path[n-1]]
                n -=1
        else:
            data[i] = result
            print "***********************************************"
            print "You are processing:", i
            print "There are still {:d} left".format(num_imgs-n-1)
            print "***********************************************"
            
            f = open('tem.pkl', 'w')
            pickle.dump(data, f)
            f.close()
            
            n +=1

    return data        



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = 'Welcome to use xPos!')
    parser.add_argument('--img-path', type=str, default=None, 
                        metavar='/path/to/imgs', help='input image path')
    parser.add_argument('--out-path', type=str, default=str(os.getcwd()), 
                        metavar='/path/to/out/file', help='XML output path (default: Working Directory)')
    parser.add_argument('--nclass', type=int, default=2, 
                        metavar='N', help='nclass object to classify (default: 2)')
    parser.add_argument('--config', type=int, default=0, 
                        metavar='config', help='set True if the tool crash (default: False)')
    
    args = parser.parse_args()

    classname = ['ball', 'basket']

    if args.img_path is not None:
        base_path = args.img_path
        out_path = args.out_path
        n_class = args.nclass


        drawing = False
        h1,h2,h3,h4 = 0,0,0,0
        posx1, posx2, posy1, posy2 = 0,0,0,0
        data = main(base_path, args)
        out_file = os.path.join(out_path,'xpos.pkl')


        f = open(out_file, 'w')
        pickle.dump(data, f)
        f.close()
        pprint(data)
