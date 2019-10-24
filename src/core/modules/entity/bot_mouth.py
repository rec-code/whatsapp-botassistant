# import wolframalpha, time

class BotMouth:
    print('DEBUG CORE: Initializing Mouth Bot...')
    enabled = True

    def answer(self, message, bot):
        if not self.enabled:
            return

        # try:
        #     client = wolframalpha.Client(bot.app_id)
        #     res = client.query(message)
        #     response = next(res.results).text
        # except:
        response = str(bot.bot.get_response(message))

        bot.get_message(response)
        #time.sleep(.5)

    def command(self, arg):
        self.enabled = True if arg == 'true' else False
        
    print('DEBUG CORE: Mouth Bot Initialized...')
