
import smtplib
import sys
import urllib2
import time

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
    for cpt in range(60):
        body = urllib2.urlopen("http://www.iheartquotes.com/api/v1/random").read()
        send_mail("Your random Quote by a (not so?) funny? consultant",body)
        time.sleep(1)

    
        
             