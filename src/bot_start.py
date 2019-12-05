# -*- coding: utf-8 -*-
from bot_main import MainBot

main_bot = MainBot()
main_bot.start()

while not main_bot.web_opened:
	main_bot.bot.listen(1)

while True:
	main_bot.update()
	main_bot.bot.update()