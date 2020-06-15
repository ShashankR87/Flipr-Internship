import numpy as np
import cv2
import pytesseract
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join
import os


def save_image(image,im):
    os.chdir( os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Trial 3 13_06_2020/result'))
    now = datetime.now()
    dot = im.find('.')
    t = int(datetime.timestamp(now))
    savedfn = str(im)[:dot] +'_'+ str(t) +'.jpg'
    cv2.imwrite(savedfn,window)
    os.chdir( os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Trial 3 13_06_2020'))



def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

os.chdir( os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Trial 3 13_06_2020'))
cwd = os.getcwd()
cwd = cwd+'\images'
images = listdir(cwd)
print(images)
#images = [f for f in listdir(f'C:\Users\Shashank\Python Projects\Flipr Internship\Trial 3 13_06_2020\images') if isfile(join(f'C:\Users\Shashank\Python Projects\Flipr Internship\Trial 3 13_06_2020\images', f))]
for im in images:
    
    imagefile = os.path.normpath('C:/Users/Shashank/Python Projects/Flipr Internship/Trial 3 13_06_2020/images/'+im)
    print(imagefile)
    
    #print(impath)
    image = cv2.imread(imagefile,0) 

    stepSize = 50
    aadhar_nos=[]
    print(image.shape)


    if image.shape[1]<500:
        image = cv2.resize(image,(image.shape[1]*3,image.shape[0]*3))
    #for ih in range(image.shape[0]):
    #    for iw in range(image.shape[1]):
    #        b,g,r = image[ih,iw]
    #        if r>80 or g>80 or b>130:
    #            image[ih,iw] = (255,255,255)
    #        else:
    #            image[ih,iw]=(0,0,0)
    img = cv2.medianBlur(image,5)
    image = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,17,2)
    
    for rot in range(0,4):
        if len(aadhar_nos)!=0:
            break
        if rot>0:
            image = rotate_image(image, 90*rot)
            
        (W_width, W_height) = (image.shape[1]//4,image.shape[0]//8) 
        tmp = image 
        #time.sleep(0.025)
        print(W_width,' ',W_height)
        print('Starting now')
        for scale in np.arange(0.5,2.1,0.5):
            print('Scale is ',scale)
            w_width = int(W_width*scale)
            w_height = int(W_height*scale)
            stepSizex = int(w_width/6)
            stepSizey = int(w_height/5)
            for y in range(0, tmp.shape[0] - w_height , stepSizey):
                for x in range(0, tmp.shape[1] - w_width, stepSizex):


                    window = tmp[y:y + w_height, x:x + w_width]
                    cv2.imwrite('win.jpg',window)
                    tmpi = image.copy()

                    ocr_result = pytesseract.image_to_string(window, lang='eng')

                    if len(ocr_result)>4 and re.search('[0-9]+',ocr_result):

                        #print('**********Numbers ' + ocr_result)
                        aadhar = re.findall('([0-9]{4} [0-9]{4} [0-9]{4})',ocr_result)
                        if(len(aadhar)>0):
                            aadhar_nos.append(aadhar[0])
                            save_image(window,im)
                            
                    
                        if len(re.findall('([0-9]{4} [0-9]{8})',ocr_result))>0:
                            aadhar_nos.append(re.findall('([0-9]{4} [0-9]{8})',ocr_result)[0])
                            save_image(window,im)
                            
                        if len(re.findall('([0-9]{8} [0-9]{4})',ocr_result))>0:
                            aadhar_nos.append(re.findall('([0-9]{8} [0-9]{4})',ocr_result)[0])
                            save_image(window,im)
                        if len(re.findall('([0-9]{12})',ocr_result))>0:
                            aadhar_nos.append(re.findall('([0-9]{12})',ocr_result)[0])
                            save_image(window,im)
                        if len(re.findall('([0-9 ]{14})',ocr_result))>0:
                            aadhar_nos.append(re.findall('([0-9 ]{14})',ocr_result)[0])
                            save_image(window,im)


                    #print('No exceptions! ')

                   # print('All '+ ocr_result)


            
    for x in aadhar_nos:
        print(x)
    
    if os.path.exists('Results.txt'):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    results = open('Results.txt',append_write)
    results.write("Filename: " + im +' AadharNos detected: ' +str(aadhar_nos)+ '\n')
    results.close()