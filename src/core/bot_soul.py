# -*- coding: utf-8 -*-

import os, time, random
import xml.etree.cElementTree as ET

from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
# logging.basicConfig(level=logging.INFO)

# Bot Modules
from core.modules.entity.bot_brain import BotBrain
from core.modules.entity.bot_ears import BotEars
from core.modules.entity.bot_mouth import BotMouth

from core.modules.general.bot_climate import BotClimate
from core.modules.general.bot_events import BotEvent
from core.modules.general.bot_help import BotHelp
from core.modules.general.bot_images import BotImages
from core.modules.general.bot_news import BotNews
from core.modules.general.bot_wikipedia import BotWikipedia

from core.modules.google.bot_google import BotGoogle

from core.modules.watson.bot_watson import BotWatson
from core.modules.watson.bot_watson_images import BotWatsonImages

# Modules Started
brain = BotBrain()
ears = BotEars()
mouth = BotMouth()

climate = BotClimate()
events = BotEvent()
aid = BotHelp()
images = BotImages()
news = BotNews()
wiki = BotWikipedia()

google = BotGoogle()

watson = BotWatson()
watson_images = BotWatsonImages()

# WolframAlpha Configuration
#app_id = "U32UR2-EXW6X24J7A"

# Bot Configuration
conversations_to_listen = []

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
    watson,
    watson_images    
]

class CoreBot:
    print('DEBUG CORE: Initializing Soul Bot..')

# Initalization Region
    def __init__(self, bot_name, main):
        self.bot = ChatBot(
            bot_name,
            logic_adapters=[
                "chatterbot.logic.BestMatch",
                #'chatterbot.logic.MathematicalEvaluation',
            ],
            )

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        print("DEBUG CORE: Path:", self.dir_path)

        # self.trainer = ChatterBotCorpusTrainer(self.bot)

        # self.trainer.train("chatterbot.corpus.portuguese")
        
        self.trainer = ListTrainer(self.bot)

        # self.set_train('train_models')

        self.current_conversation = {'id_conversation': 0, 'name_conversation': '', 'conversation': ''}
        self.last_version = '1.0.0.0'
        self.bot_version = '1.0.1.0'
        self.bot_main = main
        self.contacts_numbers = 0
        self.loaded_diary = False

        self.chrome = self.dir_path+'\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)
        self.driver.get('https://web.whatsapp.com/')
        # self.driver.implicitly_wait(12)

    def update(self):
        if self.learning:
            self.current_learn_time = self.current_learn_time + .01

            if self.current_learn_time >= self.max_time_to_wait_learn:
                self.get_message('Então tá né...')
                self.current_learn_time = 0
                self.learning = False

# Events Region
    def get_events(self, message):
        events.events(message, self)

    def check_events_remainder(self):
        events.check_events(self)

# Bot Events Region
    def check_bot_events(self):
        mouth.events(self)

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
        elem = self.get_message_element()
        temp_help_str = ''.join(aid.help_list)

        for part in temp_help_str.split('\n'):
            self.get_message_with_two_spaces(part)

        self.send_message()

# Images Region
    def try_download_image(self, images_links):
        return images.try_download_image(images_links, self)

    def get_elements_images(self, image_name, message):
        images.get_elements_images(image_name, self, message)

# Google Region
    def get_image(self, message):
        google.search_image(message, False, '', self)

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
            self.trainer.train(conversations)

# Bot Responses Region
    last_message = ''
    learning = False
    current_learn_time = 0
    max_time_to_wait_learn = 10
    current_count_conversation = 0

    def learning_b(self):
        return self.learning

    cache_responses = [
                    'Entendi mano...',
                    'Poooode',
                    'Vdd',
                    'Pode',
                    'Dmr',
                    'Ata',
                    'Huum',
                    'Hum'
                    ]
    cache_responses_ask = [
                    'O que então?',
                    'Ué??',
                    'Não??',
                    'Então?',
                    '?',
                    '??',
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
                self.trainer.train([self.last_message, message])
                self.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )])
                self.learning = False

    def get_answer_for_image(self, message):
        watson_images.recognize(self)

