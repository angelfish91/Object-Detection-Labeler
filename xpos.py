# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 18:59:18 2017
@author: 69390
"""
import cv2,os,sys,codecs,copy
import numpy as np
import pandas as pd

def init(base_path):
    listdir = os.listdir(base_path)
    full_path = [os.path.join(base_path, x) for x in listdir]
    df = pd.DataFrame({"path": full_path})
    df = df.set_index("path")
    return df, full_path


def main(base_path):
    
    
    df, full_path = init(base_path)

    data = []
    
    count = len(full_path)
    n = 0
    while n < count: 
        i = full_path[n]
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
                
                
        num_imgs = len(full_path)
        print "You are processing:", i
        print "There are still {:d} left".format(num_imgs-n-1)

        
        img = cv2.imread(i)
        img2 = copy.deepcopy(img)
        cv2.namedWindow('xPos', cv2.WND_PROP_FULLSCREEN)
        cv2.setMouseCallback('xPos', roi)
        while(1):
            cv2.imshow('xPos',img)
            k = cv2.waitKey(1) & 0xFF
            if k == 98:
                print 'roll back'
                n -= 1
                data.pop(-1)
                break
            if k == 32:
                n += 1
                print '==============>>', posx1,posy1,posx2,posy2
                data.append([posx1,posy1,posx2,posy2])
                break
            if k == 27:
                return None, None
        
    return full_path, data

def extract(full_path, data, out_path = None):
    if out_path == None:
        out_path = os.path.join(os.getcwd(), 'pos_all.txt')
    else:
        out_path = os.path.join(out_path, 'pos_all.txt')
    print "pos data has been written into >>", out_path
    f = open(out_path,'w')
    for i in range(len(full_path)):
        f.write(full_path[i] + '\t' + 
                str(data[i][0]) + '\t' + 
                str(data[i][1]) + '\t' + 
                str(data[i][2]) + '\t' + 
                str(data[i][3]) + '\n' )
    return out_path
        

def xml(pos_file, out_path = None):
    if out_path == None:
        out_path = os.path.join(os.getcwd(), 'xml')
        os.mkdir(out_path)
        out_train_path = os.path.join(os.getcwd(), 'train.txt')
    else:
        out_path = os.path.join(out_path, 'xml')
        os.mkdir(out_path)
        out_train_path = os.path.join(out_path, 'name_list.txt')        

    root = out_path

    fp = open(pos_file,'r')    
    fp2 = open(out_train_path, 'w')
    uavinfo = fp.readlines()
    
    for i in range(len(uavinfo)):
        line = uavinfo[i]
        line = line.strip().split('\t')   
        img = cv2.imread(line[0])
        sp = img.shape
        height = sp[0]
        width = sp[1]
        depth = sp[2]
        info1 = line[0].split('\\')[-1]
        info1 = info1.split('/')[-1]
        info2 = info1.split('.')[0]
        l_pos1 = line[1]
        l_pos2 = line[2]
        r_pos1 = line[3]
        r_pos2 = line[4]
        fp2.writelines(info2 + '\n')
        
        file_name = info2 + '.xml'
        with codecs.open(os.path.join(root,file_name), 'w', 'utf-8') as xml:
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + 'UAV_data' + '</folder>\n')
            xml.write('\t<filename>' + info1 + '</filename>\n')
            xml.write('\t<source>\n')
            xml.write('\t\t<database>The UAV autolanding</database>\n')
            xml.write('\t\t<annotation>UAV AutoLanding</annotation>\n')
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
            xml.write('\t<object>\n')
            xml.write('\t\t<name>uav</name>\n')
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
    fp2.close()




if __name__ == "__main__":
    drawing = False
    if len(sys.argv) !=2 and len(sys.argv) !=3:
        print """
        written:
            sparrow
        usage:
            python xpos.py /path/to/imgs  /path/to/out/file
        使用方法：
            第一个参数是图片的路径，不能为空
            第二个参数是产生的XML文件和POS文件的路径，如果为空，那么则为此脚本的路径
        """
    else:
        base_path = sys.argv[1]
        full_path, data = main(base_path)
        if data != None:
            cv2.destroyAllWindows()
            try:
                out_path = sys.argv[2]
            except:
                out_path = None
            pos_file_path = extract(full_path, data, out_path = out_path)
            print "==============================="
            print "Preparing to Generate XML file"
            print "==============================="
            xml(pos_file = pos_file_path , out_path = out_path)
            print "ALL Work done"
