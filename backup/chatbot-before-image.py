from itty import *
import urllib2
import json
import gooimage


def sendSparkGET(url):
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
    contents = urllib2.urlopen(request).read()
    return contents
   
@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    """
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'hello' in in_message:
            msg = "Hello!"
        elif 'can you' in in_message or 'do you' in in_message or 'do something' in in_message:
            msg = "I can do a Wiki search (search), find the location (locate) or translate the text (translate) of an image."
        #elif 'batsignal' in in_message:
         #   print "NANA NANA NANA NANA"
          #  sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
        #else:
         #   msg = "What can I do for you?"
        if msg != None:
            print msg
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"

bot_email = "jjla@sparkbot.io"
bot_name = "JJLA"
bearer = "MWE5M2NhM2QtOTdmMS00MTQ2LThhNjgtODM0NzE2YjVlZTdlMTAxNTk0MTItYjNl"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"
run_itty(server='wsgiref', host='0.0.0.0', port=8080)
