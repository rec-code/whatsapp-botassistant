import time

class BotEars:
    def listen_all_contacts(self, bot):
        contacts = bot.driver.find_elements_by_class_name('X7YrQ')

        for cont in contacts:
            if not cont.id in bot.get_conversations():
                bot.add_conversation(cont)

            temp_messages_unread = 0
            temp_info_contact = cont.text.split()
            try:
                temp_messages_unread = int(temp_info_contact[len(temp_info_contact) - 1])
            except:
                pass

            if temp_messages_unread > 0:
                try:
                    time.sleep(.5)
                    bot.set_conversation(cont.id)
                except:
                    time.sleep(.5)

    def listen_contact(self, bot):
        post = bot.driver.find_elements_by_class_name('message-in')
        ultimo = len(post) - 1
        user_message = ''

        try:
            user_message = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        except:
            pass

        return user_message
