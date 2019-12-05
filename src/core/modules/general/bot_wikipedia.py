import wikipedia, time

from core.bot_modules_core import BotModulesCore 


class BotWikipedia(BotModulesCore):
    def __init__(self, name, bot):
        super(BotWikipedia, self).__init__(name, bot)
        wikipedia.set_lang("pt")

    wiki_request = {}

    def wiki(self, message, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
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
            bot.get_message_with_one_space('Foram encontrados ' + str(len(search)) + ' resultados sobre ' + '*'+message+'*' + '.' +' ')
            bot.send_message()

            for se in search:
                temp_message = '*%s* - *%s*' % (str(count), se.title())
                bot.get_message_with_one_space(temp_message)
                self.wiki_request[count] = se.title()
                count += 1

            bot.send_message()
            temp_message = 'Digite o número em que deseja obter a info™'
        else:
            temp_message = 'Não foi encontrado nenhum resultado, tente escrever igual ao ser humano.'
            temp = True

        bot.get_message(temp_message)

        return temp

    def select_wikipedia(self, option, bot):
        try:
            temp_option = int(option)
        except:
            if 'cancelar' in option or 'deixa baixo' in option:
                bot.get_message('Pode pá, truta')
                return True

            bot.get_message('Opção inválida, tente novamente')
            return False

        if temp_option < len(self.wiki_request):
            self.show_wikipedia(self.wiki_request[temp_option], bot)
            return True
        else:
            bot.get_message('Opção acima dos resultados, digite um número corretamente.')
            return False

    def show_wikipedia(self, page, bot):
        temp_page = wikipedia.page(page)

        temp_message = '*_%s_*' % temp_page.title
        temp_message += '\n' + wikipedia.summary(page)

        bot.get_message(temp_message)
        bot.get_image(temp_page.title)
        time.sleep(.5)
        bot.get_message('*Veja mais em:* %s' % temp_page.url)