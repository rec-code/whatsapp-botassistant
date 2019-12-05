from core.bot_modules_core import BotModulesCore 
import requests, json, time, random
import xml.etree.cElementTree as ET

class BotClimate(BotModulesCore):
    def __init__(self, name, bot):
        super(BotClimate, self).__init__(name, bot)

        self.get_database_credentials_path = self.bot.root_path + "databases/credentials.xml"

        tree = ET.parse(self.get_database_credentials_path)
        root = tree.getroot()

        for cred in root:
            if cred.attrib['name'] == 'climate':
                self.api_key_climate = cred[0].text
                self.printi('Climate credentials loaded', 'core')

    cache_responses = [
        'Fala mestre',
        'Po, uma bagona monstra, né não mestre, mas xofala',
        'Então gurizão',
        'Fala meu pentelho',
        'Meus obliterado',
        'Então meu cheetos bola',
        'Fala amor da minha vida',
    ]

    def climate(self, mode, region, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            bot.get_message('Clima desabilitado temporariamente')
            return

        if mode == 'now':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6259/current?token=%s' % self.api_key_climate)
        elif mode == 'region':
            if region == '':
                region = 'sul'
                
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/region/%s?token=%s' % (region, self.api_key_climate))
        else:
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/city?name=Umuarama&state=PR/days/15?token=%s' % self.api_key_climate)

        if req:
            climates = json.loads(req.text)

            new = self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + '\n'

            if mode == 'region':
                new += 'Dados de clima para a região *' + climates['region'] + '*:'

                for part in new.split('\n'):
                    bot.get_message_with_one_space(part)

                bot.send_message()

                for clima in climates['data']:

                    titulo = clima['date_br']
                    image = clima['image']
                    text = clima['text']

                    # temp_image = bot.try_download_image([image])

                    # if temp_image is not None:
                    #     bot.get_elements_images(temp_image, '')

                    new = '*%s* - %s\n' % (titulo ,text)

                    bot.get_message(new)

            elif mode == 'now':
                clima = climates['data']

                new += 'Clima para o dia *' + clima['date'] + '* para a cidade de *' + climates['name'] + '*:\n'
                bot.get_message(new)

                new = '*Temperatura*: %s' % clima['temperature'] + 'º\n'
                new += '*Direção do vento*: %s' % clima['wind_direction'] + '\n'
                new += '*Velocidade do vento*: %s' % clima['wind_velocity'] + '\n'
                new += '*Umidade*: %s' % clima['humidity'] + '%\n'
                new += '*Condição climática*: %s' % clima['condition'] + '\n'
                new += '*Pressão atmosférica*: %s' % clima['pressure'] + '\n'
                new += '*Sensação térmica*: %s' % clima['sensation'] + 'º\n'

                for part in new.split('\n'):
                    bot.get_message_with_one_space(part)

            bot.send_message()
        else:
            bot.get_message('Falha ao requisitar informações de tempo, tente novamente')