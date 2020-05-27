#Uses Open-cv and Pytesseract to extract Aadhar Number from image. Rotates the image if required.
import cv2
import pytesseract
import re
import numpy as np
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result
angle = 0
img = cv2.imread('Aadhar-Card 4.png',0)
while angle!=360:
    text = 'nothing'
    img = rotate_image(img,angle)
    text = pytesseract.image_to_string(img,lang='eng')
    aadharNo = re.findall('([0-9]{4} [0-9]{4} [0-9]{4})',text)
    if len(aadharNo) == 0:
        aadharNo = re.findall('([0-9]{4}-[0-9]{4}-[0-9]{4})',text)
    if len(aadharNo) == 0:
        angle+=5
    else:
        aadharNo = aadharNo[0]
        break
print(aadharNo)