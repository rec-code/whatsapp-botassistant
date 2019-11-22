import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from core.bot_modules_core import BotModulesCore 

class BotWatson(BotModulesCore):

	def __init__(self, name):
		super(BotWatson, self).__init__(name)
		
		self.watson_preferences = {
			'api_key': 'yourkey',
			'assistant_id': 'yourassistantid',
			'service_url': 'https://gateway.watsonplatform.net/assistant/api',
			'version': '2019-02-28'
		}

		#self.session = {}

		self.authenticator = IAMAuthenticator(self.watson_preferences['api_key'])

		self.service = AssistantV2(
			version=self.watson_preferences['version'],
			authenticator=self.authenticator
		)

		self.service.set_service_url(self.watson_preferences['service_url'])

		print('DEBUG CORE: WATSON SERVICE STARTED')

		# response = service.delete_session(
		# assistant_id='yourkey',
		# session_id=session['session_id']
		# ).get_result()

		# print('SESSION DELETED')

	def answer(self, message, bot):
		if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
			bot.get_message('Onikkatson desabilitado temporariamente')
			return

		try:
			response = self.service.message(
				assistant_id=self.watson_preferences['assistant_id'],
				session_id=self.session['session_id'],
				input={
					'message_type': 'text',
					'text': message
				}
			).get_result()

			text_result = response['output']['generic'][0]['text']

			# if len(response['output']['generic']) > 1 and response['output']['generic'][1]['response_type'] == 'image':
			# 	image_source = response['output']['generic'][1]['source']
			# 	bot.google_b().search_image(text_result, True, image_source, bot)
			# else:
			# 	bot.get_message(text_result)

			print('THE BOT SAYS: ', response)

		except:
			print('DEBUG CORE: WATSON SESSION EXPIRED')
			self.session = self.create_session()
			self.answer(message, bot)

	def create_session(self):
		print('DEBUG CORE: CREATING A WATSON SESSION')

		return self.service.create_session(
			assistant_id=self.watson_preferences['assistant_id'],
		).get_result()

		print('DEBUG CORE: WATSON SESSION CREATED, ID: ', self.session['session_id'])

	def command(self, arg):
		self.enabled = True if arg == 'true' else False

	def is_in_black_list(self, current):
		return True if current in self.black_list else False