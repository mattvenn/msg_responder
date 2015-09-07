from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import logging, time, threading, urllib
from secrets import my_num, wordnik_key, sid, token

# dictionary stuff
from wordnik import *
wordnik_url = 'http://api.wordnik.com/v4'
 
# setup logger
log = logging.getLogger('')
log.setLevel(logging.DEBUG)

# create console handler and set level to info
log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(log_format)
log.addHandler(ch)

app = Flask(__name__)

def delayed_call(delay, number, to_num):
    time.sleep(delay)
    # twilio client
    client = TwilioRestClient(sid, token)
    # make the call
    log.info("placing call from %s to %s" % (number, to_num))
    msg_params = {"Message[0]": "here is your message"}
    url="http://twimlets.com/message?" + urllib.urlencode(msg_params),

    call = client.calls.create(to=to_num, 
        from_=number,
        url="http://twimlets.com/message?" + urllib.urlencode(msg_params))
    log.debug(call.sid)

 
@app.route("/", methods=['GET', 'POST'])
def respond():
    from_number = request.values.get('From', None) 
    body = request.values.get('Body', None) 
    log.debug("got [%s] from [%s]" % (body, from_number))
    if from_number != my_num:
        log.info("not responding to invalid number")
        return ''

    # look up a word
    command = body.lower().split()
    if command[0] == 'w':
        # in case more than 1 word
        word = ' '.join(command[1:])
        log.debug("looking up [%s]" % word)
        # do the lookup
        client = swagger.ApiClient(wordnik_key, wordnik_url)
        wordApi = WordApi.WordApi(client)
        definitions = wordApi.getDefinitions(word, limit=1)
        if definitions is None:
            response = "no definition"
        else:
            response = definitions[0].text
    # callback
    elif command[0] == 'p':
        try:
            # delay in seconds
            delay = int(command[1])
        except:
            # default is 60 seconds
            delay = 60
        response = "calling [%s] in %d seconds" % (my_num, delay)
        t = threading.Thread(target=delayed_call, args=(delay, my_num, my_num,))
        t.start()
    # unrecognised command given
    else:
        response = "unrecognised command"

    log.debug(response)
    resp = twilio.twiml.Response()
    resp.message(response)
    return str(resp)
 
if __name__ == "__main__":
    app.run('0.0.0.0',40000,debug=True)
    log.info("stopping")
