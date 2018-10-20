#
#SMS test via Google Voice
#
#Originally made by John Nagle
#   nagle@animats.com

#Modified by Austin Fritzemeier for use in RPiCafe
#	https://github.com/fritzemeier/RPiCafe
#	@fritzemeier
from googlevoice import Voice
from googlevoice.util import input
import sys
import BeautifulSoup
import os
from crontab import CronTab
from datetime import datetime
import pycurl
from StringIO import StringIO

def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    #	Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #	For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :								# for all rows
            #	For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems

def schedCoff(cmd):
	log = ''
	text = ''
        if len(cmd) < 3:
		log = 'Attempted to schedule coffee without specifying time on ' + str(datetime.now())
		sms = 'Time was not specified.'
	elif len(cmd[2]) < 4:
		log = 'Attempted to schedule coffee with incorrect time format on ' + str(datetime.now())
		sms = 'Time was not written correctly: ' + cmd[2]
	if log != '' and sms != "":
		myFile = open('<<path>>/log.txt','a')
		myFile.write('\n' + log)
		voice.send_sms("+1<<phone number from which you will be sending commands -- including area code>>",sms)
		return 1
	time = cmd[2]
	reply = ''
	for x in cmd:
		reply = reply + x + ' '
	if int(time[0]) > 0:
		hour = int(time[0]) * 10 + int(time[1])
	else:
		hour = int(time[1])
	if int(time[2]) > 0:
		 mins = int(time[2]) * 10 + int(time[3])
	else:
		mins = int(time[3])
	cron = CronTab(user='<<name of Raspberry Pi account>>')
	job = cron.new(command='python <<path>>/checkforcoffee.py -n', comment='start coffee')
	job.hour.on(hour)
	job.minute.on(mins)
	cron.write()
	voice.send_sms("+1<<phone number from which you will be sending commands -- including area code>>","Executing " + reply)
	return 1

def makeCoffee(cmd):
	log = ''
	sms = ''
	write = 0
	if len(cmd) == 1:
		log = 'Instant made coffee from cell at ' + str(datetime.now())
		sms = "Coffee auto started from cell\nStarting a 15 minute shut off timer."
	else:
		extra = ''
		for x in cmd[1:]:
			extra = extra + ' ' + x
		log = 'Instant made coffee from cell at ' + str(datetime.now()) + '\n	Extra arguments: ' + extra
		sms = "Coffee auto started from cell\nStarting a 15 minute shut off timer.\nExtra arguments were: " + extra

        buff = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://<<IP of NodeJS server>>:<<port of NodeJS server HTTP connections>>/devices/<<Sonoff WiFi switch device name>>/status')
        c.setopt(c.WRITEDATA, buff)
        c.perform()
        c.close()
        body = buff.getvalue()

        c = pycurl.Curl()
        if buff.getvalue() == '0':
                c.setopt(c.URL, 'http://<<IP of NodeJS server>>:<<port of NodeJS server HTTP connections>>/devices/<<Sonoff WiFi switch device name>>/on')
                c.setopt(c.WRITEDATA, buff)
                log = log + ' | Turned on relay'
                d = datetime.now()
                t = d.minute + 15
                cron = CronTab(user='pi')
                job = cron.new(command='python <<path>>/checkforcoffee.py -n', comment='start coffee')
                job.minute.on(t)
                cron.write()
        else:
                c.setopt(c.URL, 'http://<<IP of NodeJS server>>:<<port of NodeJS server HTTP connections>>/devices/<<Sonoff WiFi switch device name>>/off')
                c.setopt(c.WRITEDATA, buff)
                log = log + ' | Turned off relay'
                sms = ''
		cancCoff(0)
        c.perform()
        c.close()

	if log != '':
		myFile = open('<<path>>/log.txt','a')
		myFile.write('\n' + log)
	if sms != '':
		voice.send_sms("+1<<phone number from which you will be sending commands -- including area code>>", sms)

	return 1

def cancCoff(text):
	log = ''
	sms = ''
	delete = 0
	cron = CronTab(user='<<name of Raspberry Pi account>>')
	for job in cron:
	        if job.comment == 'start coffee':
			delete = 1
                	cron.remove(job)
	if delete == 1 and text == 1:
	        cron.write()
		log = 'Canceled all scheduled coffee at ' + str(datetime.now())
		sms = "Canceling all scheduled coffee."
	elif text == 1:
		log = 'Attempted to cancel scheduled coffee, but none scheduled at ' + str(datetime.now())
		sms = "No coffee currently scheduled."
	elif text == 0:
		log = "Coffee finished at " + str(datetime.now())
                sms = "Coffee finished"

	if log != '' and sms != "":
		myFile = open('<<path>>/log.txt', 'a')
		myFile.write('\n' + log)
		voice.send_sms("+1<<phone number from which you will be sending commands -- including area code>>", sms)
	return 1

def incorrectPhrase(cmd):
	write = 0
	myFile = open('<<path>>/log.txt','a')
	reply = ''
	for x in cmd:
		reply = reply + x + ' '
	while write == 0:
		myFile.write('\nIncorrect phrase attempted at ' + str(datetime.now()) + '\n	Phrase attempted: ' + reply)
		write = 1
	voice.send_sms("+1<<phone number from which you will be sending commands -- including area code>>","Incorrect phrase attempted: " + reply)
	return 1;

def execCmd(cmd):
	complete = 0
	if str(cmd[0]).lower() == 'coffee':
		complete = makeCoffee(cmd)
	elif len(cmd) > 1 and str(cmd[0]+cmd[1]).lower() == 'schedulecoffee':
		complete = schedCoff(cmd)
	elif str(cmd[0]).lower() == 'cancel':
		complete = cancCoff(1)
	else:
		complete = incorrectPhrase(cmd)
	return complete

def deleteMessages():
	for message in voice.sms().messages:
        	message.delete()

voice = Voice()
voice.login('<<email which Pi uses to receive texts>>', '<<password of email address>>')

voice.sms()


if __name__ == '__main__':
	text = []
	cmd = []
	tmp = []

        if len(sys.argv) < 2:
		for msg in extractsms(voice.sms.html):
			if str(msg[u'from']) == '+1<<phone number from which you will be sending commands -- including area code>>:':
				for word in msg[u'text'].split(' '):
					cmd.append(word)
				if execCmd(cmd) == 1:
					deleteMessages()

        elif len(sys.argv) >= 2:
                for i in sys.argv[1:]:
                        tmp.append(i)

                if tmp[0].lower() == '-n':
                        cmd.append('coffee')
                elif tmp[0].lower() == '-s':
                        time = tmp[1]
			for x in ['schedule', 'coffee', time]:
	                        cmd.append(x)
		elif tmp[0].lower() == '-c':
			cmd.append('cancel')

                execCmd(cmd)
