from flask import Flask, request, redirect
import twilio.twiml
import logging
from secrets import my_num
 
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
    if from_number != my_num:
        log.info("not responding to invalid number %s" % from_number)
        return ''

    resp = twilio.twiml.Response()
    resp.message(body)
    return str(resp)
 
if __name__ == "__main__":
    app.run('0,0,0,0',40000, debug=True)
