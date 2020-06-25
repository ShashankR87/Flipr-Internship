import numpy as np
import cv2
import pytesseract
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join
import os
from pdf2image import convert_from_path, convert_from_bytes
verhoeff_table_d = (
    (0,1,2,3,4,5,6,7,8,9),
    (1,2,3,4,0,6,7,8,9,5),
    (2,3,4,0,1,7,8,9,5,6),
    (3,4,0,1,2,8,9,5,6,7),
    (4,0,1,2,3,9,5,6,7,8),
    (5,9,8,7,6,0,4,3,2,1),
    (6,5,9,8,7,1,0,4,3,2),
    (7,6,5,9,8,2,1,0,4,3),
    (8,7,6,5,9,3,2,1,0,4),
    (9,8,7,6,5,4,3,2,1,0))
verhoeff_table_p = (
    (0,1,2,3,4,5,6,7,8,9),
    (1,5,7,6,2,8,3,0,9,4),
    (5,8,0,3,7,9,6,1,4,2),
    (8,9,1,6,0,4,3,5,2,7),
    (9,4,5,3,1,2,6,8,7,0),
    (4,2,8,6,5,7,3,9,0,1),
    (2,7,9,3,8,0,6,4,1,5),
    (7,0,4,6,9,1,3,2,5,8))
verhoeff_table_inv = (0,4,3,2,1,5,6,7,8,9)

def calcsum(number):
    """For a given number returns a Verhoeff checksum digit"""
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[(i+1)%8][int(item)]]
    return verhoeff_table_inv[c]

def checksum(number):
    """For a given number generates a Verhoeff digit and
    returns number + digit"""
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
    return c

def generateVerhoeff(number):
    """For a given number returns number + Verhoeff checksum digit"""
    return "%s%s" % (number, calcsum(number))

def validateVerhoeff(number):
    """Validate Verhoeff checksummed number (checksum is last digit)"""
    if len(str(number))==12:
        return checksum(number) == 0
    else:
        return False

