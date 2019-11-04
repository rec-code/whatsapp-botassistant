import time


class BotBrain:
    print('DEBUG CORE: Initializing Brain Bot...')
    enabled = True

    def learn(self, message, bot):
        if not self.enabled:
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

    def command(self, arg):
        self.enabled = True if arg == 'true' else False

    print('DEBUG CORE: Brain Bot Initialized...')
