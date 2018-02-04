from itty import *
import urllib2
import json
from translate import *
from speech import *
import numpy as np
import cv2
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def sendSparkGETFILE(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request)
    return contents

def sendSparkGETTEXT(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
   
def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read
    return contents
   
@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    """
    webhook = json.loads(request.body)

    #retrieve files code here
    if webhook['data'].has_key('files'):
        for file_url in webhook['data']['files']:

#            print "\n\nstart url"
#            print file_url
#            print "end\n\n"
            
            response = sendSparkGETFILE(file_url)

            print "\n\nstart response"
            #print response.info().get('Content-Disposition')
            print response
            print "end\n\n"
            
            content_disp = response.headers.get('Content-Disposition', None)
            if content_disp is not None:
                filename = content_disp.split("filename=")[1]
                filename = filename.replace('"', '')
                
                with open(filename, 'wb') as f:
                    f.write(response.read())
                    print 'Saved-', filename
                '''with open(response.read(), 'rb') as f:
                    data = f.read()
                with open(filename, 'wb') as f:
                    f.write(data)'''
                
            else:
                print "Cannot save file- no Content-Disposition header received."
    '''else:
        print "No files attached to retrieve!"
        return "true"'''
    #retrieve files code here

    print webhook['data']['id']
    result = sendSparkGETTEXT('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))

    #result.read()
    
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:

        #print "\n\nhere are the results"
        #print result
        #print "end of result\n\n"

        #if 'files' in result:
        #    in_image = result.get('files', '')
        
        in_message = result.get('text').lower()
        in_message = in_message.replace(bot_name, '')
        if 'hello' in in_message:
            msg = "Hello!"
        elif 'can you' in in_message or 'do you' in in_message or 'do something' in in_message:
            msg = "I translate the English text (attach an image and type \"translate\" + language) from an image to any language you want.\n\nI can also read an English text image (attach an image and type \"read\"). "
        
        #start functions
        #elif 'search' in in_message:
        #    print "searching..."
        #    msg = search(filename)
            
        #elif 'locate' in in_message:
        #    msg = locate(filename)
            
        elif 'translate' in in_message:
            tolanguage = result.get('text').split('translate')[1].strip(" ")
            tolanguage = tolanguage.lower()

            #dictionary?
            languages = {
                    "afrikaans": "af",
                    "albanian" : "sq",
                    "arabic" : "ar",
                    "azerbaijani": "az",
                    "basque": "eu",
                    "bengali": "bn",
                    "belarusian": "be",
                    "bulgarian": "bg",
                    "catalan": "ca",
                    "chinese-simplified": "zh-CN",
                    "chinese-traditional": "zh-TW",
                    "croatian": "hr",
                    "czech": "cs",
                    "danish": "da",
                    "dutch": "nl",
                    "english": "en",
                    "esperanto": "eo",
                    "estonian": "et",
                    "filipino": "tl",
                    "finnish": "fi",
                    "french": "fr",
                    "galician": "gl",
                    "georgian": "ka",
                    "german": "de",
                    "greek": "el",
                    "gujarati": "gu",
                    "haitian creole": "ht",
                    "hebrew": "iw",
                    "hindi": "hi",
                    "hungarian": "hu",
                    "icelandic": "is",
                    "indonesian": "id",
                    "irish": "ga",
                    "italian": "it",
                    "japanese": "ja",
                    "kannada": "kn",
                    "korean": "ko",
                    "latin": "la",
                    "latvian": "lv",
                    "lithuanian": "lt",
                    "macedonian": "mk",
                    "malay": "ms",
                    "maltese": "mt",
                    "norwegian": "no",
                    "persian": "fa",
                    "polish": "pl",
                    "portuguese": "pt",
                    "romanian": "ro",
                    "russian": "ru",
                    "serbian": "sr",
                    "slovak": "sk",
                    "slovenian": "sl",
                    "spanish": "es",
                    "swahili": "sw",
                    "swedish": "sv",
                    "tamil": "ta",
                    "telugu": "te",
                    "thai": "th",
                    "turkish": "tr",
                    "ukrainian": "uk",
                    "urdu": "ur",
                    "vietnamese": "vi",
                    "welsh": "cy",
                    "yiddish": "yi",    
                }

            for k, m in languages.items():
                if tolanguage.lower() == k:
                    langcode = m
            msg = translate(filename, langcode).encode('utf-8')
            os.remove(filename)
            
        elif 'read' in in_message:
            speech(filename)

            m = MultipartEncoder({'roomId': 'Y2lzY29zcGFyazovL3VzL1JPT00vNGE2NWIxODAtMDkxMi0xMWU4LThmMmItNzUyNTQzMWRjYTYw',
                                  'text': 'example attached',
                                  'files': ('audio.mp3', open('audio.mp3', 'rb'),
                                  'audio/mpeg')})

            r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                              headers={'Authorization': 'Bearer MWE5M2NhM2QtOTdmMS00MTQ2LThhNjgtODM0NzE2YjVlZTdlMTAxNTk0MTItYjNl',
                              'Content-Type': m.content_type})
            os.remove(filename)
            print r
          
        #end functions

        else:
            msg = "What can I do for you?"
        if msg != None:
            print msg
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

        #if my_function != None:
         #   if "search" in my_function:
          #  elif "locate" in my_function:
           # elif ""
        
    return "true"

bot_email = "jjla@sparkbot.io"
bot_name = "JJLA"
bearer = "MWE5M2NhM2QtOTdmMS00MTQ2LThhNjgtODM0NzE2YjVlZTdlMTAxNTk0MTItYjNl"
run_itty(server='wsgiref', host='0.0.0.0', port=8080)
