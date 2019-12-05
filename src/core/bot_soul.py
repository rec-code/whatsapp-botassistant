# -*- coding: utf-8 -*-

import os, time, random, platform
import xml.etree.cElementTree as ET

from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
# logging.basicConfig(level=logging.INFO)

# Mine
from functions import Functions

# Bot Modules
from core.modules.entity.bot_brain import BotBrain
from core.modules.entity.bot_ears import BotEars
from core.modules.entity.bot_mouth import BotMouth

from core.modules.general.bot_climate import BotClimate
from core.modules.general.bot_events import BotEvent
from core.modules.general.bot_help import BotHelp
from core.modules.general.bot_images import BotImages
from core.modules.general.bot_news import BotNews
from core.modules.general.bot_supply import BotSupply
from core.modules.general.bot_wikipedia import BotWikipedia

from core.modules.google.bot_google import BotGoogle
from core.modules.google.bot_media import BotMedia

from core.modules.misc.bot_game import BotGame

class CoreBot(Functions):
    conversations_to_listen = []

    last_message = ''
    learning = False
    current_learn_time = 0
    max_time_to_wait_learn = 10
    current_count_conversation = 0
    password = '@roizz3'

# Initalization Region
    def __init__(self, bot_name, main):
        self.system = platform.system()
        self.printi('The bot is starting in the %s system' % self.system)
        self.printi('Initializing Soul Bot', 'core')

        self.bot = ChatBot(
            bot_name,
            logic_adapters=[
                "chatterbot.logic.BestMatch",
                #'chatterbot.logic.MathematicalEvaluation',
            ],
            )

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.root_path = os.getcwd() + '/'
        
        self.bot_main = main

        self.printi('Root Path: ' + self.root_path, 'core')
        self.printi('Core Path: ' + self.dir_path, 'core')
        self.load_configs()
        self.load_modules()

        # self.trainer = ChatterBotCorpusTrainer(self.bot)

        # self.trainer.train("chatterbot.corpus.portuguese")
        
        self.trainer = ListTrainer(self.bot)

        # self.set_train('train_models')

        self.printi('Setting up the web browser', 'core')

        chrome_driver_path = 'chromedriver.exe'
        #chrome_driver_path = 'geckodriver'
        profile_path = 'wpp_%s' % self.system.lower()

        self.chrome = self.dir_path+'/%s' % chrome_driver_path
        self.options = webdriver.ChromeOptions()
        #self.options = webdriver.FirefoxOptions()

        self.options.add_argument(r"user-data-dir="+self.root_path+"profile/" + profile_path)
        self.printi('Opening the browser and WhatsApp web address', 'core')
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)
        self.driver.get('https://web.whatsapp.com/')

        self.current_conversation = {
            'name_conversation': ''
            }

        self.last_version = '1.0.0.0'
        self.bot_version = '1.0.1.0'
        self.contacts_numbers = 0
        self.loaded_diary = False
        self.printi('Soul Bot Initialized', 'core')

    def update(self):
        if self.learning:
            self.current_learn_time = self.current_learn_time + .01

            if self.current_learn_time >= self.max_time_to_wait_learn:
                self.get_message('Então tá né...')
                self.current_learn_time = 0
                self.learning = False

# Supply Region
    def get_supply(self, message):
        self.supply.supply(message, self)

# Game Region
    def get_game(self, user, number, inp, game_id):
        user = user.strip()
        inp = inp.strip()
        number = number.strip()
        self.game.game(user, number, inp, self.current_conversation, game_id)

