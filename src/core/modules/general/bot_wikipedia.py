import wikipedia, time

wikipedia.set_lang("pt")


class BotWikipedia:
    print('DEBUG CORE: Initializing Wikipedia Bot...')
    enabled = True

    wiki_request = {}

    def wiki(self, message, bot):
        if not self.enabled:
            bot.get_message('Wikipedia Pesquisas desabilitado temporariamente')
            return True

        search = None

        try:
            message = message.strip()
            search = wikipedia.search(message)
            temp = False
        except:
            temp_message = 'Algo errado aconteceu, tente novamente!'
            return True

        if len(search) == 1:
            temp_message = search[0]
            self.show_wikipedia(temp_message, bot)
            return True
        elif len(search) > 1:
            count = 1
            self.wiki_request = {}
            temp_message = 'Foram encontrados ' + str(len(search)) + ' resultados sobre ' + '*'+message+'*' + '.' +'\nDigite o número em que deseja obter a info:\n'

            for se in search:
                temp_message += str(count) + ' - ' + se.title() + '\n'
                self.wiki_request[count] = se.title()
                count += 1
        else:
            temp_message = 'Não foi encontrado nenhum resultado, tente escrever igual ao ser humano.'
            temp = True

        bot.get_message(temp_message)

        return temp

    def select_wikipedia(self, option, bot):
        # temp_option = 0

        try:
            temp_option = int(option)
        except:
            temp_message = 'Opção inválida, tente novamente'
            if 'cancelar' in option or 'deixa baixo' in option:
                temp_message = 'Entendido, cancelado'
                bot.get_message(temp_message)
                return True

            bot.get_message(temp_message)
            return False

        if temp_option < len(self.wiki_request):
            self.show_wikipedia(self.wiki_request[temp_option], bot)
            return True
        else:
            bot.get_message('Opção acima dos resultados, digite um número corretamente.')
            return False

    def show_wikipedia(self, page, bot):
        temp_page = wikipedia.page(page)

        temp_message = temp_page.title
        temp_message += '\n' + wikipedia.summary(page)
        temp_message += '\n' + 'Veja mais em: ' + temp_page.url

        bot.get_message(temp_message)

    def command(self, arg):
        self.enabled = True if arg == 'true' else False

    print('DEBUG CORE: Wikipedia Bot Initialized...')
