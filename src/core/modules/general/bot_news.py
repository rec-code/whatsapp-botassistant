import requests, json, time, random

from core.bot_modules_core import BotModulesCore 


class BotNews(BotModulesCore):
    def __init__(self, name):
        super(BotNews, self).__init__(name)

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
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            bot.get_message('Notícias de Tecnologias desabilitadas temporariamente')
            return

        req = requests.get(
            'https://newsapi.org/v2/top-headlines?country=br&category=technology&pageSize=6&apiKey=yourkey')
        noticias = json.loads(req.text)

        if noticias['articles']:
            # try:
            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', as noticias de tecnologias ae:\n' )
           
            for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                titulo = '*%s.*' % titulo

                bot.get_message_with_two_spaces(titulo)
                bot.get_message_with_two_spaces(link)
                bot.send_message()
            # except:
            #     time.sleep(1)
            #     print('DEBUG LOG: Can\'t get tech news, retrying: %s' % user_message)
            #     self.news_tech(bot)
        else:
            bot.get_message('Não consegui pega as noticias de tech truta, foi mal, tenta de novo ae...')

    def news(self, top_br, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            bot.get_message('Notícias desabilitadas temporariamente')
            return

        if top_br:
            req = requests.get(
                'https://newsapi.org/v2/top-headlines?country=br&pageSize=6&apiKey=yourkey')
        else:
            if random.randint(0, 2) == 0:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=google-news-br&pageSize=6&apiKey=yourkey')
            else:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=globo&pageSize=6&apiKey=yourkey')

        noticias = json.loads(req.text)

        if noticias['articles']:
            bot.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', as noticias ae:\n')

            for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                titulo = '*%s.*' % titulo

                bot.get_message_with_two_spaces(titulo)
                bot.get_message_with_two_spaces(link)
                bot.send_message()
        else:
            bot.get_message('Não consegui pega as noticias, foi mal meu pia, tenta de novo ae...')