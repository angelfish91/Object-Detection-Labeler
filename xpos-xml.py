# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 23:19:50 2017

@author: 69390
"""

import pickle
import os
import cv2
import codecs
import argparse

def get_pkl(path):
    f = open(path)
    data = pickle.load(f)
    return data


def xml(out_path, data):
    if out_path == None:
        out_path = os.path.join(os.getcwd(), 'xml')
        os.mkdir(out_path)

    else:
        out_path = os.path.join(out_path, 'xml')
        os.mkdir(out_path)
       
    
    root = out_path
    



    for i in range(len(data.keys())): 
        img = cv2.imread(data.keys()[i])
        sp = img.shape
        height = sp[0]
        width = sp[1]
        depth = sp[2]
        info1 = data.keys()[i].split('\\')[-1]
        info1 = info1.split('/')[-1]
        info2 = info1.split('.')[0]
        

        file_name = info2 + '.xml'
        with codecs.open(os.path.join(root,file_name), 'w', 'utf-8') as xml:
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + 'basketball_data' + '</folder>\n')
            xml.write('\t<filename>' + info1 + '</filename>\n')
            xml.write('\t<source>\n')
            xml.write('\t\t<database>basketball tracking</database>\n')
            xml.write('\t\t<annotation>basketball Tracking</annotation>\n')
            xml.write('\t\t<image>flickr</image>\n')
            xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t</source>\n')
            xml.write('\t<owner>\n')
            xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t\t<name>XuSenhai</name>\n')
            xml.write('\t</owner>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>'+ str(width) + '</width>\n')
            xml.write('\t\t<height>'+ str(height) + '</height>\n')
            xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
            xml.write('\t</size>\n')
            xml.write('\t\t<segmented>0</segmented>\n')
            
            pos1 = data[data.keys()[i]]['1']
            if len(pos1)!=0:
                for j in pos1:
                    l_pos1 = str(j[0])
                    l_pos2 = str(j[1])
                    r_pos1 = str(j[2])
                    r_pos2 = str(j[3])
                    
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>ball</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    xml.write('\t\t<truncated>0</truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + l_pos1 + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + l_pos2 + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + r_pos1 + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + r_pos2 + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
            else:
                pass
            
            pos2 = data[data.keys()[i]]['2']
            if len(pos2)!=0:
                for j in pos2:
                    l_pos1 = str(j[0])
                    l_pos2 = str(j[1])
                    r_pos1 = str(j[2])
                    r_pos2 = str(j[3])
                    
                    
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>basket</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    xml.write('\t\t<truncated>0</truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + l_pos1 + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + l_pos2 + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + r_pos1 + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + r_pos2 + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
            
            
            
            xml.write('</annotation>')
            
            
            
            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Welcome to use xPos-xml!')
    parser.add_argument('--pkl-path', type=str, default=None, 
                        metavar='/path/to/pkl', help='input pkl path')
    parser.add_argument('--out-path', type=str, default=str(os.getcwd()), 
                        metavar='/path/to/out/file', help='XML output path (default: Working Directory)')
    
    args = parser.parse_args()
    if args.pkl_path is not None:
        pkl_path = args.pkl_path
        out_path = args.out_path
        
        data = get_pkl(pkl_path)
        xml(out_path = out_path, data = data)
        
        
        
        
        