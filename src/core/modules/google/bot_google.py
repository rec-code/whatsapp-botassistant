from googleapiclient.discovery import build

class BotGoogle:
	print('DEBUG CORE: Initializing Google Bot...')
	enabled = True

	googleInfos = {
		'apiKey': 'YOURKEY',
		'searchEngineId': 'YOURSENGINE'
	}
	
	googleService = build(
		"customsearch", 
		"v1", 
		developerKey=googleInfos['apiKey'])

	retrieve_times_allowed = 3
	current_timeout = 1

	def search(self, message, bot):
		# bot.get_message('Recurso desabilitado temporariamente...')
		# return
		if not self.enabled:
			bot.get_message('Google Pesquisas desabilitado temporariamente <3')
			return

		try:
			res = self.googleService.cse().list(
				q=message, 
				cx=self.googleInfos['searchEngineId'],
				num=4
			).execute()

			if 'items' in res:
				bot.get_message('Resultados no tio Google para *%s*:' % message)

				temp_items = res['items']
				temp_count = 0

				for item in temp_items:
					temp_snippet = item['snippet'].replace('\n', '') 
					bot.get_message('%s -  %s \n%s' % (temp_count, temp_snippet, item['link']))
					temp_count = temp_count + 1
		except:
			bot.get_message('Buguei monstro parçaaaaa, chama o bombeiro\nZoas, mas se pá atingi minha cota máxima de pesquisas no dia... <3')

	def search_image(self, message, is_link, url, bot):
		if not self.enabled:
			bot.get_message('Google Pesquisas Imagens desabilitado temporariamente <3')
			return

		success = False
		temp_image = None

		try:
			temp_links = []

			if not is_link:
				res = self.googleService.cse().list(
					q=message, 
					cx=self.googleInfos['searchEngineId'],
					searchType='image',
					num=10
				).execute()

				if 'items' in res:
					temp_items = res['items']

					for item in temp_items:
						temp_links.append(item['link'])

			else:
				temp_links.append(url)

			temp_image = bot.try_download_image(temp_links)

			if temp_image:
				success = True
		except:
			pass

		if success:
			temp_image = temp_image.replace('/', '\\')
			bot.get_elements_images(temp_image, message)
		else:
			bot.get_message('Não achei nenhuma foto na net de *%s* ou a função foi desabilitada temporariamente, malz, mestre <3' % message)

	def command(self, arg):
		self.enabled = True if arg == 'true' else False

	print('DEBUG CORE: Google Bot Initialized...')
