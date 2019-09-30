# -*- coding: utf-8 -*-

from core.bot_soul import CoreBot

class MainBot:
    bot = CoreBot('Domini')
    bot.start('My thoughts')
    last_message = ''
    temp_goodbye = True
    wiking = False
    listening = False

    def update(self):
        user_message = self.bot.listen(0)

        if not self.listening:
            self.bot.listen(1)

        user_message = user_message.lower()

        if user_message != self.last_message:
            temp_called_me = self.contains_word(user_message, 'domi', 'domi?')
            self.last_message = user_message
            user_message = user_message.strip()
            print(user_message)

            if self.wiking:
                self.wiking = not self.bot.get_wikipedia(1, user_message)
            elif temp_called_me:
                self.listening = True
                user_message = user_message.replace('domi', '')
                user_message = user_message.strip()
                print(user_message)

                if 'help' in user_message or 'ajuda' in user_message:
                    self.bot.get_help()
                elif 'aprender' in user_message or 'ensinar' in user_message:
                    self.bot.set_learn(user_message)
                elif 'wiki' in user_message or 'wikipedia' in user_message:
                    user_message = user_message.replace('wikipedia', '')
                    user_message = user_message.replace('wiki', '')
                    self.wiking = not self.bot.get_wikipedia(0, user_message)
                elif 'clima' in user_message or 'tempo' in user_message:
                    temp = 'region'

                    #if 'agora' in user_message:
                        #temp = 'now'
                    #elif '15 dias' in user_message:
                        #temp = '15'
                    #else:
                        #temp = 'region'

                    self.bot.get_climate(temp)
                elif 'noticias' in user_message \
                        or 'noticia' in user_message \
                        or 'notícias' in user_message \
                        or 'notícia' in user_message:
                    temp_top_br = False

                    if 'brasil' in user_message or 'br' in user_message:
                        temp_top_br = True

                    self.bot.get_news(1, temp_top_br)
                elif 'tecnologia' in user_message \
                        or 'tecnologias' in user_message \
                        or 'tech' in user_message \
                        or 'technology' in user_message:
                    self.bot.get_news(0, False)
                elif 'marcar' in user_message or 'role' in user_message:
                    self.bot.get_events(user_message)
                else:
                    self.bot.get_answer(user_message)

                self.listening = False

        self.bot.check_events_remainder()

    def contains_word(self, s, *args):

        for w in args:
            if f' {w} ' in f' {s} ':
                return True

        return False


body_bot = MainBot()

while True:
    body_bot.update()
