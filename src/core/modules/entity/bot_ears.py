import time, wget
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from core.bot_modules_core import BotModulesCore 

class BotEars(BotModulesCore):
    def __init__(self, name, bot):
        super(BotEars, self).__init__(name, bot)

    timeout_allowed_listen = 3
    #current_timeout = 1
    last_message = None
    images_path = '\\media\\images-onitson'

    def listen_all_contacts(self, bot):
        if not self.enabled or bot.learning_b():
            return

        contacts = bot.driver.find_elements_by_xpath('(//DIV[@class=\'_2WP9Q\'])')
        bot.contacts_numbers = len(contacts)

        for cont in contacts:
            temp_name_conversation = ''

            try:
                temp_name_conversation = cont.find_element_by_class_name('_19RFN').text
            except StaleElementReferenceException:
                continue

            if bot.get_conversation_by_name(temp_name_conversation) == None:
                bot.add_conversation(cont, temp_name_conversation)

            if len(cont.find_elements_by_css_selector('span.P6z4j')) == 1 and bot.get_conversation()['name_conversation'] != temp_name_conversation:
                bot.set_conversation(temp_name_conversation)
                break

    def listen_contact(self, bot):
        not_mine_messages = bot.driver.find_elements_by_class_name('message-in')
        temp_message_id = len(not_mine_messages) - 1
        user_name = user_number = user_message = ''

        if temp_message_id >= 0:
            last_message = not_mine_messages[temp_message_id]
            
            for i in reversed(not_mine_messages):
                try:
                    if user_message == '':
                        user_message = self.get_text_by_css_selector('span.selectable-text', last_message)

                    user_number = self.get_text_by_css_selector('span.ZObjg', i)
                    user_name = self.get_text_by_css_selector('span._1F9Ap', i)
                    break
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    continue

        return {'user': user_name, 'user_number': user_number, 'message': str(user_message)}

    def get_text_by_css_selector(self, css, element):
        return element.find_element_by_css_selector(css).text