import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class BotWatsonImages():
	print('DEBUG CORE: Initializing Watson Image Bot...')
	enabled = True

	def __init__(self):
		self.watson_preferences = {
			'api_key': 'YOURKEY',
			'version': '2018-03-19'
		}

		self.authenticator = IAMAuthenticator(self.watson_preferences['api_key'])

		self.service = VisualRecognitionV3(
			version=self.watson_preferences['version'],
			authenticator=self.authenticator
		)

		self.service.set_default_headers({'x-watson-learning-opt-out': "true"})

		print('DEBUG CORE: WATSON IMAGE SERVICE STARTED')

	def recognize(self, bot, link):
		if not self.enabled:
			bot.get_message('Onikkatson images desabilitado temporariamente')
			return

		try:
			#temp_path = 
			#temp_image = wget.download(link, temp_path)

			temp_image = link
			print(temp_image)

			with open(temp_image, 'rb') as images_file:
				response = self.service.classify(
					images_file=images_file,
					accept_language='pt-br',
					#classifier_ids=["general"]
					).get_result()

				#print(json.dumps(response, indent=2))
				temp_label = ''

				for resp in response['images'][0]['classifiers'][0]['classes']:
					print(resp)

					temp_score = float(resp['score'])

					if temp_score >= .85:
						print(resp['class'])
						temp_label += ', ' + resp['class']

				temp_label = temp_label.replace(',', '', 1)
				temp_label = temp_label.strip()

				bot.get_message(temp_label)
				print('THE ONITSON RECOGNIZED THE IMAGE AS: ', temp_label)

		except:
			print('DEBUG LOG: Onikkatson images could not recognize this photo')

	def command(self, arg):
		self.enabled = True if arg == 'true' else False