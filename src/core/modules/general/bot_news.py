import requests, json, time, random


class BotNews:
    print('DEBUG CORE: Initializing News Bot...')
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
    
    # you have to put your key of newsapi to news work
    def news_tech(self, bot):
        if not self.enabled:
            bot.get_message('Notícias de Tecnologias desabilitadas temporariamente')
            return

        req = requests.get(
            'https://newsapi.org/v2/top-headlines?country=br&category=technology&pageSize=6&apiKey=YOURKEYHERE')
        noticias = json.loads(req.text)

        try:
            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', as noticias de tecnologias ae:\n' )
            time.sleep(.5)
            for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                new = 'Domi: ' + titulo + ' ' + link + '\n'

                bot.get_message(new)
                time.sleep(.5)
        except:
            time.sleep(1)
            print('DEBUG LOG: Can\'t get tech news, retrying: %s' % user_message)
            self.news_tech(bot)

    def news(self, top_br, bot):
        if not self.enabled:
            bot.get_message('Notícias desabilitadas temporariamente')
            return

        if top_br:
            req = requests.get(
                'https://newsapi.org/v2/top-headlines?country=br&pageSize=6&apiKey=YOURKEYHERE')
        else:
            if random.randint(0, 2) == 0:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=google-news-br&pageSize=6&apiKey=YOURKEYHERE')
            else:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=globo&pageSize=6&apiKey=fYOURKEYHERE')

        noticias = json.loads(req.text)

        try:
            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', as noticias ae:\n' )
            time.sleep(.5)
            for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                new = 'Domi: ' + titulo + ' ' + link + '\n'

                bot.get_message(new)
                time.sleep(1)
        except:
            time.sleep(1)
            print('DEBUG LOG: Can\'t get news, retrying: %s' % user_message)
            self.news(top_br, bot)
            
    def command(self, arg):
        self.enabled = True if arg == 'true' else False

    print('DEBUG CORE: News Bot Initialized...')
