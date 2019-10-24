# -*- coding: utf-8 -*-

from core.bot_soul import CoreBot

class MainBot:
    print('DEBUG CORE: Initializing Bot...')

    bot = CoreBot('Ônika')
    #bot.start('My thoughts')
    last_message = ''
    wiking = False
    listening = False
    #waiting_cmd = False
    print('DEBUG CORE: Bot Initialized...')

    def update(self):
        if not self.listening:
            self.bot.listen(1)

        user_message = self.bot.listen(0)

        temp_user_message = user_message.lower()

        if user_message != self.last_message:
            temp_called_me = self.contains_word(
                temp_user_message, 
                'domi', 'domi?', 'domi,', ',domi', ',domi,', 'domi.', '.domi', '.domi.', 
                'oni', 'oni?', 'oni,', ',oni', ',oni,', 'oni.', '.oni', '.oni.',
                'onik', 'onik?', 'onik,', ',onik', ',onik,', 'onik.', '.onik', '.onik.',
                'onika', 'onika?', 'onika,', ',onika', ',onika,', 'onika.', '.onika', '.onika.',
                'onikk', 'onikk?', 'onikk,', ',onikk', ',onikk,', 'onikk.', '.onikk', '.onikk.',
                'onikka', 'onikka?', 'onikka,', ',onikka', ',onikka,', 'onikka.', '.onikka', '.onikka.'
            )
            temp_called_watson = self.contains_word(
                temp_user_message, 
                'domitson', 'domitson?', 'domitson,', ',domitson', ',domitson,', 'domitson.', '.domitson', '.domitson.', 
                'onitson', 'onitson?', 'onitson,', ',onitson', ',onitson,', 'onitson.', '.onitson', '.onitson.',
                'oniktson', 'oniktson?', 'oniktson,', ',oniktson', ',oniktson,', 'oniktson.', '.oniktson', '.oniktson.',
                'onikatson', 'onikatson?', 'onikatson,', ',onikatson', ',onikatson,', 'onikatson.', '.onikatson', '.onikatson.',
                'onikktson', 'onikktson?', 'onikktson,', ',onikktson', ',onikktson,', 'onikktson.', '.onikktson', '.onikktson.',
                'onikkatson', 'onikkatson?', 'onikkatson,', ',onikkatson', ',onikkatson,', 'onikkatson.', '.onikkatson', '.onikkatson.'
            )
            self.last_message = user_message
            temp_user_message = temp_user_message.strip()
            print('DEBUG LOG: Listening message: %s' % user_message)

            if self.wiking:
                self.wiking = not self.bot.get_wikipedia(1, temp_user_message)
            elif temp_called_me:
                self.listening = True
                temp_user_message = self.replace_words(temp_user_message, '', 
                    'domi?', 'domi,', ',domi', ',domi,', 'domi.', '.domi', '.domi.', 'domi',
                    'oni?', 'oni,', ',oni', ',oni,', 'oni.', '.oni', '.oni.', 'oni',
                    'onik?', 'onik,', ',onik', ',onik,', 'onik.', '.onik', '.onik.', 'onik',
                    'onika?', 'onika,', ',onika', ',onika,', 'onika.', '.onika', '.onika.', 'onika',
                    'onikk?', 'onikk,', ',onikk', ',onikk,', 'onikk.', '.onikk', '.onikk.', 'onikk',
                    'onikka?', 'onikka,', ',onikka', ',onikka,', 'onikka.', '.onikka', '.onikka.','onikka'
                )
                temp_user_message = temp_user_message.strip()

                if self.contains_word(temp_user_message, 'cmd', 'command'):
                    #self.waiting_cmd = True
                    self.bot.send_cmd(temp_user_message)
                elif 'help' in temp_user_message or 'ajuda' in temp_user_message:
                    self.bot.get_help()
                elif 'aprender' in temp_user_message or 'ensinar' in temp_user_message:
                    self.bot.set_learn(temp_user_message)
                elif 'wiki' in temp_user_message or 'wikipedia' in temp_user_message:
                    temp_user_message = temp_user_message.replace('wikipedia', '')
                    temp_user_message = temp_user_message.replace('wiki', '')
                    self.wiking = not self.bot.get_wikipedia(0, temp_user_message)
                elif self.contains_word(temp_user_message, 'tempo', 'clima', 'previsão', 'temperatura', 'temp'):
                    temp = 'region'

                    if 'region' in temp_user_message:
                        temp = 'region'
                    elif '15 dias' in temp_user_message:
                        temp = '15'
                    else:
                        temp = 'now'

                    self.bot.get_climate(temp)
                elif 'noticias' in temp_user_message \
                        or 'noticia' in temp_user_message \
                        or 'notícias' in temp_user_message \
                        or 'notícia' in temp_user_message:
                    temp_top_br = False

                    if 'brasil' in temp_user_message or 'br' in temp_user_message:
                        temp_top_br = True

                    print('DEBUG LOG: Getting News: %s' % temp_user_message)
                    self.bot.get_news(1, temp_top_br)
                elif self.contains_word(temp_user_message, 'tecnologia', 'tecnologias', 'tech', 'technology'):
                    self.bot.get_news(0, False)
                elif self.contains_word(temp_user_message, 'marcar', 'roles', 'rolês', 'role', 'rolê', 'eventos', 'evento', 'a boa'):
                    self.bot.get_events(temp_user_message)
                elif self.contains_word(temp_user_message, 'images', 'imagens', 'img', 'imgs', 'foto', 'fotos', 'photo', 'photos'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'imagens', 'images', 'imgs', 'img', 'fotos', 'foto','photos', 'photo')

                    self.bot.get_image(temp_user_message)
                elif self.contains_word(temp_user_message, 'google', 'pesquisar', 'search', 'procurar', 'achar'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'google', 'pesquisar', 'search', 'procurar', 'achar')

                    self.bot.get_search(temp_user_message)
                else:
                    self.bot.get_answer(temp_user_message, False)
            elif temp_called_watson:
                self.listening = True
                user_message = self.replace_words(user_message, '', 
                    'domitson?', 'domitson,', ',domitson', ',domitson,', 'domitson.', '.domitson', '.domitson.', 'domitson',
                    'onitson?', 'onitson,', ',onitson', ',onitson,', 'onitson.', '.onitson', '.onitson.', 'onitson',
                    'oniktson?', 'oniktson,', ',oniktson', ',oniktson,', 'oniktson.', '.oniktson', '.oniktson.', 'oniktson',
                    'onikatson?', 'onikatson,', ',onikatson', ',onikatson,', 'onikatson.', '.onikatson', '.onikatson.', 'onikatson',
                    'onikktson?', 'onikktson,', ',onikktson', ',onikktson,', 'onikktson.', '.onikktson', '.onikktson.', 'onikktson',
                    'onikkatson?', 'onikkatson,', ',onikkatson', ',onikkatson,', 'onikkatson.', '.onikkatson', '.onikkatson.', 'onikkatson'
                )
                user_message = user_message.strip()

                self.bot.get_answer(user_message, True)
            elif self.bot.learning_b() or self.contains_word(temp_user_message, 'errado', 'n', 'não', 'nao', 'er'):
                self.bot.get_answer(user_message, False)

            self.listening = False
            print('DEBUG LOG:', 'Stopped listening')

        self.bot.check_events_remainder()

    def contains_word(self, s, *args):
        for w in args:
            if f' {w} ' in f' {s} ':
                return True

        return False

    def replace_words(self, message, s, *args):
        for w in args:
            message = message.replace(w, s)

        message = message.strip()
        return message

body_bot = MainBot()

while True:
    body_bot.update()
