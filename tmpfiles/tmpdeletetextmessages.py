from crontab import CronTab
from googlevoice import Voice

voice = Voice()
voice.login('<<email which Pi uses to receive texts>>','<<password of email address>>')

for message in voice.sms().messages:
	message.delete()
