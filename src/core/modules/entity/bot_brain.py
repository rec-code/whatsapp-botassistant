import time
from core.bot_modules_core import BotModulesCore 

class BotBrain(BotModulesCore):
    def __init__(self, name, bot):
        super(BotBrain, self).__init__(name, bot)

    def learn(self, message, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            bot.get_message('Cérebro desabilitado temporariamente')
            return

        error_message = 'Não entendi seus ensinamentos, mestre jedi'

        message = message.replace('aprender', '')
        message = message.replace('ensinar', '')

        if message.find('?') != -1:
            #message = message.lower()
            message = message.replace('?', '?*')
            message = message.split('*')

            new_knowledge = []

            for element in message:
                element = element.strip()
                new_knowledge.append(element)

            bot.trainer.train(new_knowledge)
            bot.get_message('Huuuum, vlw truta, vai servir no futuro tipo uma bagona monstra')
        else:
            bot.get_message(error_message)