def save_image(image,im):
    os.chdir( os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Final 23_06_2020/result'))
    now = datetime.now()
    dot = im.find('.')
    t = int(datetime.timestamp(now))
    savedfn = str(im)[:dot] +'_'+ str(t) +'.jpg'
    cv2.imwrite(savedfn,window)
    os.chdir( os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Final 23_06_2020'))



def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def imageop(imagefile):
    image = cv2.cvtColor(imagefile, cv2.COLOR_BGR2GRAY)
    colorimg = imagefile.copy()

    stepSize = 50
    aadhar_nos=[]
    print(image.shape)


    if image.shape[1]<500:
        image = cv2.resize(image,(image.shape[1]*4,image.shape[0]*4))
    img = cv2.medianBlur(image,5)
    image = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,35,2)
    
    found_in_rot=[]
    
    for rot in range(0,1):
        if len(found_in_rot)>0:
            break
        if len(aadhar_nos)!=0:
            break
        if rot>0:
            image = rotate_image(image, 90*rot)
            
        (W_width, W_height) = (image.shape[1]//4,image.shape[0]//8) 
        tmp = image 
        
        print(W_width,' ',W_height)
        print('Starting now')
        
        found_coord_scale=[]
        for scale in np.arange(0.5,2.1,0.5):
            print('Scale is ',scale)
            print('Already found : ',found_coord_scale)
            w_width = int(W_width*scale)
            w_height = int(W_height*scale)
            stepSizex = int(w_width/7) 
            stepSizey = int(w_height/5)
            
            found_coordinates=[]
            flag=False
            break_from_both=False
            for y in range(0, tmp.shape[0] - w_height , stepSizey):
                for x in range(0, tmp.shape[1] - w_width, stepSizex):
                    if len(found_coord_scale)>0:
                        for e in found_coord_scale:
                            if (e[0]<x and e[0] + w_width>x) and (e[1]<y and e[1] + w_height>y):
                                print('Same')
                                break_from_both=True
                                continue
                    if flag==True:
                        insideflag=False
                        for e in found_coordinates:
                            if (e[0] - x)**2 < (image.shape[1]//8)**2 and (e[1] - y)**2 < (image.shape[0]//8)**2:
                                insideflag=True
                                break
                        if insideflag==True:
                            break
                    window = tmp[y:y + w_height, x:x + w_width]
                    cv2.imwrite('win.jpg',window)
                    tmpi = image.copy()

                    ocr_result = pytesseract.image_to_string(window, lang='eng')
                    
                    
                    detected_aadhar=[]
                    if len(ocr_result)>4 and re.search('[0-9]+',ocr_result):

                        
                        aadhar = re.findall('([0-9]{4} [0-9]{4} [0-9]{4})',ocr_result)
                        if(len(aadhar)>0):
                            detected_aadhar.append(aadhar[0])
                            aadhar_nos.append(aadhar[0])
                            save_image(window,im)
                            flag=True
                            
                    
                        if len(re.findall('([0-9]{4} [0-9]{8})',ocr_result))>0:
                            detected_aadhar.append(re.findall('([0-9]{4} [0-9]{8})',ocr_result)[0])
                            save_image(window,im)
                            flag=True
                            
                        if len(re.findall('([0-9]{8} [0-9]{4})',ocr_result))>0:
                            detected_aadhar.append(re.findall('([0-9]{8} [0-9]{4})',ocr_result)[0])
                            save_image(window,im)
                            flag=True
                        if len(re.findall('([0-9]{12})',ocr_result))>0:
                            detected_aadhar.append(re.findall('([0-9]{12})',ocr_result)[0])
                            save_image(window,im)
                            flag=True
                        if len(re.findall('([0-9 ]{14})',ocr_result))>0:
                            detected_aadhar.append(re.findall('([0-9 ]{14})',ocr_result)[0])
                            save_image(window,im)
                            flag=True
                        if flag==True and len(detected_aadhar)>0:
                            print(detected_aadhar)
                            for i in range(len(detected_aadhar)):
                                isValid = validateVerhoeff(int(str(detected_aadhar[i]).replace(' ','')))
                                
                                if isValid == True:
                                    aadhar_nos.append(detected_aadhar[0])
                                    print(detected_aadhar,' ',isValid)
                                    for  sw_width in range(window.shape[1]//10, window.shape[1], (window.shape[1]//10)):

                                        for sw_height in range(window.shape[0]//5, window.shape[0], window.shape[0]//5):
                                            
                                            smallwindow = window[:sw_height, : sw_width]
                                            
                                            text = pytesseract.image_to_string(smallwindow, lang='eng')

                                            ocr_result_small = re.findall('[0-9 ]+',text)
                                            

                                            if(len(ocr_result_small))>0:
                                                number=0
                                                for d in ocr_result_small:
                                                    d = d.replace(' ','')
                                                    if d.isnumeric():
                                                        number = d
                                                ocr_result_small = number
                                                if len(str(ocr_result_small))==8:
                                                    for e in found_coord_scale:
                                                        if (e[0]<=x and e[0] + sw_width>=x) and (e[1]<=y and e[1] + sw_height>=y):
                                                            print('Same coord')
                                                            break_from_both=True
                                                            break
                                                    if break_from_both==True:
                                                        break

                                                    cv2.rectangle(colorimg,(x,y),(x+sw_width,y+sw_height),(0, 0, 0),-1)
                                                    cv2.rectangle(tmp,(x,y),(x+sw_width,y+sw_height),(0, 0, 0),-1)
                                                    dot = im.find('.')
                                                    now = datetime.now()
                                                    t = str(int(datetime.timestamp(now)))
                                                    cv2.imwrite('output//'+im[:dot]+t+'masked.jpg',colorimg)
                                                    consh=sw_height
                                                    print('Drawn ',x,' ',y)
                                                    found_coord_scale.append([x,y])
                                                    break
                                        
                        else:
                                flag=False
                        if flag==True:
                            found_coordinates.append([x,y])
        
                else:
                    continue
                break
            
        found_in_rot.extend(found_coord_scale)


            
    for x in aadhar_nos:
        print(x)
    
    if os.path.exists('Results.txt'):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    results = open('Results.txt',append_write)
    results.write("Filename: " + im +' AadharNos detected: ' +str(aadhar_nos)+ '\n')
    results.close()

#Driver Code
os.chdir( os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Final 23_06_2020'))
cwd = os.getcwd()
cwd = cwd+'\images'
images = listdir(cwd)
print(images)

for im in images:
    
    imagefile = os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Final 23_06_2020/images/'+im)
    print(imagefile)
    
    if '.pdf' in im:
        imginpdf = convert_from_path(imagefile)
        for ip in imginpdf:
            ip.save('temp.jpg','JPEG')
            srcimg = cv2.imread('temp.jpg')
            imageop(srcimg)
    
    else:
        srcimg = cv2.imread(imagefile)
        imageop(srcimg)
    
    
    