# Inter Message Region
    def get_inter_message(self, dic_message):
        temp_to = dic_message['to_conv']

        conv = self.get_conversation_by_name(temp_to)

        if conv is None:
            self.get_message('Contato ou grupo(*%s*) não encontrado, tente novamente.' % temp_to)
            return

        self.set_conversation(temp_to)

        temp_from = dic_message['from']
        temp_anon = True if temp_from.lower() == 'anon' else False
        temp_number = dic_message['number']
        temp_to_who = dic_message['to']
        temp_subject = dic_message['subject']
        temp_message = dic_message['message']

        temp_who = 'Anônimo' if temp_anon else '(*%s*) @%s' % (temp_from, temp_number)
        label = 'Telegrama' if random.randint(0, 2) == 0 else 'Trombeta'

        self.get_message_with_one_space('|------*%s da Ônika*------|' % label)
        self.get_message_with_keys('De: %s' % temp_who)

        if not temp_anon:
            self.mention_someone()

        self.get_space()

        self.get_message_with_keys('Para: @%s' % temp_to_who)

        if temp_to_who.lower() != 'geral': 
            self.mention_someone()
        
        self.get_space()
        self.get_message_with_one_space_before_and_after('*%s*' % temp_subject)
        self.get_message('_%s_' % temp_message)

    def mention_someone(self):
        to = None
        clicked = False

        while to is None and not clicked:
            try:
                temp_container = self.driver.find_element_by_css_selector('div._15EmS')
                to = temp_container.find_element_by_css_selector('div._1Yz8K')

                try:
                    to.click()
                    clicked = True
                except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                    pass
            except NoSuchElementException:
                self.printi('I did not find the container or contact to click')

# Events Region
    def get_events(self, message):
        self.events.events(message, self)

    def check_events_remainder(self):
        self.events.check_events(self)

# Bot Events Region
    def check_bot_events(self):
        self.mouth.events(self)

# News Region
    def get_news(self, action_id, top_br):
        if action_id == 0:
            self.news.news_tech(self)
        else:
            self.news.news(top_br, self)

# Climate Region
    def get_climate(self, mode, region):
        self.climate.climate(mode, region, self)

# Wikipedia Region
    def get_wikipedia(self, action_id, message):
        if action_id == 0:
            return self.wiki.wiki(message, self)
        else:
            return self.wiki.select_wikipedia(message, self)

# Help Region
    def get_help(self, module):
        helps = self.aid.get_help(module)

        if helps == None:
            self.get_message('Então meu... Módulo não encontrado, digite o nome corretamente')
            self.get_message_with_two_spaces('Disponíveis: eventos, intera, aprender, noticia, wiki, google, media, game e trombeta')
            self.get_message('Digite *ajuda* _nome do módulo_ para ver a lista de comandos desse módulo')
            return
        
        temp_help_str = ''.join(helps)

        for p in temp_help_str.split('\\~'):
            for part in p.split('\n'):
                self.get_message_with_two_spaces(part)
            self.send_message()

# Images Region
    # def try_download_image(self, images_links):
    #     return images.try_download_image(images_links, self)

    def try_download_image(self, images_links, amount):
        return self.images.try_download_image(images_links, amount, self)

    def get_elements_images(self, images_names, message):
        temp_images = []

        for image_name in images_names:
            if self.system != 'Linux':
                image_name = image_name.replace('/', '\\')
            temp_images.append(image_name)

        self.images.get_elements_images(temp_images, self, message)

# Google Region
    def get_image(self, message):
        self.google.search_image(message, self)

    def get_search(self, message):
        self.google.search(message, self)

    def get_video_or_spotify(self, message, domain_search):
        self.media.search(message, domain_search, self)

# Bot Listen Region
    def listen(self, action_id):
        if action_id == 0:
            return self.ears.listen_contact(self)
        else:
            self.ears.listen_all_contacts(self)

# Bot Learning Region
    def set_learn(self, message):
        self.brain.learn(message, self)

    def set_train(self, folder_name):
        temp_path_folder = self.dir_path + '/' + folder_name

        for train_models in os.listdir(temp_path_folder):
            conversations = open(temp_path_folder+'/'+train_models, encoding='utf-8').readlines()
            self.trainer.train(conversations)

# Bot Responses Region
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
                    self.current_conversation['last_message'] = message
                    self.mouth.answer(message, self)
            else:
                self.trainer.train([self.current_conversation['last_message'], message])
                self.get_message(self.cache_responses[random.randint(0, len(self.cache_responses)-1 )])
                self.learning = False

    # def get_answer_for_image(self, message):
    #     watson_images.recognize(self)

