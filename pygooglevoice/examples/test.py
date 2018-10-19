from googlevoice import Voice,util


voice = Voice()
voice.login('rpifritzemeier@gmail.com','Crown87InfernalPigeon')

number = '+16056514032'
folder = voice.search(util.input() = '+16056514032')

util.print_('Found %s messages: ', len(folder))
util.pprint(folder.messages)
