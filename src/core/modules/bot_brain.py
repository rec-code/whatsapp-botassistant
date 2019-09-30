import time


class BotBrain:
    def learn(self, message, bot):
        frase_inicial = 'bot: Escreva a pergunta e após o ? a resposta.'
        frase_final = 'bot: Obrigado por ensinar! Agora já sei!'
        frase_erro = 'bot: Você escreveu algo errado! Comece novamente..'

        bot.get_message('aprendendo...' + message)
        time.sleep(1)
        bot.send_message()
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

            novo = []
            for elemento in message:
                elemento = elemento.strip()
                novo.append(elemento)

            bot.bot.train(novo)
            bot.caixa_de_mensagem.send_keys(frase_final)
            time.sleep(1)
            bot.send_message()
        else:
            bot.caixa_de_mensagem.send_keys(frase_erro)
            time.sleep(1)
            bot.send_message()
