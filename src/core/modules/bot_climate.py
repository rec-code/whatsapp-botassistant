import requests, json, time

class BotClimate:
    def climate(self, mode, bot):
        if mode == 'now':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6259/current?token=e89a9dfc71c314242b10d99ff380ab4a')
        elif mode == 'region':
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/region/sul?token=e89a9dfc71c314242b10d99ff380ab4a')
        else:
            req = requests.get(
                'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/city?name=Umuarama&state=PR/days/15?token=e89a9dfc71c314242b10d99ff380ab4a')

        climates = json.loads(req.text)

        try:
            if mode == 'region':
                new = 'Dados de clima para a região ' + climates['region'] + ':\n'
                bot.caixa_de_mensagem.send_keys(new)

            for clima in climates['data']:
                titulo = clima['date_br']
                image = clima['image']
                text = clima['text']

                new = titulo + ' - ' + text + '\n'

                bot.caixa_de_mensagem.send_keys(new)
        except:
            pass