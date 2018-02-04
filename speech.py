import pyttsx
import Image, ImageEnhance, ImageFilter
import pytesseract
import argparse
import cv2
import os
from gtts import gTTS

def speech(filename):

    im = Image.open(str(filename))
    im = im.filter(ImageFilter.MedianFilter())
    im = im.convert('1')
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    
    text = pytesseract.image_to_string(im)
    text = text.encode('utf-8')
    
    #engine = pyttsx.init()
    #engine.say(text)
    #engine.runAndWait()

    tts = gTTS(text.decode('utf-8'), lang = 'en')
    tts.save("audio.mp3")
   # os.system("mpg321 audio.mp3")
