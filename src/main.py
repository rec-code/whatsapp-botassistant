# -*- coding: utf-8 -*-
import re
from sys import stdout
from datetime import datetime

class MainBot:
    bot = None
    #bot.start('My thoughts')
    last_message = ''
    wiking = False
    listening = False
    #waiting_cmd = False
    wiki_time_count = 0
    web_opened = False

    def start(self):
        self.printi('Initializing Bot...', 'core')
        from core.bot_soul import CoreBot
        self.bot = CoreBot('Ônika', self)
        self.printi('Bot Initialized...', 'core')
        self.printi('Waiting for WhatsApp web to open...', 'core')

    def update(self):
        if not self.listening and not self.wiking:
            self.bot.listen(1)

        if self.wiking:
            if self.wiki_time_count < 10:
                self.wiki_time_count += .5
            else:
                self.wiki_time_count = 0
                self.wiking = False
                self.bot.get_message('Ce mosco e o cross passo')
                return

        user_message = self.bot.listen(0)

        temp_user_message = user_message.lower()

        if user_message != self.last_message:
            temp_called_me = self.contains_word(
                temp_user_message, 
                'domika', 'domika?', 'domika,', ',domika', ',domika,', 'domika.', '.domika', '.domika.', 
                'domi', 'domi?', 'domi,', ',domi', ',domi,', 'domi.', '.domi', '.domi.', 
                # 'oni', 'oni?', 'oni,', ',oni', ',oni,', 'oni.', '.oni', '.oni.',
                # 'onik', 'onik?', 'onik,', ',onik', ',onik,', 'onik.', '.onik', '.onik.',
                # 'onika', 'onika?', 'onika,', ',onika', ',onika,', 'onika.', '.onika', '.onika.',
                # 'onikk', 'onikk?', 'onikk,', ',onikk', ',onikk,', 'onikk.', '.onikk', '.onikk.',
                # 'onikka', 'onikka?', 'onikka,', ',onikka', ',onikka,', 'onikka.', '.onikka', '.onikka.',
            )
            # temp_called_watson = self.contains_word(
            #     temp_user_message, 
            #     'domitson', 'domitson?', 'domitson,', ',domitson', ',domitson,', 'domitson.', '.domitson', '.domitson.', 
            #     'onitson', 'onitson?', 'onitson,', ',onitson', ',onitson,', 'onitson.', '.onitson', '.onitson.',
            #     'oniktson', 'oniktson?', 'oniktson,', ',oniktson', ',oniktson,', 'oniktson.', '.oniktson', '.oniktson.',
            #     'onikatson', 'onikatson?', 'onikatson,', ',onikatson', ',onikatson,', 'onikatson.', '.onikatson', '.onikatson.',
            #     'onikktson', 'onikktson?', 'onikktson,', ',onikktson', ',onikktson,', 'onikktson.', '.onikktson', '.onikktson.',
            #     'onikkatson', 'onikkatson?', 'onikkatson,', ',onikkatson', ',onikkatson,', 'onikkatson.', '.onikkatson', '.onikkatson.'
            # )
            self.last_message = user_message
            temp_user_message = temp_user_message.strip()
            self.printi('Listening message: %s' % (user_message + '\r'), 'inline')

            if self.wiking:
                self.wiking = not self.bot.get_wikipedia(1, temp_user_message)
            elif temp_called_me:
                self.listening = True
                temp_user_message = self.replace_words(temp_user_message, '', 
                    'domika', 'domika?', 'domika,', ',domika', ',domika,', 'domika.', '.domika', '.domika.', 
                    'domi?', 'domi,', ',domi', ',domi,', 'domi.', '.domi', '.domi.', 'domi',
                    # 'oni?', 'oni,', ',oni', ',oni,', 'oni.', '.oni', '.oni.', 'oni',
                    # 'onik?', 'onik,', ',onik', ',onik,', 'onik.', '.onik', '.onik.', 'onik',
                    # 'onika?', 'onika,', ',onika', ',onika,', 'onika.', '.onika', '.onika.', 'onika',
                    # 'onikk?', 'onikk,', ',onikk', ',onikk,', 'onikk.', '.onikk', '.onikk.', 'onikk',
                    # 'onikka?', 'onikka,', ',onikka', ',onikka,', 'onikka.', '.onikka', '.onikka.','onikka',
                )

                user_message = self.replace_words(user_message, '', 
                    'domika', 'domika?', 'domika,', ',domika', ',domika,', 'domika.', '.domika', '.domika.', 
                    'domi?', 'domi,', ',domi', ',domi,', 'domi.', '.domi', '.domi.', 'domi',
                    # 'oni?', 'oni,', ',oni', ',oni,', 'oni.', '.oni', '.oni.', 'oni',
                    # 'onik?', 'onik,', ',onik', ',onik,', 'onik.', '.onik', '.onik.', 'onik',
                    # 'onika?', 'onika,', ',onika', ',onika,', 'onika.', '.onika', '.onika.', 'onika',
                    # 'onikk?', 'onikk,', ',onikk', ',onikk,', 'onikk.', '.onikk', '.onikk.', 'onikk',
                    # 'onikka?', 'onikka,', ',onikka', ',onikka,', 'onikka.', '.onikka', '.onikka.','onikka',
                )
                temp_user_message = temp_user_message.strip()
                user_message = user_message.strip()

                if self.contains_word(temp_user_message, 'cmd', 'command'):
                    #self.waiting_cmd = True
                    self.bot.send_cmd(temp_user_message, True, False)
                elif self.contains_word(temp_user_message, 'ajuda', 'help') and (len(temp_user_message.split()) == 1 or len(temp_user_message.split()) == 2):
                    self.bot.get_help(temp_user_message.split()[0] if len(temp_user_message.split()) == 2 else '')
                elif 'aprender' in temp_user_message or 'ensinar' in temp_user_message:
                    self.bot.set_learn(user_message)
                elif 'wiki' in temp_user_message or 'wikipedia' in temp_user_message:
                    temp_user_message = temp_user_message.replace('wikipedia', '')
                    temp_user_message = temp_user_message.replace('wiki', '')
                    self.wiking = not self.bot.get_wikipedia(0, temp_user_message)
                elif self.contains_word(
                    temp_user_message, 
                    'tempo', 'tempo?', 'tempo!', 'tempo.',
                    'clima', 'clima?', 'clima!', 'clima.',
                    'previsão', 'previsão?', 'previsão!', 'previsão.', 
                    'temperatura', 'temperatura?', 'temperatura!', 'temperatura.',
                    'temp', 'temp?', 'temp!', 'temp.'
                    ):

                    temp = 'region'
                    temp_region = ''

                    if 'região' in temp_user_message:
                        temp = 'region'

                        for reg in temp_user_message.split():
                            reg = reg.strip()

                            if self.contains_word(reg, 'sul', 'sudeste', 'norte', 'nordeste', 'centro-oeste'):
                                temp_region = reg

                    elif '15 dias' in temp_user_message:
                        temp = '15'
                    else:
                        temp = 'now'


                    self.bot.get_climate(temp, temp_region)
                elif 'noticias' in temp_user_message \
                        or 'noticia' in temp_user_message \
                        or 'notícias' in temp_user_message \
                        or 'notícia' in temp_user_message:
                    temp_top_br = False

                    if 'brasil' in temp_user_message or 'br' in temp_user_message:
                        temp_top_br = True

                    self.printi('Getting News: %s' % temp_user_message)
                    self.bot.get_news(1, temp_top_br)
                elif self.contains_word(temp_user_message, 'tecnologia', 'tecnologias', 'tech', 'technology'):
                    self.bot.get_news(0, False)
                elif self.contains_word(temp_user_message, 'marcar', 'roles', 'rolês', 'role', 'rolê', 'eventos', 'evento', 'a boa'):
                    self.bot.get_events(user_message)
                elif self.contains_word(temp_user_message, 'intera'):
                    self.bot.get_supply(user_message)
                elif self.contains_word(temp_user_message, 'imagens', 'images', 'imgs', 'imagem', 'image', 'img', 'fotos', 'photos', 'foto', 'photo'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'imagens', 'images', 'imgs', 'imagem', 'image', 'img', 'fotos', 'photos', 'foto', 'photo')

                    self.bot.get_image(temp_user_message)
                elif self.contains_word(temp_user_message, 'google', 'pesquisar', 'search', 'procurar', 'achar'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'google', 'pesquisar', 'search', 'procurar', 'achar')

                    self.bot.get_search(temp_user_message)
                elif self.contains_word(temp_user_message, 'youtube', 'yt', 'videos', 'video'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'youtube', 'yt', 'videos', 'video')

                    self.bot.get_video_or_spotify(temp_user_message, 'youtube.com')
                elif self.contains_word(temp_user_message, 'music', 'musics', 'musicas', 'musica', 'sons', 'som'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'music', 'musics', 'musicas', 'musica', 'sons', 'som')

                    self.bot.get_video_or_spotify(temp_user_message, 'music.youtube.com')
                elif self.contains_word(temp_user_message, 'spotify', 'spot', 'spt', 'sptfy'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'spotify', 'spot', 'spt', 'sptfy')

                    self.bot.get_video_or_spotify(temp_user_message, 'spotify.com')
                elif self.contains_word(temp_user_message, 'soundcloud', 'sound', 'sd', 'sc', 'soundc'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'soundcloud', 'sound', 'sd', 'sc', 'soundc')

                    self.bot.get_video_or_spotify(temp_user_message, 'soundcloud.com')
                elif self.contains_word(temp_user_message, 'twitter', 'tt', 'twit', 'twt'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'twitter', 'tt', 'twit', 'twt')

                    self.bot.get_video_or_spotify(temp_user_message, 'twitter.com')
                else:
                    self.bot.get_answer(user_message, False)
            # elif temp_called_watson:
            #     self.listening = True
            #     user_message = self.replace_words(user_message, '', 
            #         'domitson?', 'domitson,', ',domitson', ',domitson,', 'domitson.', '.domitson', '.domitson.', 'domitson',
            #         'onitson?', 'onitson,', ',onitson', ',onitson,', 'onitson.', '.onitson', '.onitson.', 'onitson',
            #         'oniktson?', 'oniktson,', ',oniktson', ',oniktson,', 'oniktson.', '.oniktson', '.oniktson.', 'oniktson',
            #         'onikatson?', 'onikatson,', ',onikatson', ',onikatson,', 'onikatson.', '.onikatson', '.onikatson.', 'onikatson',
            #         'onikktson?', 'onikktson,', ',onikktson', ',onikktson,', 'onikktson.', '.onikktson', '.onikktson.', 'onikktson',
            #         'onikkatson?', 'onikkatson,', ',onikkatson', ',onikkatson,', 'onikkatson.', '.onikkatson', '.onikkatson.', 'onikkatson'
            #     )
            #     user_message = user_message.strip()

            #     # if self.contains_word(temp_user_message, 'imagens', 'images', 'imgs', 'imagem', 'image', 'img', 'fotos', 'photos', 'foto', 'photo'):
            #     #     self.bot.get_answer_for_image(user_message)
            #     #else:
            #     self.bot.get_answer(user_message, True)
            elif self.bot.learning_b() or self.contains_word(temp_user_message, 'errado', 'n', 'não', 'nao', 'er'):
                self.bot.get_answer(user_message, False)

            self.listening = False
            #print('DEBUG LOG:', 'Stopped listening')

        self.bot.check_events_remainder()
        self.bot.check_bot_events()

    def contains_word(self, s, *args):
        for w in args:
            if f' {w} ' in f' {s} ':
                return True

        return False

    def replace_words(self, message, s, *args):
        for w in args:
            #message = message.replace(w, s)
            # pattern = re.compile(w, re.IGNORECASE)
            #print(pattern)

            #message = pattern.sub(s, message)
            message = re.sub(r"\b%s\b" % w, s, message, flags=re.I) #'bye bye bye'
            # print(message)
            #message = re.sub(r"\b%s\b".lower() % w.lower() , s, message)

        message = message.strip()
        
        return message

    def get_time(self):
        return datetime.now().strftime('%X')
    
    def printi(self, log, *args):
        level_debug = 'LOG'
        inline = False
        temp_label = '%s - DEBUG %s: %s'

        for i in args:
            if i == 'inline':
                inline = True
            elif i == 'core':
                level_debug = 'CORE'

        debug = temp_label % (self.get_time(), level_debug, log)
        
        start_time = str(datetime.now().strftime('%x')).replace('/', '-')
        log = self.replace_words(log, '', '\n', '\r')

        try:
            with open('debug\\debug-%s.txt' % start_time,'a') as file:
                file.write(str(debug+'\n'))
        except UnicodeEncodeError:
            self.printi('Not a string, mother...', 'core')
            
        #debug_file.close()

        # if inline:
        #     stdout.write(debug + str(' ' * (50 - len(log))) + '\r')
        #     stdout.flush()
        # else:
        print(debug)

body_bot = MainBot()
body_bot.start()

while not body_bot.web_opened:
    body_bot.bot.listen(1)

while True:
    body_bot.update()
    body_bot.bot.update()
