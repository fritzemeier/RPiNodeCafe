from googlevoice import Voice

voice = Voice()
voice.login('rpifritzemeier@gmail.com','Crown87InfernalPigeon')

for message in voice.sms().messages:
	if message.isRead:
		message.delete()
