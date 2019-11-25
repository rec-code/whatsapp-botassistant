import time, wget
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from core.bot_modules_core import BotModulesCore 

class BotEars(BotModulesCore):
    def __init__(self, name):
        super(BotEars, self).__init__(name)

    def listen_all_contacts(self, bot):
        if not self.enabled or bot.learning_b():
            return

        #contacts = bot.driver.find_elements_by_class_name('X7YrQ')
        contacts = bot.driver.find_elements_by_xpath('(//DIV[@class=\'_2WP9Q\'])')
        # contacts.reverse()
        # new_messages = bot.driver.find_elements_by_xpath('//SPAN[@class=\'P6z4j\']')
        bot.contacts_numbers = len(contacts)
        # print(bot.contacts_numbers)

        for cont in contacts:
            #print(cont)
            temp_name_conversation = ''

            try:
                temp_name_conversation = cont.find_element_by_class_name('_19RFN').text
            except StaleElementReferenceException:
                continue

            if bot.get_conversation_by_name(temp_name_conversation) == None:
                bot.add_conversation(cont, temp_name_conversation)

            if len(cont.find_elements_by_css_selector('span.P6z4j')) == 1 and bot.get_conversation()['name_conversation'] != temp_name_conversation:
                time.sleep(.5)
                bot.set_conversation(temp_name_conversation)
                time.sleep(.5)
                break

        # for mes in new_messages:

    timeout_allowed_listen = 3
    current_timeout = 1
    last_message = None
    images_path = '\\media\\images-onitson'

    def listen_contact(self, bot):
        not_mine_messages = bot.driver.find_elements_by_class_name('message-in')
        # all_messages = bot.driver.find_elements_by_css_selector('span.selectable-text')
        # not_mine_messages = []

        # for mes in all_messages:
        #     temp_mes = mes.find_element_by_xpath('..')

        #     if 'message-in' in temp_mes.get_attribute('class'):
        #         not_mine_messages.append(mes)

        # not_mine_messages.reverse()
        #all_messages = bot.driver.find_elements_by_class_name('message-in')
        temp_message_id = len(not_mine_messages) - 1
        user_message = ''

        if temp_message_id >= 0:
            #print('DEBUG LOG: Trying get message, attempt %s...' % self.current_timeout)

            last_message = not_mine_messages[temp_message_id]

            try:
                user_message = last_message.find_element_by_css_selector('span.selectable-text').text
            except NoSuchElementException:
               pass
            except StaleElementReferenceException:
                pass
 
                # if self.current_timeout < self.timeout_allowed_listen:
                #     self.current_timeout = self.current_timeout + 1
                #     print('DEBUG LOG: Did not get the message, retrying attempt %s...' % self.current_timeout)
                #     user_message = self.listen_contact(bot)
                # else:
                #     print('DEBUG LOG: Could not get the message, returning an empty message...')
                #pass
                
        temp_is_image = False
        temp_image_path = None

        if user_message != self.last_message:
            # user_image = None
            # try:
            #     print('DEBUG LOG: Maybe image? Lets see...')
            #     user_image = last_message.find_element_by_class_name('_18vxA').get_attribute('src')
            #     print('DEBUG LOG: Image found...')
            #     print(user_image) 

            #     temp_is_image = True

            #     temp_image_path = wget.download(user_image, bot.dir_path + self.images_path)
            #     print(temp_image_path)
            #     bot.watson_images.recognize(bot, temp_image_path)
            # except:
            #     pass  

            #print('DEBUG LOG: Message read successfully, answering...')
            self.last_message = user_message
            self.current_timeout = 1

        return user_message