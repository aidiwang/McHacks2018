import Image, ImageEnhance, ImageFilter
import pytesseract
import argparse
import cv2
import os
from googletrans import Translator

def translate(translatefilename, langcode):

    #pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    

    im = Image.open(str(translatefilename))
    im = im.filter(ImageFilter.MedianFilter())
    im = im.convert('1')
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    
    text = pytesseract.image_to_string(im)

    translator = Translator()
    text = translator.translate(text, dest=langcode).text
    
    
    return text



     
    #show the output images
    '''cv2.imshow("Image", image)
    cv2.imshow("Output", gray)
    cv2.waitKey(0)'''
