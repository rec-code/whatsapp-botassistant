# -*- coding: utf-8 -*-

import os, time, random

from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver

# logging.basicConfig(level=logging.INFO)

# Bot Modules
from core.modules.entity.bot_brain import BotBrain
from core.modules.entity.bot_ears import BotEars
from core.modules.entity.bot_mouth import BotMouth

from core.modules.general.bot_climate import BotClimate
from core.modules.general.bot_events import BotEvent
from core.modules.general.bot_help import BotHelp
from core.modules.general.bot_news import BotNews
from core.modules.general.bot_wikipedia import BotWikipedia

from core.modules.google.bot_google import BotGoogle

from core.modules.watson.bot_watson import BotWatson

# Modules Started
brain = BotBrain()
ears = BotEars()
mouth = BotMouth()

climate = BotClimate()
events = BotEvent()
aid = BotHelp()
news = BotNews()
wiki = BotWikipedia()

google = BotGoogle()

watson = BotWatson()

# Bot Configuration
app_id = "U32UR2-EXW6X24J7A"

conversations_to_listen = {}

modules = [
    brain,
    ears,
    mouth,
    climate,
    events,
    aid,
    news,
    wiki,
    google,
    watson    
]

class CoreBot:
    print('DEBUG CORE: Initializing Soul Bot..')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    current_conversation = ''
    last_version = '1.0.0.0'
    bot_version = '1.0.1.0'

# Initalization Region
    def __init__(self, bot_name):
        self.bot = ChatBot(
            bot_name,
            logic_adapters=[
                "chatterbot.logic.BestMatch",
                #'chatterbot.logic.MathematicalEvaluation',
            ],
            )

        # self.bot.set_trainer(ChatterBotCorpusTrainer)
        # self.bot.train(
        #     "chatterbot.corpus.portuguese",
        #     #"chatterbot.corpus.english",
        # )

        self.bot.set_trainer(ListTrainer)
        #self.set_train('train_models')

        print("DEBUG CORE: Path:", self.dir_path)
        self.chrome = self.dir_path+'\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)
        time.sleep(1)

# Events Region
    def get_events(self, message):
        events.events(message, self)

    def check_events_remainder(self):
        events.check_events(self)

# News Region
    def get_news(self, action_id, top_br):
        if action_id == 0:
            news.news_tech(self)
        else:
            news.news(top_br, self)

# Climate Region
    def get_climate(self, mode):
        climate.climate(mode, self)

# Wikipedia Region
    def get_wikipedia(self, action_id, message):
        if action_id == 0:
            return wiki.wiki(message, self)
        else:
            return wiki.select_wikipedia(message, self)

# Help Region
    def get_help(self):
        self.get_message(aid.help_list)

# Images Region
    def get_image(self, message):
        google.search_image(message, False, '', self)

# Internet Search Region
    def get_search(self, message):
        google.search(message, self)

# Bot Listen Region
    def listen(self, action_id):
        if action_id == 0:
            return ears.listen_contact(self)
        else:
            ears.listen_all_contacts(self)

# Bot Learning Region
    def set_learn(self, message):
        brain.learn(message, self)

    def set_train(self, folder_name):
        temp_path_folder = self.dir_path + '/' + folder_name

        for train_models in os.listdir(temp_path_folder):
            conversations = open(temp_path_folder+'/'+train_models, encoding='utf-8').readlines()
            self.bot.train(conversations)

# Bot Responses Region
    last_message = ''
    learning = False

    def learning_b(self):
        return self.learning

    cache_responses = [
                    'Aaaaaaaaaaaaah, smc??',
                    'Entendi mano...',
                    'Poooode',
                    'Vdd',
                    'Pode',
                    'Dmr',
                    'Aham',
                    'Huum',
                    'Hum'
                    ]
    cache_responses_ask = [
                    'Ham?',
                    'Am?',
                    'O que então?',
                    'Ué??',
                    'Não??',
                    'Então?',
                    '???',
                    '?',
                    '???'
                    ]

    def get_answer(self, message, domitson):
        if domitson:
            watson.answer(message, self)
        else:
            temp_message = message.lower()

            if not self.learning:
                if temp_message == 'errado' or \
                    temp_message == 'n' or \
                    temp_message == 'não' or \
                    temp_message == 'nao' or \
                    temp_message == 'er':

                    self.learning = True
                    self.get_message(self.cache_responses_ask[random.randint(0, len(self.cache_responses_ask)-1 )] + ('?' * random.randint(0, 10)) )
                else:
                    self.last_message = message
                    mouth.answer(message, self)
            else:
                self.bot.train([self.last_message, message])
                self.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )])
                self.learning = False

# Messages Region
    def get_message(self, message):
        self.driver.find_element_by_xpath('//DIV[@class=\'_3u328 copyable-text selectable-text\']').send_keys(message)
        time.sleep(.5)
        self.send_message()

    def send_message(self):
        try:
            self.botao_enviar = self.driver.find_element_by_xpath('//SPAN[@data-icon=\'send\']').click()
        except:
            pass

# Conversations Region
    def add_conversation(self, cv):
        conversations_to_listen[cv.id] = cv
        print('DEBUG LOG: Adding conversation %s to the list' % cv.id)

        if len(str(self.current_conversation)) == 0:
            self.set_conversation(cv.id)
            cv.click()

    def set_conversation(self, cv_id):
        if self.current_conversation != conversations_to_listen[cv_id]:
            self.current_conversation = conversations_to_listen[cv_id]
            self.current_conversation.click()
            print('DEBUG LOG: Current conversation id: %s' % cv_id)

    def get_conversation(self):
        return self.current_conversation

    def get_conversations(self):
        return conversations_to_listen

# Access Region
    def google_b(self):
        return google

    password = '@roizz3'

# Admin Command Region
    def send_cmd(self, cmd):
        splited_command = cmd.split()

        cmd = splited_command[0]
        mod = splited_command[1]
        arg = splited_command[2]
        pasw = splited_command[3]

        if mod == 'password' and pasw == self.password:
            self.password = arg
            self.get_message('Password changed successfully!')
            return

        if pasw != self.password:
            print(pasw)
            print(self.password)
            self.get_message('Wrong password, you dick!')
            return

        for module in modules:
            temp_module = str(module)

            if mod in temp_module:
                module.command(arg)
                temp_message = '%s bot setted to %s' % (mod, arg)
                self.get_message(temp_message)
                print('DEBUG CORE: %s...' % temp_message)
                break

    print('DEBUG CORE: Soul Bot Initialized...')
