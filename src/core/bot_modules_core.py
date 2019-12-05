import xml.etree.cElementTree as ET

from sys import stdout
from datetime import datetime

# Mine
from functions import Functions

class BotModulesCore(Functions):
	def __init__(self, name, bot):
		self.my_name = 'Ônikka'
		self.bot_name = name + ' Bot'
		self.bot = bot
		self.printi('Initializing %s' % self.bot_name, 'core')

		temp_path = self.get_database_bl_path = self.bot.root_path + "databases/blacklists/%s.xml" % name.lower()
		self.black_list = []

		self.load_database(temp_path)

		self.enabled = True
		self.printi('%s Initialized' % self.bot_name, 'core')
	
	def command(self, arg):
		self.enabled = True if arg == 'true' else False

	def set_black_list(self, conv, bot):
		if conv not in self.black_list:
			self.black_list.append(conv)
			temp_label = 'added to'
			added = True
		else:
			self.black_list.remove(conv)
			temp_label = 'removed of'
			added = False

		temp_debug = '\'%s\' - %s the %s black list!' % (conv, temp_label, self.bot_name)
		
		if bot is not None:
			self.save_database(conv, added)
			bot.get_message(temp_debug)
		
		self.printi(temp_debug, 'core')

	def load_database(self, path):
		try:
			tree = ET.parse(path)
			root = tree.getroot()

			for lst in root:
				self.set_black_list(lst.attrib['conv_name'], None)

			temp_log = 'Black list of %s loaded' % self.bot_name
		except FileNotFoundError:
			root = ET.Element('black_list')

			#ET.SubElement(root, 'conv_name', conv_name=)

			ET.ElementTree(root).write(path, encoding="UTF-8", xml_declaration=True)
			temp_log = 'Black list file of %s not found, creating one' % self.bot_name

			self.printi(temp_log)

	def save_database(self, name, added):
		tree = ET.parse(self.get_database_bl_path)
		root = tree.getroot()

		if added:
			conv_name = ET.SubElement(root, 'conv', conv_name=name)
		else:
			for c in root:
				if c.attrib['conv_name'] == name:
					root.remove(c)
					break

		tree = ET.ElementTree(root)
		tree.write(self.get_database_bl_path, encoding="UTF-8", xml_declaration=True)
		self.printi('%s saved to %s black list database' % (name, self.bot_name))

	def is_in_black_list(self, current):
		return True if current in self.black_list else False