# msg_responder

Twilio based SMS responder service that at the moment has these commands:

* w word - looks up a word on wordnik.com and replies with the definition
* p delay - gives a callback in delay seconds

# Requirements

## Python

python2.7 or higher

pip install -r requirements.txt

## Wordnik

Setup an account and apply for API (which will be shown in account settings)

## Twilio

* setup account
* buy a number capable of receiving and sending texts
* set SMS URL to your internet host on port 40000

## Secrets

copy not-secrets.py to secrets.py and fill in the blanks

## Firewall

open port 40000

    -A INPUT -p tcp -m state --state NEW --dport 40000 -j ACCEPT

## Install supervisord service

    sudo cp msg_responder.conf /etc/supervisor/conf.d
    sudo supervisorctl reread
    sudo supervisorctl start msg_responder
