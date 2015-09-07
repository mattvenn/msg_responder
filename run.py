from flask import Flask, request, redirect
import twilio.twiml
import logging
from secrets import my_num, wordnik_key
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
        word = command[1]
        log.debug("looking up [%s]" % word)
        client = swagger.ApiClient(wordnik_key, wordnik_url)
        wordApi = WordApi.WordApi(client)
        definitions = wordApi.getDefinitions(word, limit=1)
        if definitions is None:
            response = "no definition"
        else:
            response = definitions[0].text
    else:
        response = "unrecognised command"

    log.debug(response)
    resp = twilio.twiml.Response()
    resp.message(response)
    return str(resp)
 
if __name__ == "__main__":
    app.run('0.0.0.0',40000)
    log.info("stopping")
