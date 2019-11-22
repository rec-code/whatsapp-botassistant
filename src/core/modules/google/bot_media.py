from core.bot_modules_core import BotModulesCore 
from selenium.common.exceptions import NoSuchElementException

class BotMedia(BotModulesCore):

	def __init__(self, name):
		super(BotMedia, self).__init__(name)

	def search(self, message, domain_search, bot):
		if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
			return

		temp_domain_search = domain_search.replace('music.', '')

		res = bot.google_b().base_search('%s %s' % (temp_domain_search, message), 6, '', bot)
				
		temp_link = []

		if 'items' in res:
			for t in res['items']:
				if temp_domain_search in t['link']:
					temp_link.append(t['link'])

		if len(temp_link) != 0:
			tp_link = temp_link[0]
			
			if 'music' in domain_search:
				tp_link = tp_link.replace('https://www.youtube', 'https://music.youtube')
				
				if not 'channel' in tp_link:
					tp_link += '&list=RDAMVM' + tp_link.split('?')[1][2:]

			bot.get_message_with_keys(tp_link)

			temp_parent = bot.driver.find_element_by_xpath('//DIV[@class=\'_30sf0\']')
			thumb = None

			temp_counter = 0

			while thumb is None and temp_counter < 15:
				try:
					thumb = temp_parent.find_element_by_xpath('//DIV[@class=\'_1ebw2\']')
				except NoSuchElementException:
					pass

				temp_counter += .01

			bot.send_message()
		else:
			temp_response = 'Então truta, algo errado deu e não consegui acha o vídeo no youtube, tlg... Tenta uns termos mais sucintos ae'

			if 'soundcloud' in domain_search:
				temp_response = 'Então vei, não dei conta de acha essa track no soundcloud, foi mal'
			elif 'music' in domain_search:
				temp_response = 'O youtube music caiu, o Ministro da Magia está morto. Eles estão vindo'
			elif 'spotify' in domain_search:
				temp_response = 'Então truta, se pá o spotify não curte essa música, vei... Nem achei'
			
			bot.get_message(temp_response)