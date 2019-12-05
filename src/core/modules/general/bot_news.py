import requests, json, time, random
import xml.etree.cElementTree as ET

from core.bot_modules_core import BotModulesCore 


class BotNews(BotModulesCore):
    def __init__(self, name, bot):
        super(BotNews, self).__init__(name, bot)
        self.get_database_credentials_path = self.bot.root_path + "databases/credentials.xml"

        self.cache_responses = [
            'Fala mestre',
            'Po, uma bagona monstra, né não mestre, mas xofala',
            'Então gurizão',
            'Fala meus pentelhos',
            'Meus obliterados',
            'Então meu cheetos bola',
            'Fala amor da minha vida',
        ]

        tree = ET.parse(self.get_database_credentials_path)
        root = tree.getroot()
        
        for cred in root:
            if cred.attrib['name'] == 'news':
                self.api_key_news = cred[0].text
                self.apiv2_key_news = cred[1].text
                self.printi('News credentials loaded', 'core')

    def news_tech(self, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            bot.get_message('Notícias de Tecnologias desabilitadas temporariamente')
            return

        req = requests.get(
            'https://newsapi.org/v2/top-headlines?country=br&category=technology&pageSize=6&apiKey=%s' % self.api_key_news)
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
                'https://newsapi.org/v2/top-headlines?country=br&pageSize=6&apiKey=%s' % self.api_key_news)
        else:
            if random.randint(0, 2) == 0:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=google-news-br&pageSize=6&apiKey=%s' % self.api_key_news)
            else:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=globo&pageSize=6&apiKey=%s' % self.apiv2_key_news)

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