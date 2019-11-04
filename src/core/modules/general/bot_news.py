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

    def news_tech(self, bot):
        if not self.enabled:
            bot.get_message('Notícias de Tecnologias desabilitadas temporariamente')
            return

        req = requests.get(
            'https://newsapi.org/v2/top-headlines?country=br&category=technology&pageSize=6&apiKey=f47086f0e00d43be9fe271e7e56b51db')
        noticias = json.loads(req.text)

        if noticias['articles']:
            # try:
            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', as noticias de tecnologias ae:\n' )
           
            for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                new = '*%s.* %s\n' % (titulo, link)

                bot.get_message(new)
            # except:
            #     time.sleep(1)
            #     print('DEBUG LOG: Can\'t get tech news, retrying: %s' % user_message)
            #     self.news_tech(bot)
        else:
            bot.get_message('Não consegui pega as noticias de tech truta, foi mal, tenta de novo ae...')

    def news(self, top_br, bot):
        if not self.enabled:
            bot.get_message('Notícias desabilitadas temporariamente')
            return

        if top_br:
            req = requests.get(
                'https://newsapi.org/v2/top-headlines?country=br&pageSize=6&apiKey=f47086f0e00d43be9fe271e7e56b51db')
        else:
            if random.randint(0, 2) == 0:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=google-news-br&pageSize=6&apiKey=f47086f0e00d43be9fe271e7e56b51db')
            else:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=globo&pageSize=6&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')

        noticias = json.loads(req.text)

        # try:
        if noticias['articles']:
            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', as noticias ae:\n')

            for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                new = '*%s.* %s\n' % (titulo, link)

                bot.get_message(new)
        else:
            bot.get_message('Não consegui pega as noticias, foi mal meu pia, tenta de novo ae...')
        # except:
            # time.sleep(1)
            # print('DEBUG LOG: Can\'t get news, retrying: %s' % user_message)
            # self.news(top_br, bot)
            
    def command(self, arg):
        self.enabled = True if arg == 'true' else False

    print('DEBUG CORE: News Bot Initialized...')