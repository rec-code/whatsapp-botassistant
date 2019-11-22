from core.bot_modules_core import BotModulesCore 
from googleapiclient.discovery import build

class BotGoogle(BotModulesCore):
	
	def __init__(self, name):
		super(BotGoogle, self).__init__(name)

	googleInfos = {
		'apiKey': 'yourkey',
		'searchEngineId': 'yoursearchengine'
	}

	googleService = build(
		"customsearch", 
		"v1", 
		developerKey=googleInfos['apiKey'])

	retrieve_times_allowed = 3
	current_timeout = 1

	def base_search(self, message, q_limit, search_type, bot):
		try:
			if search_type == 'image':
				res = self.googleService.cse().list(
					q=message, 
					cx=self.googleInfos['searchEngineId'],
					searchType=search_type,
					num=int(q_limit),
					start=10
				).execute()
			else:
				res = self.googleService.cse().list(
					q=message, 
					cx=self.googleInfos['searchEngineId'],
					num=int(q_limit),
				).execute()

		except ConnectionResetError:
			if self.current_timeout < self.retrieve_times_allowed:
				bot.bot_main.printi('Google connection reseted, restarting, attempt %s' % self.current_timeout, 'inline')
				self.current_timeout += 1
				return self.base_search(message, q_limit, search_type, bot)
			else:
				bot.get_message('Buguei monstro parçaaaaa, chama o bombeiro\nZoas, mas se pá atingi minha cota máxima de pesquisas no dia... <3')
				return None

		self.current_timeout = 1
		return res

	def search(self, message, bot):
		if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
			bot.get_message('Google Pesquisas desabilitado temporariamente <3')
			return

		res = self.base_search(message, 4, None, bot)

		if 'items' in res:
			bot.get_message('Resultados no tio Google para *%s*:' % message)

			temp_items = res['items']
			temp_count = 0

			for item in temp_items:
				temp_snippet = item['snippet'].replace('\n', '')
				bot.get_message_with_two_spaces('%s -  %s' % (temp_count, temp_snippet))
				bot.get_message(item['link'])
				
				temp_count += 1

		else:
			bot.get_message('Não achei nenhum resultado na net de *%s*, malz mestre <3' % message)

	def search_image(self, message, bot):
		if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
			bot.get_message('Google Pesquisas Imagens desabilitado temporariamente <3')
			return

		success = False
		temp_images = [] 
		temp_number = None
		temp_message = ''

		for m in message.split('-'):
			try:
				temp_number = int(m)
			except:
				temp_message += m
		
		temp_links = []

		res = self.base_search(message, 10, 'image', bot)

		if 'items' in res:
			temp_items = res['items']

			for item in temp_items:
				temp_links.append(item['link'])
	
		temp_number = 1 if not temp_number else temp_number

		if temp_number != 1:
			n = 2
			l =  temp_links
			tp_lks = (l[i:i+n] for i in range(0, len(l), n))
			counter = 0

			for i in tp_lks:
				i = bot.try_download_image(i, 2)
				
				if len(i) != 0:
					for k in i:
						counter += 1
						temp_images.append(k)

					if counter > temp_number:
						try:
							del i[1]
						except IndexError:
							pass

					bot.get_elements_images(i, message)

					if counter > temp_number:
						break
		else:
			temp_images = bot.try_download_image(temp_links, 1)
			bot.get_elements_images(temp_images, message)

		if len(temp_images) != 0:
			success = True

		if not success:
			bot.get_message('Não achei nenhuma foto na net de *%s*, malz mestre <3' % message)