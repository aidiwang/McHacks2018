import Image, ImageEnhance, ImageFilter
import pytesseract
import argparse
import cv2
import os
from googletrans import Translator

def translate(translatefilename):

    #pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    '''image=cv2.imread(translatefilename)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    gray=cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    gray=cv2.medianBlur(gray,3)

    filename='{}.png'.format(os.getpid())
    cv2.imwrite(filename,gray)

    text=pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)'''

    im = Image.open(str(translatefilename))
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    
    
    text = pytesseract.image_to_string(im)

    #translator = Translator()
    #translated = translator.translate(text).encode("utf-8")

    return text.encode("utf-8")
    

     
    #show the output images
    '''cv2.imshow("Image", image)
    cv2.imshow("Output", gray)
    cv2.waitKey(0)'''
