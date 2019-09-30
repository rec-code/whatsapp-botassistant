import wolframalpha, time


class BotMouth:
    def answer(self, message, bot):
        print(message)

        try:
            client = wolframalpha.Client(bot.app_id)
            res = client.query(message)
            response = next(res.results).text
        except:
            response = bot.bot.get_response(message)

        response = str(response)
        bot.get_message(response)
        time.sleep(1)
        try:
            bot.send_button = bot.driver.find_element_by_class_name('_3M-N-')
        except:
            return

        bot.send_button.click()