import time, wget, win32clipboard, random
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class BotImages:
	print('DEBUG CORE: Initializing Image Bot...')
	enabled = True

	retrieve_times_allowed = 3
	current_timeout = 1

	def try_download_image(self, images_links, bot):
		temp_rand_image = random.randint(0, len(images_links) - 1)
		link = images_links[temp_rand_image]
		temp_image = None

		try:
			print('DEBUG LOG: Trying download image: %s... - attempt %s...' % (link[len(link)-50:], self.current_timeout))
			temp_image = wget.download(link, bot.dir_path + '\\media\\images')

			if temp_image[len(temp_image)-5:] == '.wget':
				print('\nDEBUG LOG: Image with .wget format')
				raise Exception('Invalid image format data')

			print('\nDEBUG LOG: Image downloaded succesfully on attempt %s...' % self.current_timeout)
		except:
			if self.current_timeout < (self.retrieve_times_allowed * 3):
				self.current_timeout += 1
				print('DEBUG LOG: Image %s not downloaded succesfully, trying another, attempt %s...' % (link[len(link)-50:], self.current_timeout))
				return self.try_download_image(images_links, bot)

		if temp_image is None:
			print('DEBUG LOG: Failed to download the image...')
		
		self.current_timeout = 1

		return temp_image

	def get_elements_images(self, image_name, bot, message):
		success = False

		try:
			print('DEBUG LOG: Trying get images elements, attempt %s...' % self.current_timeout)
			image = Image.open(image_name)

			output = BytesIO()
			image.convert("RGB").save(output, "BMP")
			data = output.getvalue()[14:]
			output.close()

			self.send_to_clipboard(win32clipboard.CF_DIB, data)
			ActionChains(bot.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

			print('DEBUG LOG: Images elements get succesfully on attempt %s...' % self.current_timeout)
			success = True
		except:
			if self.current_timeout < self.retrieve_times_allowed:
				time.sleep(.5)
				self.current_timeout += 1
				print('DEBUG LOG: Failed to get images elements, trying again, attempt %s...' % self.current_timeout)
				self.get_elements_images(image_name, bot, message)
				return

		if self.current_timeout == self.retrieve_times_allowed:
			print('DEBUG LOG: Failed to get images elements...')

		if success:
			self.send_image(bot, message)

		self.current_timeout = 1

	def send_image(self, bot, message):
		time.sleep(1)

		try:
			print('DEBUG LOG: Trying send images, attempt %s...' % self.current_timeout)
			#bot.driver.find_element_by_xpath("(//DIV[@class='_3u328 copyable-text selectable-text'])[1]").send_keys(message)
			#time.sleep(.5)
			bot.driver.find_element_by_xpath("//SPAN[@data-icon='send-light']").click()
			print('DEBUG LOG: Image sended succesfully on attempt %s...' % self.current_timeout)
		except:
			if self.current_timeout < self.retrieve_times_allowed:
				time.sleep(.5)
				self.current_timeout += 1
				print('DEBUG LOG: Failed to send image, trying again, attempt %s...' % self.current_timeout)
				time.sleep(.5)
				self.send_image(bot, message)
				return

		if self.current_timeout == self.retrieve_times_allowed:
			print('DEBUG LOG: Failed to send image...')

		self.current_timeout = 1

	def send_to_clipboard(self, clip_type, data):
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(clip_type, data)
		win32clipboard.CloseClipboard()

	def command(self, arg):
		self.enabled = True if arg == 'true' else False

	print('DEBUG CORE: Image Bot Initialized...')