# Messages Region
    def get_message_with_one_space_before(self, message):
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        self.get_message_with_keys(message)
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    def get_message_with_one_space(self, message):
        self.get_message_with_keys(message)
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    def get_message_with_two_spaces(self, message):
        self.get_message_with_keys(message)
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        #self.send_message()

    def get_message_with_keys(self, message):
        self.get_message_element().send_keys(message)

    def get_message(self, message):
        self.get_message_with_keys(message)
        self.send_message()

    def send_message(self):
        #self.botao_enviar = self.driver.find_element_by_xpath('//SPAN[@data-icon=\'send\']').click()
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    def get_message_element(self):
        return self.driver.find_element_by_xpath('//DIV[@class=\'_3u328 copyable-text selectable-text\']')

# Conversations Region
    def add_conversation(self, cv, cv_name):
        conversations_to_listen.append({'conversation': cv, 'name_conversation': cv_name, 'id_conversation': self.current_count_conversation})
        temp_current_id = self.current_count_conversation

        if temp_current_id == 0:
            print('DEBUG CORE: WhatsApp web opened...')
            print('DEBUG CORE: %s contacts available...' % self.contacts_numbers)

            self.set_conversation(cv_name)
            cv.click()

        if len(conversations_to_listen) == self.contacts_numbers and not self.loaded_diary:
            self.loaded_diary = True
            print('DEBUG LOG: Maybe new messages, refreshing and updating diary')
            mouth.start(self)

        print('DEBUG LOG: Conversation [id: %s - name: %s] - added to the list' % (temp_current_id, cv_name))
        self.current_count_conversation += 1

    def set_conversation(self, cv_name):
        temp_cv_name = self.current_conversation['name_conversation']

        if temp_cv_name != cv_name:
            self.current_conversation = self.get_conversation_by_name(cv_name)

            ActionChains(self.driver).move_to_element(self.current_conversation['conversation']).click().perform();

            print('DEBUG LOG: Changed to conversation [id: %s - name: %s]' % (self.current_conversation['id_conversation'], cv_name))
            self.bot_main.last_message = ''
            
    def get_conversation(self):
        return self.current_conversation

    def get_conversations(self):
        return conversations_to_listen

    def get_conversation_by_name(self, cv_name):
        for d in conversations_to_listen:
            if cv_name in d['name_conversation']:
                return d

        return None
    def get_conversation_name_by_id(self, cv_id):
        for d in conversations_to_listen:
            if cv_id == conversations_to_listen[d].id:
                return d

# Access Region
    def google_b(self):
        return google

    password = '@roizz3'

    try:
        tree = ET.parse('databases/configs.xml')
        root = tree.getroot()
        for configs in root:
            password = configs.attrib['password']

        print('DEBUG LOG:', 'Configs loaded')
    except:
        pass

# Admin Command Region
    def send_cmd(self, cmd, front, loading):
        splited_command = cmd.split()

        cmd = splited_command[0]
        mod = splited_command[1]
        arg = splited_command[2]

        if mod == 'diary':
            for d in conversations_to_listen:
                temp_current_conversation = d['name_conversation']

                if arg.lower() in temp_current_conversation and temp_current_conversation not in mouth.conversations:
                    mouth.conversations.append(d)

                    if not loading:
                        mouth.save_database(arg.lower())

                    temp_debug = 'Conversation [id: %s - name: %s] - added to my diary news!' % (d['id_conversation'], d['name_conversation'])
                    print('DEBUG LOG: %s...' % temp_debug)

                    if front:
                        self.get_message(temp_debug)
                    break
            return

        pasw = splited_command[3]

        if mod == 'test':
            if pasw == self.password:
                self.get_message('Test passed!!')
            else:
                self.get_message('Test not passed!!')

        if pasw != self.password:
            self.get_message('Wrong password, you dick!')
            return

        if mod == 'password' and pasw == self.password:
            self.password = arg
            self.get_message('Password changed successfully!')

            # try:
            #     tree = ET.parse('databases/configs.xml')
            #     root = tree.getroot()
            # except:
            root = ET.Element('config')

            password = ET.SubElement(root, 'pass', password=arg)

            tree = ET.ElementTree(root)
            tree.write('databases/configs.xml', encoding="UTF-8", xml_declaration=True)
            print('DEBUG LOG:', 'Password changed successfully to %s' % arg)
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
