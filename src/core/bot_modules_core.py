from sys import stdout
from datetime import datetime

class BotModulesCore():
	def __init__(self, name):
		self.bot_name = name + ' Bot'
		self.black_list = []
		self.enabled = True
		self.printi('Initializing %s' % self.bot_name, 'core')
		self.printi('%s Initialized' % self.bot_name, 'core')
	
	def command(self, arg):
		self.enabled = True if arg == 'true' else False

	def set_black_list(self, conv, bot):
		if conv not in self.black_list:
			self.black_list.append(conv)
			temp_label = 'added to'
		else:
			temp_label = 'removed of'
			self.black_list.remove(conv)

		temp_debug = 'Conversation \'%s\' - %s the black list of %s!' % (conv, temp_label, self.bot_name)
		bot.get_message(temp_debug)
		bot.bot_main.printi(temp_debug, 'core')

	def is_in_black_list(self, current):
		return True if current in self.black_list else False

	def get_time(self):
		return datetime.now().strftime('%X')

	def printi(self, log, *args):
		level_debug = 'LOG'
		inline = False
		temp_label = '%s - DEBUG %s: %s'

		for i in args:
			if i == 'inline':
				inline = True
			elif i == 'core':
				level_debug = 'CORE'

		debug = temp_label % (self.get_time(), level_debug, log)
		
		start_time = str(datetime.now().strftime('%x')).replace('/', '-')
		with open('debug\\debug-%s.txt' % start_time,'a') as file:
			file.write(str(debug+'\n'))

		if inline:
			stdout.write(debug + str(' ' * (50 - len(log))) + '\r')
			stdout.flush()
		else:
			print(debug)