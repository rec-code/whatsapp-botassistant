import time, pyautogui, wget, win32clipboard
from io import BytesIO
from PIL import Image
from googleapiclient.discovery import build

class BotGoogle:
	print('DEBUG CORE: Initializing Google Bot...')
	enabled = True

    # you have to put your google api infos here
	googleInfos = {
		'apiKey': 'YOURGOOGLEAPIKEY',
		'searchEngineId': 'YOURGOOGLESEARCHENGINEID'
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
			bot.get_message('Google Pesquisas desabilitado temporariamente')
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
			bot.get_message('Buguei monstro parçaaaaa, chama o bombeiro\nZoas, mas se pá atingi minha cota máxima de pesquisas no dia...')

	def search_image(self, message, is_link, url, bot):
		if not self.enabled:
			bot.get_message('Google Pesquisas Imagens desabilitado temporariamente')
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
					num=1
				).execute()

				if 'items' in res:
					temp_items = res['items']

					for item in temp_items:
						temp_links.append(item['link'])

			else:
				temp_links.append(url)

			for link in temp_links:
				try:
					print('DEBUG LOG: Trying download image: %s...' % link[:50])
					temp_image = wget.download(link, bot.dir_path + '\\images')
					print('\nDEBUG LOG: Image downloaded succesfully...')
					break
				except:
					print('\nDEBUG LOG: Image %s not downloaded succesfully, trying another...' % link)

			if temp_image:
				success = True
		except:
			bot.get_message('Buguei *\'- \'*\nZoas, mas se pá atingi minha cota máxima de pesquisas no dia...')

		if success:
			temp_image = temp_image.replace('/', '\\')
			self.get_elements_images(temp_image, bot, message)
		else:
			bot.get_message('Não achei nenhuma foto na net de *%s* ou a função foi desabilitada temporariamente, malz, mestre' % message)

	def get_elements_images(self, image_name, bot, message):
		success = False

		try:
			print('DEBUG LOG: Trying get images elements...')
			image = Image.open(image_name)

			output = BytesIO()
			image.convert("RGB").save(output, "BMP")
			data = output.getvalue()[14:]
			output.close()

			self.send_to_clipboard(win32clipboard.CF_DIB, data)
			pyautogui.hotkey('ctrl', 'v')

			print('DEBUG LOG: Images elements get succesfully...')
			success = True
		except:
			if self.current_timeout < 3:
				time.sleep(.5)
				self.current_timeout = self.current_timeout + 1
				print('DEBUG LOG: Failed to get images elements, trying again, attempt %s...' % self.current_timeout)
				self.get_elements_images(image_name, bot, message)
				return

		if self.current_timeout == 3:
			print('DEBUG LOG: Failed to get images elements...')

		if success:
			self.send_image(bot, message)

		self.current_timeout = 1

	def send_image(self, bot, message):
		try:
			time.sleep(.5)
			print('DEBUG LOG: Trying send image...')
			bot.driver.find_element_by_xpath("(//DIV[@class='_3u328 copyable-text selectable-text'])[1]").send_keys(message)
			time.sleep(.5)
			bot.driver.find_element_by_xpath("//SPAN[@data-icon='send-light']").click()
			print('DEBUG LOG: Image sended succesfully...')
		except:
			if self.current_timeout < 3:
				time.sleep(.5)
				self.current_timeout = self.current_timeout + 1
				print('DEBUG LOG: Failed to send image, trying again, attempt %s...' % self.current_timeout)
				self.send_image(bot, message)
				return

		if self.current_timeout == 3:
			print('DEBUG LOG: Failed to send image...')

		self.current_timeout = 1

	def send_to_clipboard(self, clip_type, data):
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(clip_type, data)
		win32clipboard.CloseClipboard()

	def command(self, arg):
		self.enabled = True if arg == 'true' else False

	print('DEBUG CORE: Google Bot Initialized...')
