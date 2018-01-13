import time
import smtplib
from email.mime.text import MIMEText
import sys

doc = '''
Useage: python 2.7 followlog.py <logfile> <smtpserver> <smtpport> <username> <password> <mailfrom> <mailto>
'''


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        if '!----- Alarm Raise ----' in line:
            alarm = line
            for currentalertline in range(10):
                alarm += thefile.readline()
            sendmail(alarm, 'Alarm Raise')
        elif '!----- Alarm Clear ' in line:
            alarmclear = line
            for currentalertline in range(10):
                alarmclear += thefile.readline()
            sendmail(alarmclear, 'Alarm Clear')


def sendmail(message='', alarmtype=''):
    user = sys.argv[4]
    passwd = sys.argv[5]
    mailserver = sys.argv[2]
    mailserverport = sys.argv[3]
    mailfrom = sys.argv[6]
    mailtarget = sys.argv[7]
    try:
        msg = MIMEText('')
        msg['Subject'] = alarmtype
        msg['From'] = mailfrom
        msg['To'] = mailtarget
        smtpserver = smtplib.SMTP(mailserver, mailserverport)
        smtpserver.starttls()
        smtpserver.login(user, passwd)
        smtpserver.sendmail(mailfrom, mailtarget, str(message))
        smtpserver.quit()
    except Exception, e:
        print(str(e))


if __name__ == '__main__':
    if len(sys.argv) != 7:
        print(doc)
        sys.exit(-1)
    with open(sys.argv[1]) as logfile:
        follow(logfile)
