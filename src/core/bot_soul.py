# -*- coding: utf-8 -*-

import os, time, random

from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver

# logging.basicConfig(level=logging.INFO)

# modules
from core.modules.bot_brain import BotBrain
from core.modules.bot_climate import BotClimate
from core.modules.bot_ears import BotEars
from core.modules.bot_events import BotEvent
from core.modules.bot_help import BotHelp
from core.modules.bot_mouth import BotMouth
from core.modules.bot_news import BotNews
from core.modules.bot_wikipedia import BotWikipedia

brain = BotBrain()
climate = BotClimate()
ears = BotEars()
events = BotEvent()
aid = BotHelp()
mouth = BotMouth()
news = BotNews()
wiki = BotWikipedia()

app_id = "U32UR2-EXW6X24J7A"

conversations_to_listen = {}

class CoreBot:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    current_conversation = ''

    def __init__(self, bot_name):
        self.bot = ChatBot(
            bot_name,
            logic_adapters=[
                "chatterbot.logic.BestMatch",
                #'chatterbot.logic.MathematicalEvaluation',
            ],
            )

        self.bot.set_trainer(ListTrainer)
        self.set_train('train_models')

        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train(
        "chatterbot.corpus.portuguese",
        #"chatterbot.corpus.english",
        )

        print("Real path is : ", self.dir_path)
        self.chrome = self.dir_path+'\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    def start(self, initial_contact):
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)

        # self.caixa_de_pesquisa = self.driver.find_element_by_class_name('_2zCfw')
        # self.caixa_de_pesquisa.send_keys(initial_contact)
        time.sleep(2)
        print(initial_contact)
        # self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(initial_contact))
        # self.contato.click()
        # time.sleep(2)

    def listen(self, action_id):
        if action_id == 0:
            return ears.listen_contact(self)
        else:
            ears.listen_all_contacts(self)

    def get_events(self, message):
        events.events(message, self)

    def check_events_remainder(self):
        events.check_events(self)

    def get_news(self, action_id, top_br):
        if action_id == 0:
            news.news_tech(self)
        else:
            news.news(top_br, self)

    def get_answer(self, message):
        mouth.answer(message, self)

    def set_learn(self, message):
        brain.learn(message, self)

    def get_climate(self, mode):
        climate.climate(mode, self)

    def get_wikipedia(self, action_id, message):
        if action_id == 0:
            return wiki.wiki(message, self)
        else:
            return wiki.select_wikipedia(message, self)

    def get_help(self):
        self.send_message_pattern(aid.help_list)

    def send_message_pattern(self, message):
        self.get_message(message)
        time.sleep(1)
        self.send_message()

    def get_message(self, message):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_3u328')
        self.caixa_de_mensagem.send_keys(message)

    def send_message(self):
        try:
            self.botao_enviar = self.driver.find_element_by_class_name('_3M-N-')
            self.botao_enviar.click()
        except:
            pass

    def bye(self, message):
        temp_greets = random.randint(0, len(message) - 1)

        if type(message) == list:
            frase = message[temp_greets]
            self.get_message(frase)
            time.sleep(1)
            self.send_message()
            time.sleep(1)

    def set_train(self, folder_name):
        temp_path_folder = self.dir_path + '/' + folder_name

        for train_models in os.listdir(temp_path_folder):
            conversations = open(temp_path_folder+'/'+train_models, encoding='utf-8').readlines()
            self.bot.train(conversations)

    def get_conversations(self):
        return conversations_to_listen

    def add_conversation(self, cv):
        conversations_to_listen[cv.id] = cv
        print('Adding conversation %s to the list' % cv.id)

        if len(str(self.current_conversation)) == 0:
            self.set_conversation(cv.id)
            cv.click()

    def get_conversation(self):
        return self.current_conversation

    def set_conversation(self, cv_id):
        if self.current_conversation != conversations_to_listen[cv_id]:
            self.current_conversation = conversations_to_listen[cv_id]
            self.current_conversation.click()
            print('Current conversation id: %s' % cv_id)
