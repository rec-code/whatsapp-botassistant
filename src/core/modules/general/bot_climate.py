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

        # you have to put your token of climatempo api here to climate work
        if mode == 'now':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6259/current?token=YOURTOKENHERE')
        elif mode == 'region':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/region/sul?token=YOURTOKENHERE')
        else:
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/city?name=Umuarama&state=PR/days/15?token=YOURTOKENHERE')

        climates = json.loads(req.text)

        bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + '\n')
        time.sleep(.5)

        if mode == 'region':
            new = 'Dados de clima para a região ' + climates['region'] + ':\n'
            bot.get_message(new)

            for clima in climates['data']:
                titulo = clima['date_br']
                image = clima['image']
                text = clima['text']

                new = titulo + ' - ' + text + '\n'

                bot.get_message(new)

        elif mode == 'now':
            clima = climates['data']

            new = 'Clima para o dia *' + clima['date'] + '* para a cidade de *' + climates['name'] + '*:\n'
            new += '*Temperatura*: %s' % clima['temperature'] + 'º\n'
            new += '*Direção do vento*: %s' % clima['wind_direction'] + '\n'
            new += '*Velocidade do vento*: %s' % clima['wind_velocity'] + '\n'
            new += '*Umidade*: %s' % clima['humidity'] + '%\n'
            new += '*Condição climática*: %s' % clima['condition'] + '\n'
            new += '*Pressão atmosférica*: %s' % clima['pressure'] + '\n'
            new += '*Sensação térmica*: %s' % clima['sensation'] + 'º\n'

            time.sleep(.5)
            bot.get_message(new)

    def command(self, arg):
        self.enabled = True if arg == 'true' else False
        
    print('DEBUG CORE: Climate Bot Initialized...')
