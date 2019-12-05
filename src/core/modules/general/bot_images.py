import time, wget, win32clipboard, random
#import time, wget, random

from selenium.common.exceptions import NoSuchElementException
from core.bot_modules_core import BotModulesCore 
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from urllib.error import HTTPError, URLError


class BotImages(BotModulesCore):
	def __init__(self, name, bot):
		super(BotImages, self).__init__(name, bot)

	retrieve_times_allowed = 3
	current_timeout = 1

	def try_download_image(self, images_links, amount, bot):
		temp_image = []

		count = 0

		while count < amount and len(images_links) != 0:
			tp_rd = random.randint(0, len(images_links) - 1)
			link = images_links[tp_rd]
			images_links.remove(link)
			
			tp_img = self.try_download(link, bot.root_path + 'media/images', bot)

			if tp_img is not None:
				if tp_img[len(tp_img)-5:] == '.wget':
					self.printi('Image with .wget format', 'inline')
					#raise Exception('Invalid image format data')
					continue

				count += 1

				# if amount > 1:
				temp_image.append(tp_img)
				# else:
				# 	temp_image = tp_img

				self.printi('Image downloaded succesfully on attempt %s' % self.current_timeout, 'inline')
			else:
				continue

		if len(temp_image) == 0:
			self.printi('Failed to download the image')
		
		self.current_timeout = 1

		return temp_image

	def try_download(self, link, path, bot):
		tp_img = None

		try:
			self.printi('Trying download image: %s' % link[len(link)-20:], 'inline')
			tp_img = wget.download(link, path)
		except (URLError, HTTPError) as e:
			self.printi('Image %s not downloaded succesfully, trying another' % link[len(link)-20:], 'inline')
			
		return tp_img

	def get_elements_images(self, images_names, bot, message):
		success = False

		# try:
		count = 0

		while count < len(images_names):
			self.printi('Trying get images elements, attempt %s' % self.current_timeout, 'inline')

			try:
				image = Image.open(images_names[count])
			except IOError:
				self.printi('Bones for this image')
				count += 1
				continue

			if self.bot.system != 'Linux':
				output = BytesIO()
				image.convert("RGB").save(output, "BMP")
				data = output.getvalue()[14:]
				output.close()
				self.send_to_clipboard(win32clipboard.CF_DIB, data)
				
				ActionChains(bot.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
			else:
				self.printi('Getting galery_button')
				media_button = bot.driver.find_element_by_css_selector('div._2kYeZ').find_elements_by_css_selector('div._3j8Pd')[1]
				media_button.click()

				self.printi('Button clicked')
				galery_button = None
				temp_counter = 0
				self.printi('Clicking on media button')
				
				temp_link = images_names[count].replace('/', '\\').replace('\\mnt\\d', 'd:')
				#clipboard.copy(temp_link)

				while galery_button is None and temp_counter < 15:
					try:
						galery_button = media_button.find_element_by_xpath('(//BUTTON[@class=\'Ijb1Q\'])[1]')
						self.printi('Media button founded, opening windows explorer')
						galery_button.send_keys(temp_link)
						#galery_button.click()
					except NoSuchElementException:
						pass

					temp_counter += .01
				
				handle = "[CLASS:#32770; TITLE:Open]"
				autoit.win_wait(handle, 60)
				autoit.control_set_text(handle, "Edit1", temp_link)
				autoit.control_click(handle, "Button1")
			#subprocess.call([self.bot.root_path + 'src/start_test.bat'])
			
			#clipboard.paste()

			#self.send_to_clipboard(win32clipboard.CF_DIB, data)
			
			#ActionChains(bot.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

			self.printi('Images elements get succesfully on attempt %s' % self.current_timeout, 'inline')
			success = True
			count += 1
			time.sleep(1)
		#except:
			# if self.current_timeout < self.retrieve_times_allowed:
			# 	time.sleep(.5)
			# 	self.current_timeout += 1
			# 	print('DEBUG LOG: Failed to get images elements, trying again, attempt %s...' % self.current_timeout)
			# 	self.get_elements_images(images_names, bot, message)
			# 	return

		if self.current_timeout == self.retrieve_times_allowed:
			self.printi('Failed to get images elements')

		if success:
			self.send_image(bot, message)

		self.current_timeout = 1

	def send_image(self, bot, message):
		try:
			self.printi('Trying send images, attempt %s' % self.current_timeout, 'inline')
			#bot.driver.find_element_by_xpath("(//DIV[@class='_3u328 copyable-text selectable-text'])[1]").send_keys(message)
			#time.sleep(.5)
			# bot.driver.find_element_by_xpath("//SPAN[@data-icon='send-light']").click()
			ActionChains(bot.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
			self.printi('Image sended succesfully on attempt %s' % self.current_timeout, 'inline')
		except:
			if self.current_timeout < self.retrieve_times_allowed:
				time.sleep(.5)
				self.current_timeout += 1
				self.printi('Failed to send image, trying again, attempt %s' % self.current_timeout)
				time.sleep(.5)
				self.send_image(bot, message)
				return

		if self.current_timeout == self.retrieve_times_allowed:
			self.printi('Failed to send image')

		self.current_timeout = 1

	def send_to_clipboard(self, clip_type, data):
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(clip_type, data)
		win32clipboard.CloseClipboard()