# Messages Region
    def get_message_with_one_space_before(self, message):
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        self.get_message_with_keys(message)
        
    def get_message_with_one_space(self, message):
        self.get_message_with_keys(message)
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    def get_message_with_one_space_before_and_after(self, message):
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        self.get_message_with_keys(message)
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    def get_message_with_two_spaces(self, message):
        self.get_message_with_keys(message)
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        #self.send_message()
    def get_space(self):
        ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    def get_message_with_keys(self, message):
        self.get_message_element().send_keys(message)

    def get_message(self, message):
        self.get_message_with_keys(message)
        self.send_message()

    def send_message(self):
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    def get_message_element(self):
        return self.driver.find_element_by_xpath('//DIV[@class=\'_3u328 copyable-text selectable-text\']')

# Conversations Region
    def add_conversation(self, cv, cv_name):
        temp_role_ammount = self.get_role_ammount(cv_name)

        self.conversations_to_listen.append({
            'conversation': cv, 
            'name_conversation': cv_name, 
            'id_conversation': self.current_count_conversation,
            'conversation_role_ammount': temp_role_ammount,
            'last_message': '',
            'game_old': {
                'game':[x for x in self.game.game_pixels],
                'players': [],
                'vacancies': 2,
                'last_move' : ''
                },
            'game_chess': {
                'game':[x for x in self.game.game_chess_pixels],
                'players': [],
                'vacancies': 2,
                'last_move' : ''
                }
            })

        temp_current_id = self.current_count_conversation

        if temp_current_id == 0:
            self.printi('WhatsApp web opened', 'core')
            self.bot_main.web_opened = True
            self.printi('%s contacts available...' % self.contacts_numbers, 'core')

            self.set_conversation(cv_name)
            cv.click()

        # if len(self.conversations_to_listen) == self.contacts_numbers and not self.loaded_diary:
        #     self.loaded_diary = True
        #     self.printi('Maybe new messages, refreshing and updating diary')
        #     self.mouth.start(self)

        #self.printi('[id: %s - "%s" - events: %s] - conv added' % (temp_current_id, cv_name, temp_role_ammount), 'inline')
        self.current_count_conversation += 1

    current_timeout_set_conversation = 1

    def set_conversation(self, cv_name):
        temp_cv_name = self.current_conversation['name_conversation']

        if temp_cv_name != cv_name:
            self.current_conversation = self.get_conversation_by_name(cv_name)

            try:
                ActionChains(self.driver).move_to_element(self.current_conversation['conversation']).click().perform();
                self.current_conversation['conversation'].click()
            except:
                if self.current_timeout_set_conversation < 3:
                    self.current_timeout_set_conversation += 1
                    self.printi('Failed to set the conversation, trying again, attempt %s...' % self.current_timeout_set_conversation)
                    self.set_conversation(cv_name)
                    return
                else:
                    self.bot_main.printi('Failed to set the conversation, check this shit modafoca')
                    self.current_timeout_set_conversation = 1
                    return
            
            self.current_timeout_set_conversation = 1
            self.printi('Changed to [id: %s - "%s"]' % (self.current_conversation['id_conversation'], cv_name), 'inline')
            #self.bot_main.last_message = ''
            
    def get_conversation(self):
        return self.current_conversation

    def get_conversations(self):
        return self.conversations_to_listen

    def get_conversation_by_name(self, cv_name):
        for d in self.conversations_to_listen:
            if cv_name in d['name_conversation']:
                return d
        return None
    
    def check_conversation_by_name(self, cv_name):
        for d in self.conversations_to_listen:
            if cv_name.lower() in d['name_conversation'].lower():
                return d['name_conversation']
        return None

    def get_conversation_name_by_id(self, cv_id):
        for d in self.conversations_to_listen:
            if cv_id == self.conversations_to_listen[d].id:
                return d

    def get_current_role_ammount(self):
        temp_current_ammount = 0
        temp_cv_name = self.current_conversation['name_conversation']

        for r in self.events.roles:
            if temp_cv_name == r['conversation']:
                temp_current_ammount += 1
        
        return temp_current_ammount

    def get_current_supply_ammount(self):
        temp_current_ammount = 0
        temp_cv_name = self.current_conversation['name_conversation']

        for r in self.supply.supplys:
            if temp_cv_name == r['conversation']:
                temp_current_ammount += 1
        
        return temp_current_ammount

    def get_role_ammount(self, cv_name):
        temp_current_ammount = 0

        for r in self.events.roles:
            if cv_name == r['conversation']:
                temp_current_ammount += 1
        
        return temp_current_ammount
