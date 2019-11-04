import requests, json, time, random

class BotClimate:
    print('DEBUG CORE: Initializing Climate Bot...')
    enabled = True

    cache_responses = [
        'Fala mestre',
        'Po, uma bagona monstra, né não mestre, mas xofala',
        'Então gurizão',
        'Fala meus pentelhos',
        'Meus obliterados',
        'Então meu cheetos bola',
        'Fala amor da minha vida',
    ]

    def climate(self, mode, bot):
        if not self.enabled:
            bot.get_message('Clima desabilitado temporariamente')
            return

        if mode == 'now':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6259/current?token=e89a9dfc71c314242b10d99ff380ab4a')
        elif mode == 'region':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/region/sul?token=e89a9dfc71c314242b10d99ff380ab4a')
        else:
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/city?name=Umuarama&state=PR/days/15?token=e89a9dfc71c314242b10d99ff380ab4a')

        if req:
            climates = json.loads(req.text)

            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + '\n')

            if mode == 'region':
                new = 'Dados de clima para a região *' + climates['region'] + '*:\n'
                bot.get_message(new)

                for clima in climates['data']:
                    titulo = clima['date_br']
                    image = clima['image']
                    text = clima['text']

                    new = '*%s* - %s\n' % (titulo ,text)

                for part in new.split('\n'):
                    bot.get_message_with_one_space(part)

            elif mode == 'now':
                clima = climates['data']

                new = 'Clima para o dia *' + clima['date'] + '* para a cidade de *' + climates['name'] + '*:\n'
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

    def command(self, arg):
        self.enabled = True if arg == 'true' else False
        
    print('DEBUG CORE: Climate Bot Initialized...')
