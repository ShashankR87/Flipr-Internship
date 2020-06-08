import cv2
import pytesseract
import imutils
import time
import re
def pyramid(image, scale=1, minSize=(30, 30)):
    
    yield image
    
    while True:
        
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)
        
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        
        yield image
def sliding_window(image, stepSize, windowSize):
    
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
            
img = cv2.imread("image4.jpg",0)
aadhar_nos = set()
shape  = img.shape
ratio = shape[1]/shape[0]
print(shape)
img = cv2.resize(img, (600, int(shape[0]/ratio)))
shape  = img.shape
print(shape,' ',ratio)
(ww,wh) = (shape[1]//3,shape[0]//10)
print(ww,' ',wh)

for resized in pyramid(img, scale=1.5):
    
    for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(ww, wh)):
        
        if window.shape[0] != wh or window.shape[1] != ww:
            continue
        
        copy = img[y:y+wh,x:x+ww]
        cv2.imwrite('temp.jpg',copy)
        copy = cv2.imread('temp.jpg')
        
        for ih in range(copy.shape[0]):
            for iw in range(copy.shape[1]):
                b,g,r = copy[ih,iw]
                if r>80 or g>80 or b>130:
                    copy[ih,iw] = (255,255,255)
                else:
                    copy[ih,iw]=(0,0,0)
                
        
        ocr_result = pytesseract.image_to_string(copy, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        if len(ocr_result)>5 and re.search('[0-9]+',ocr_result):
            aadhar = re.findall('([0-9]{4} [0-9]{4} [0-9]{4})',ocr_result)
            if(len(aadhar)>0):
                aadhar_nos.add(aadhar[0])


for a in aadhar_nos:
    print(a)