# Access Region
    def google_b(self):
        return self.google

    def load_configs(self):
        temp_path = self.root_path + 'databases/configs.xml'

        try:
            tree = ET.parse(temp_path)
            root = tree.getroot()

            for configs in root:
                self.password = configs.attrib['password']

            temp_log = 'Configs loaded'
        except FileNotFoundError:
            root = ET.Element('config')

            ET.SubElement(root, 'conf', password=self.password)

            ET.ElementTree(root).write(temp_path, encoding="UTF-8", xml_declaration=True)
            temp_log = 'Config file not found, creating one'

        self.printi(temp_log)

    def load_modules(self):
        self.printi('Starting loading modules', 'core')

        # Modules Started
        self.brain = BotBrain('Brain', self)
        self.ears = BotEars('Ears', self)
        self.mouth = BotMouth('Mouth', self)

        self.climate = BotClimate('Climate', self)
        self.events = BotEvent('Events', self)
        self.aid = BotHelp('Help', self)
        self.images = BotImages('Images', self)
        self.news = BotNews('News', self)
        self.supply = BotSupply('Supply', self)
        self.wiki = BotWikipedia('Wiki', self)

        self.google = BotGoogle('Google', self)
        self.media = BotMedia('Media', self)

        self.game = BotGame('Game', self)

        self.modules = [
            self.brain,
            self.ears,
            self.mouth,

            self.climate,
            self.events,
            self.aid,
            self.images,
            self.news,
            self.supply,
            self.wiki,
            
            self.google,
            self.media,

            self.game,
        ]        
        self.printi('Modules loaded successfully', 'core')

# Admin Command Region
    def send_cmd(self, cmd, front, loading):
        splited_command = cmd.split()

        cmd = splited_command[0]
        mod = splited_command[1]
        arg = splited_command[2]

        if mod == 'diary':
            for d in self.conversations_to_listen:
                temp_current_conversation = d['name_conversation']

                if arg.lower() in temp_current_conversation.lower() and temp_current_conversation not in self.mouth.conversations:
                    self.mouth.conversations.append(temp_current_conversation)

                    if not loading:
                        self.mouth.save_database_in(arg.lower())

                    temp_debug = '%s - added to my diary news!' % d['name_conversation']
                    self.printi(temp_debug)

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

        temp_name_conv = None

        if len(splited_command) > 4:
            temp_name_conv = splited_command[4]

        if  mod == 'module' and \
            temp_name_conv is not None:
            
            temp_name_conv = self.check_conversation_by_name(temp_name_conv)

            if temp_name_conv is not None:
                for module in self.modules:
                    temp_module = str(module)

                    if arg.lower() in temp_module:
                        module.set_black_list(temp_name_conv, self)
                        return

                self.get_message('Sorry, module not found')
            else:
                self.get_message('Conversation not found')

            return

        if mod == 'password' and pasw == self.password:
            self.password = arg
            self.get_message('Password changed successfully!')

            # try:
            #     tree = ET.parse('databases/configs.xml')
            #     root = tree.getroot()
            # except:
            root = ET.Element('config')

            ET.SubElement(root, 'conf', password=arg)

            ET.ElementTree(root).write('databases/configs.xml', encoding="UTF-8", xml_declaration=True)
            self.printi('Password changed successfully to %s' % arg)
            return

        for module in self.modules:
            temp_module = str(module)

            if mod in temp_module:
                module.command(arg)
                temp_message = '%s bot setted to %s' % (mod, arg)
                self.get_message(temp_message)
                self.printi(temp_message, 'core')
                break