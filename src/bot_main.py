from functions import Functions

class MainBot(Functions):
    bot = None
    #bot.start('My thoughts')
    last_message = last_user = last_number = ''
    wiking = False
    listening = False
    #waiting_cmd = False
    wiki_time_count = 0
    web_opened = main_started = False

    domika_spells = ['domika', 'domika?', 'domika,', ',domika', ',domika,', 'domika.', '.domika', '.domika.', 
                'domi', 'domi?', 'domi,', ',domi', ',domi,', 'domi.', '.domi', '.domi.', 
                # 'oni', 'oni?', 'oni,', ',oni', ',oni,', 'oni.', '.oni', '.oni.',
                # 'onik', 'onik?', 'onik,', ',onik', ',onik,', 'onik.', '.onik', '.onik.',
                # 'onika', 'onika?', 'onika,', ',onika', ',onika,', 'onika.', '.onika', '.onika.',
                # 'onikk', 'onikk?', 'onikk,', ',onikk', ',onikk,', 'onikk.', '.onikk', '.onikk.',
                # 'onikka', 'onikka?', 'onikka,', ',onikka', ',onikka,', 'onikka.', '.onikka', '.onikka.',
                ]

    climate_spells = ['tempo', 'tempo?', 'tempo!', 'tempo.',
                    'clima', 'clima?', 'clima!', 'clima.',
                    'previsão', 'previsão?', 'previsão!', 'previsão.', 
                    'temperatura', 'temperatura?', 'temperatura!', 'temperatura.',
                    'temp', 'temp?', 'temp!', 'temp.']


    greetings_spells = ['oi', 'olá', 'ois', 'tudo bem', 'tudo bom']
    morning_spells = ['bom', 'dia']
    afternoon_spells = ['boa', 'tarde']
    evening_spells = ['boa', 'noite']

    news_spells = ['noticias', 'noticia', 'notícias', 'notícia']
    tech_spells = ['tecnologia', 'tecnologias', 'tech', 'technology']
    events_spells = ['marcar', 'roles', 'rolês', 'role', 'rolê', 'eventos', 'evento', 'a boa']
    supply_spells = ['interas', 'intera']
    gg_images_spells = ['imagens', 'images', 'imgs', 'imagem', 'image', 'img', 'fotos', 'photos', 'foto', 'photo']
    gg_search_spells = ['google', 'pesquisar', 'search', 'procurar', 'achar']
    yt_videos_spells = ['youtube', 'yt', 'videos', 'video']
    yt_music_spells = ['musics', 'musicas', 'músicas', 'music', 'musica', 'música', 'sons', 'som', 'tracks', 'track', 'clipes', 'clipe']
    spotify_spells = ['spotify', 'spot', 'spt', 'sptfy']
    soundcloud_spells = ['soundcloud', 'sound', 'sd', 'sc', 'soundc']
    twitter_spells = ['twitter', 'tt', 'twit', 'twt']
    game_spells = ['jogo', 'game', 'veia', 'xadrez']
    inter_mes_spells = ['message', 'mensagem']

    def start(self):
        self.printi('Initializing Bot...', 'core')
        from core.bot_soul import CoreBot
        self.bot = CoreBot('Ônika', self)
        self.printi('Bot Initialized...', 'core')
        self.printi('Waiting for WhatsApp web to open...', 'core')
        self.main_started = True

    def update(self):
        if not self.listening and not self.wiking:
            self.bot.listen(1)

        if self.wiking:
            if self.wiki_time_count < 10:
                self.wiki_time_count += .01
            else:
                self.wiki_time_count = 0
                self.wiking = False
                self.bot.get_message('Ce mosco e o cross passo')
                return

        something = self.bot.listen(0)
        user_name = something['user']
        user_number = something['user_number']
        user_message = something['message']

        temp_user_message = user_message.lower()

        if user_message != self.bot.get_conversation()['last_message']:
            temp_called_me = self.contains_word(
                temp_user_message, 
                *self.domika_spells
            )

            self.bot.get_conversation()['last_message'] = user_message

            if user_name != '':
                self.last_user = user_name
                self.last_number = user_number

            temp_user_message = temp_user_message.strip()
            self.printi('Listening message: "%s" | from "%s (%s)"' % (user_message, self.last_user, self.last_number))

            self.check(self.last_user, self.last_number, user_message, temp_called_me, temp_user_message)

            self.listening = False

        self.bot.check_events_remainder()
        self.bot.check_bot_events()

    def check(self, user_name, user_number, user_message, temp_called_me, temp_user_message):
            if self.wiking:
                self.wiking = not self.bot.get_wikipedia(1, temp_user_message)
            #if self.contains_word()
            elif temp_called_me:
                self.listening = True
                temp_user_message = self.replace_words(temp_user_message, '', *self.domika_spells)
                user_message_completed = user_message
                user_message = self.replace_words(user_message, '', *self.domika_spells)

                temp_user_message = temp_user_message.strip()
                user_message = user_message.strip()

                temp_user_message_splited = temp_user_message.split()
                temp_user_message_hif_splited = user_message.split('--')
                temp_length_message = len(temp_user_message_splited)
                temp_length_hif_message = len(temp_user_message_hif_splited)

                if self.contains_word(temp_user_message, 'cmd', 'command'):
                    self.bot.send_cmd(temp_user_message, True, False)
                elif self.contains_word(temp_user_message, 'ajuda', 'help') and (temp_length_message == 1 or temp_length_message == 2):
                    temp_help_of_what = ''

                    if temp_length_message == 2:
                        if self.contains_word(temp_user_message_splited[0], 'ajuda', 'help'):
                            temp_help_of_what = temp_user_message_splited[1]
                        else:
                            temp_help_of_what = temp_user_message_splited[0]

                    self.bot.get_help(temp_help_of_what)
                elif self.contains_word(temp_user_message, 'aprender', 'ensinar'):
                    self.bot.set_learn(user_message_completed)
                elif self.contains_word(temp_user_message, 'wikipedia', 'wiki'):
                    temp_user_message = self.replace_words(temp_user_message, '', 'wikipedia', 'wiki')
                    self.wiking = not self.bot.get_wikipedia(0, temp_user_message)
                elif self.contains_word(temp_user_message, *self.gg_images_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.gg_images_spells)

                    self.bot.get_image(temp_user_message)
                elif self.contains_word(temp_user_message, *self.gg_search_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.gg_search_spells)

                    self.bot.get_search(temp_user_message)
                elif self.contains_word(temp_user_message, *self.yt_videos_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.yt_videos_spells)

                    self.bot.get_video_or_spotify(temp_user_message, 'youtube.com')
                elif self.contains_word(temp_user_message, *self.yt_music_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.yt_music_spells)

                    self.bot.get_video_or_spotify(temp_user_message, 'music.youtube.com')
                elif self.contains_word(temp_user_message, *self.spotify_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.spotify_spells)

                    self.bot.get_video_or_spotify(temp_user_message, 'spotify.com')
                elif self.contains_word(temp_user_message, *self.soundcloud_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.soundcloud_spells)

                    self.bot.get_video_or_spotify(temp_user_message, 'soundcloud.com')
                elif self.contains_word(temp_user_message, *self.twitter_spells):
                    temp_user_message = self.replace_words(temp_user_message, '', *self.twitter_spells)

                    self.bot.get_video_or_spotify(temp_user_message, 'twitter.com')
                elif self.contains_word(temp_user_message, *self.climate_spells):

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
                elif self.contains_word(temp_user_message, *self.news_spells):
                    temp_top_br = False

                    if 'brasil' in temp_user_message or 'br' in temp_user_message:
                        temp_top_br = True

                    self.printi('Getting News: %s' % temp_user_message)
                    self.bot.get_news(1, temp_top_br)
                elif self.contains_word(temp_user_message, *self.tech_spells):
                    self.bot.get_news(0, False)
                elif self.contains_word(temp_user_message, *self.events_spells):
                    self.bot.get_events(user_message)
                elif self.contains_word(temp_user_message, *self.supply_spells):
                    self.bot.get_supply(user_message)
                elif (self.contains_word(temp_user_message, *self.game_spells) and temp_length_hif_message == 2) or temp_length_hif_message == 2:

                    # if temp_length_hif_message != 2:
                    #     self.bot.get_message('O hífen singular *-* para parâmetros, foi substituído por dois *--*')
                    #     return

                    temp_xadrez = self.contains_word(temp_user_message, 'xadrez')

                    temp_game_id = 0 if not temp_xadrez else 1

                    self.bot.get_game(user_name, user_number, temp_user_message_hif_splited[1], temp_game_id)
                elif self.contains_word(temp_user_message, *self.inter_mes_spells) and temp_length_hif_message == 6:

                    temp_message = {
                        'from': temp_user_message_hif_splited[1].strip(),
                        'number': user_number,
                        'to_conv': str(temp_user_message_hif_splited[2].strip()),
                        'to': temp_user_message_hif_splited[3].strip(),
                        'subject': temp_user_message_hif_splited[4].strip(),
                        'message': temp_user_message_hif_splited[5].strip(),
                    }

                    self.bot.get_inter_message(temp_message)
                else:
                    self.bot.get_answer(user_message_completed, False)
            elif self.bot.learning_b() or self.contains_word(temp_user_message, 'errado', 'n', 'não', 'nao', 'er'):
                self.bot.get_answer(user_message, False)