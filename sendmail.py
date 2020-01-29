
import smtplib
import sys
import os
import datetime
import urllib2
import time

import MyBruGISDeployConf as MDC

def send_mail(subject,body):
    sender = 'brugis@urban.brussels'
    receivers = ['brugis@urban.brussels']
    msg = "\r\n".join([
        "From: " + sender,
        "To: " + ",".join(receivers),
        "Subject: " + subject,
        "",
        body
        ])
    try:
        server=smtplib.SMTP('relay.irisnet.be')
        server.ehlo()
        server.sendmail(sender,receivers,msg)
        print "Successfully sent mail"
    except Exception:
        print "Error : Unable to send email", sys.exc_info[0]

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
	with open(os.path.join(os.path.dirname(__file__), args[1]), 'r') as body:
            send_mail('%s - %s - mail content of %s - %s' % (MDC.localServerName, os.path.basename(__file__), args[1], str(datetime.datetime.today())), body.read())
    else:
        for cpt in range(60):
            body = urllib2.urlopen("http://www.iheartquotes.com/api/v1/random").read()
            send_mail("Your random Quote by a (not so?) funny? consultant",body)
            time.sleep(1)

    
        
             
