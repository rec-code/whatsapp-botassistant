import requests, json, time


class BotNews:
    def news_tech(self, bot):
        req = requests.get(
            'https://newsapi.org/v2/top-headlines?country=br&category=technology&pageSize=6&apiKey=f47086f0e00d43be9fe271e7e56b51db')
        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'Domi: ' + titulo + ' ' + link + '\n'

            bot.caixa_de_mensagem.send_keys(new)
            time.sleep(1)

    def news(self, top_br, bot):
        if top_br:
            req = requests.get(
                'https://newsapi.org/v2/top-headlines?country=br&pageSize=6&apiKey=f47086f0e00d43be9fe271e7e56b51db')
        else:
            if bot.random.randint(0, 2) == 0:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=google-news-br&pageSize=6&apiKey=f47086f0e00d43be9fe271e7e56b51db')
            else:
                req = requests.get(
                    'https://newsapi.org/v2/top-headlines?sources=globo&pageSize=6&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')

        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'Domi: ' + titulo + ' ' + link + '\n'

            bot.caixa_de_mensagem.send_keys(new)
            time.sleep(1)