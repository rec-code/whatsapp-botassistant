# import wolframalpha, time
from datetime import datetime
import random, time
import xml.etree.cElementTree as ET

class BotMouth:
    print('DEBUG CORE: Initializing Mouth Bot...')
    enabled = True
    get_database_diary_path = "databases/diary.xml"

    def start(self, bot):    
        tree = ET.parse(self.get_database_diary_path)
        root = tree.getroot()

        for conv in root:
            temp_conv_name = conv.attrib['conv_name']
            # roles.append({'conv_name': temp_conv_name})
            bot.send_cmd('cmd diary %s %s' % (temp_conv_name, bot.password), False, True)
            print('DEBUG LOG:', 'Conversation [name: %s] - loaded from diary database' % temp_conv_name)

    def save_database(self, name):
        try:
            tree = ET.parse(self.get_database_diary_path)
            root = tree.getroot()
        except:
            root = ET.Element('conversations')

        conv_name = ET.SubElement(root, 'conv', conv_name=name)

        tree = ET.ElementTree(root)
        tree.write(self.get_database_diary_path, encoding="UTF-8", xml_declaration=True)
        print('DEBUG LOG:', 'Conversation [name: %s] - saved to diary database' % name)


    def answer(self, message, bot):
        if not self.enabled:
            return

        # try:
        #     client = wolframalpha.Client(bot.app_id)
        #     res = client.query(message)
        #     response = next(res.results).text
        # except:
        response = bot.bot.get_response(message)

        bot.get_message(str(response))
        #time.sleep(.5)

    my_events = [
        {
            'hour' : datetime(2019, 1, 1, 4, 20),
            'search' : 'maconha',
            'random' : False,
            'sended' : False,
            'messages': [
                'Quaaaaaaaaaaaaaaaaatro e vinte da madrugada, hora de dar uma bongadaaa',
                '4:20 na madruga poha, caralho\nJá estão fumando aquele de lei?',
                'Fala meus confrades, 4:20 na madrugadinha hein ;=; poha, já to doidão e vocês?',
                '4:20\nHora boa',
                '4:20'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 6, 0),
            'search' : 'amanhecer',
            'random' : True,
            'sended' : False,
            'messages': [
                'Oi lindos, mais um dia amanhecendo hein...',
                'Uma boa pa nois famia, uma manhã nova no horizonte\nUm dia top pa nois smc',
                'Fala meus confrades, mais um amanhecer top começando, uma boa pa noisssxx',
                'Uma boa pa nois famia, um bom amanhecer pa noizxx\nPeguem os incesos, a cadeira, o madeira e va comtempla mais um dia começando',
                'Mais um dia nascendo no horizonte'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 7, 0),
            'search' : 'bom dia',
            'random' : True,
            'sended' : False,
            'messages': [
                'Bom dia meus amigos, a tia ama vocês',
                'Uma boa pa nois famia linda da tia\nUm dia top pa nois smc',
                'Fala meus netinhos, mais um dia top começando, uma boa pa noisssxx lindos',
                'Uma boa pa nois famia linda, um bom dia da tia Oni',
                'Bom dia, a vó Onik ama vocês'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 8, 0),
            'search' : 'motivação trabalho',
            'random' : True,
            'sended' : False,
            'messages': [
                'Bom dia meus amigos, a tia ama vocês, um bom trabalho a todos',
                'Uma boa pa nois famia linda da tia, come a marmita e bom trampo\nUm dia top pa nois smc',
                'Fala meus netinhos, bom trabalho e não esquece do boné de tricó, uma boa pa noisssxx lindos',
                'Uma boa pa nois famia linda, um bom trabalho. Beijo da tia Oni',
                'Bom dia, bom trabalho, a vó Onik ama vocês'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 9, 0),
            'search' : 'bolsonaro',
            'random' : True,
            'sended' : False,
            'messages': [
            ]
        },
        # {
        #     'hour' : datetime(2019, 1, 1, 10, 0),
        #     'search' : 'café',
        #     'random' : True,
        #     'sended' : False,
        #     'messages': [
        #         'Hora do café',
        #         'Uma boa pa nois famia\nTomem água',
        #         'Fala meus confrades, uma boa pa noisssxx',
        #         'Uma boa pa nois famia, um bom uso das drogas',
        #         'Um tiroliro pa nois famia'
        #     ]
        # },
        # {
        #     'hour' : datetime(2019, 1, 1, 11, 0),
        #     'search' : 'tira gosto',
        #     'random' : True,
        #     'sended' : False,
        #     'messages': [
        #         'Já já tem almoço, caraaaai',
        #         'Uma saladinha no almoço, não se esqueçam gente'
        #     ]
        # },
        {
            'hour' : datetime(2019, 1, 1, 12, 20),
            'search' : 'almoço',
            'random' : True,
            'sended' : False,
            'messages': [
                'Hora do almoço',
                'Uma boa pa nois no almoço, famia\nTomem água e escovem os dentes depois do almoço, é o bicho',
                'Uma boa no almoço',
                'Bom almoço',
                'Um ótimo almoço a todos'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 13, 0),
            'search' : 'descanso',
            'random' : True,
            'sended' : False,
            'messages': [
                'Pós almoço, buchin chei',
                'Uma boa pa nois famia',
                'Fala meus confrades, uma boa pa noisssxx depois desse armocin',
                'Uma boa pa nois famia, um bom uso das drogas pós almoço',
                'Um tiroliro pa nois famia after almoço'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 15, 15),
            'search' : 'bolsonaro',
            'random' : True,
            'sended' : False,
            'messages': [
            ]
        },
        # {
        #     'hour' : datetime(2019, 1, 1, 15, 50),
        #     'search' : 'café da tarde',
        #     'random' : True,
        #     'sended' : False,
        #     'messages': [
        #         'Quem vai toma o cafézin da tarde já já heeein?? :p',
        #         'Um cafezin da tarde, yumi yumi',
        #         'Que fominhaaaaa',
        #         'Alguém me trás um chocolate ai smc, queria come algo no café da tarde'
        #     ]
        # },
        {
            'hour' : datetime(2019, 1, 1, 16, 20),
            'search' : 'maconha',
            'random' : False,
            'sended' : False,
            'messages': [
                'Quatro:20te',
                '4:20',
                '16:20',
                '4:20\nHora boa',
                '4:vinte'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 17, 45),
            'search' : 'motivação descanso',
            'random' : False,
            'sended' : False,
            'messages': [
                # 'Boa galera, mais um dia se passando, espero que tenham tido um bom dia e que o trampo foi massa\n\
                # Para os que vão começar a trampa agora, uma boa pu ceis mulekagem',
                # 'Um bom descanso',
                # '5:30 p.m already???? Quem vai bate um happy hour jaja?? CHAMA EU HEEEEIN',
                # 'Ooopa, ainda bem que já já vou embora para poder tomar um banho online',
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 18, 30),
            'search' : 'amor frases',
            'random' : False,
            'sended' : False,
            'messages': [
                '<3',
                's2',
                'ç2',
                '<3<3',
                '<3<3<3',
                '<3<3<3<3'
            ]
        },
        {
            'hour' : datetime(2019, 1, 1, 19, 0),
            'search' : 'boa noite',
            'random' : True,
            'sended' : False,
            'messages' : [
                'Boa noite rapaziada',
                'Uma boa pa nois famia\nNoitinha top pa nois smc',
                'Fala meus confrades, mais um dia se passando ai',
                'Uma boa pa nois famia, uma boa noite',
                'Boa noite'
            ]
        },
        # {
        #     'hour' : datetime(2019, 1, 1, 20, 15),
        #     'search' : '',
        #     'random' : True,
        #     'sended' : False,
        #     'messages' : [
        #         'Boa noite rapaziada',
        #         'Uma boa pa nois famia\nNoitinha top pa nois smc',
        #         'Fala meus confrades, mais um dia se passando ai',
        #         'Uma boa pa nois famia, uma boa noite',
        #         'Boa noite'
        #     ]
        # },
        {
            'hour' : datetime(2019, 1, 1, 22, 0),
            'search' : 'bons sonhos',
            'random' : True,
            'sended' : False,
            'messages' : [
                'Bons sonhos gente, vou dormir\nzzzzzoas <3',
                'Um bom descanso pa noixx <3',
                'Que a noite seja regada a bons sonhos <3',
                'Boa noite meus amigos <3',
                'Se cuidem amores, até mais <3',
            ]
        },
    ]

    conversations = []
    reseted = False
    date_bolsonaro_over = datetime(2022, 12, 31, 0, 0)
    bolso_messages = [
        '%s dias',
    ]
    
    friday_messages = [
        'Opa, sextinha trutinhas, hoje vai se binga',
        'Uma boa pa nóis na sexta rapaziada',
        'Sexta gente, não usem drogas, não contratem prostitutas... Mandem tudo para mim',
        'Sexta fire, day to gonna be craaazy 3:)',
        'Sexta chera rapeize, só não pode chera o reboco de casa, de resto ta sussa... Una good for us'
    ]

    thursday_messages = [
        'Quinta feira já rapeize, o bagui ficando loco, mas amanhã já é sexta poha',
        'Uma boa pa nóis na quinta rapaziada',
        'Quinta feira gente, não usem drogas hoje, só amanhã',
        'Quinta fire, day to gonna be craaazy 3:)',
        'Quintinha po, já já tem relento, só aguenta gente'
    ]

    def get_bolsonaro_time_left(self):
        temp_now = datetime.now()
        time_remaing = self.date_bolsonaro_over - temp_now

        return self.bolso_messages[random.randint(0, len(self.bolso_messages) - 1 )] % time_remaing.days

    def events(self, bot):
        temp_now = datetime.now()

        if len(self.conversations) != 0:
            for eve in self.my_events:
                time_remaing = temp_now - eve['hour']

                if time_remaing.seconds <= 5 and not eve['sended']:
                    for conv in self.conversations:
                        bot.set_conversation(conv)
                        temp_message = ''

                        if len(eve['messages']) != 0:
                            temp_message = eve['messages'][random.randint(0, len(eve['messages'])-1 )]

                        temp_search = eve['search']

                        if temp_search == 'bolsonaro':
                            temp_message += '\n%s' % self.get_bolsonaro_time_left()

                        if temp_search == 'motivação trabalho' or temp_search == 'motivação descanso':
                            if temp_now.weekday() == 4:
                                temp_search = 'sexta feira'
                                temp_message += '\n' + self.friday_messages[random.randint(0, len(self.friday_messages)-1 )]
                            elif temp_now.weekday() == 3:
                                temp_search = 'quinta feira'
                                temp_message += '\n' + self.thursday_messages[random.randint(0, len(self.thursday_messages)-1 )]

                        time.sleep(.5)

                        if temp_message != '':
                            bot.get_message(temp_message)
                            time.sleep(.5)

                        if temp_search != 'bolsonaro':
                            bot.get_image(temp_search)

                    eve['sended'] = True

                    if self.reseted:
                        self.reseted = False
    
        time_remaing_reset = temp_now - datetime(2019, 1, 1, 0, 0)

        if time_remaing_reset.seconds <= 5 and not self.reseted:
            for eve in self.my_events:
                eve['sended'] = False

            self.reseted = True


    def command(self, arg):
        self.enabled = True if arg == 'true' else False
        
    print('DEBUG CORE: Mouth Bot Initialized...')
