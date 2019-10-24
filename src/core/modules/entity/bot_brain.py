import time


class BotBrain:
    print('DEBUG CORE: Initializing Brain Bot...')
    enabled = True

    def learn(self, message, bot):
        if not self.enabled:
            bot.get_message('Cérebro desabilitado temporariamente')
            return


        start_message = 'bot: Escreva a pergunta e após o ? a resposta.'
        result = 'bot: Obrigado por ensinar! Agora já sei!'
        error_message = 'bot: Você escreveu algo errado! Comece novamente..'

        bot.get_message('aprendendo...' + message)
        #      self.x = True
        #      while self.x == True:
        #          texto = self.escuta()
        message = message.replace('aprender', '')
        message = message.replace('ensinar', '')

        if message.find('?') != -1:
            # texto = texto.replace('domi', '')
            message = message.lower()
            message = message.replace('?', '?*')
            message = message.split('*')

            new = []
            for element in message:
                element = element.strip()
                new.append(element)

            bot.bot.train(new)
            bot.get_message(result)
        else:
            bot.get_message(error_message)

    def command(self, arg):
        self.enabled = True if arg == 'true' else False

    print('DEBUG CORE: Brain Bot Initialized...')
