import random
import xml.etree.cElementTree as ET
from core.bot_modules_core import BotModulesCore 
from datetime import datetime

class BotGame(BotModulesCore):
    def __init__(self, name, bot):
        super(BotGame, self).__init__(name, bot)
        self.get_database_games_path = self.bot.root_path + "databases/games/"
        self.get_database_old_path = self.get_database_games_path + "oldlady/"
        self.get_database_ranking_old_path = self.get_database_old_path + 'rankingold.xml'
        self.get_database_matchs_old_path = self.get_database_old_path + 'matchsold.xml'
        self.load_configs()

        self.game_pixels = [' - ' for x in range(9)]

        self.white_chess = ['♕', '♔', '♗', '♘', '♖', '♙']
        self.black_chess = ['♛', '♚', '♝', '♞', '♜', '♟' ]

        self.game_chess_pixels = list(range(64))
        k = 0
        for i in self.game_chess_pixels:
            k += 1 if i % 8 == 0 else 0
            j = i
            j += 1 if k % 2 == 0 else 0
            
            temp_chess = self.black_chess

            if k == 7 or k == 8:
                temp_chess = self.white_chess

            if k == 2 or k == 7:
                self.game_chess_pixels[i] = ' %s ' % temp_chess[5]

                if k == 2:
                    self.game_chess_pixels[i] = self.game_chess_pixels[i].strip()
            elif k == 1 or k == 8:
                if i % 7 == 0:
                    self.game_chess_pixels[i]= ' %s ' % temp_chess[4]
                elif i % 8 == 1 or i % 8 == 6:
                    self.game_chess_pixels[i] = ' %s ' % temp_chess[3]
                elif i % 8 == 2 or i % 8 == 5:
                    self.game_chess_pixels[i] = ' %s ' % temp_chess[2]
                elif i % 8 == 4:
                    self.game_chess_pixels[i] = ' %s ' % temp_chess[1]
                elif i % 8 == 3:
                    self.game_chess_pixels[i] = ' %s ' % temp_chess[0]

            else:
                self.game_chess_pixels[i] = ' ▉ ' if j % 2 == 0 else ' ☏ '

        self.searchs_after_win = [
            'you win',
            'você ganhou',
            'você é demais',
            'você destruiu',
            'você',
            'ai sim'
        ]
        self.searchs_after_veia = [
            'jogo da velha', 
            'osso', 
            'foi bom enquanto durou', 
            'motivação', 
            'empatou', 
            'obrigado por jogarem'
            ]

    def load_configs(self):
        temp_path = self.get_database_ranking_old_path
        self.players = []

        try:
            self.load_ranking(temp_path)

            temp_log = 'Game old lady ranking loaded'
        except FileNotFoundError:
            self.create_rankings()
            temp_log = 'Game old lady ranking file not found, creating one'

        self.printi(temp_log)

        temp_path = self.get_database_matchs_old_path
        self.matchs = []
       
        try:
            self.load_matchs(temp_path)

            temp_log = 'Game old lady matchs loaded'
        except FileNotFoundError:
            self.create_matchs()
            temp_log = 'Game old lady matchs file not found, creating one'

        self.printi(temp_log)

    def game(self, user, number, inp, current_conversation, game_id):
        if not self.enabled:
            return

        if user == '':
            self.bot.get_message('Ossado, não consegui ler seu nome, tente de novo pf')
            return
        
        if game_id == 0:
            self.old_game(user, number, inp, current_conversation, current_conversation['game_old'])
        else:
            self.chess_game(user, inp, current_conversation, current_conversation['game_chess'])

    def old_game(self, user, number, inp, current_conversation, temp_game):
        temp_vacancies = temp_game['vacancies']

        if inp == '':
            self.bot.get_message('Sério memo?')
            return

        temp_user_ingame = False
        temp_user_char = temp_user_label = ''
        temp_users = temp_game['players']
        temp_slots = temp_game['game']

        for i in temp_users:
            if i['number'] == number:
                temp_user_ingame = True
                temp_user_char = i['char']
                temp_user_label = i['label']

#            temp_users.append({'label': i['label'], 'number': i['number'], 'winner': False, 'char': temp_user_char})

        if inp == 'reset':
            if len(temp_users) > 0:
                self.erase_game(temp_game)
                self.bot.get_message('Peido, bora, quem vai pra batalha')
            else:
                self.bot.get_message('Er')
            return
        elif inp == 'board':
            self.load_board(temp_slots, 'Naruto', 'Hinata', 3)
            return
        elif inp == 'partidas':
            self.bot.get_message_with_two_spaces('║-------*Old Lady - Últimas 10 partidas*-------║')

            if len(self.matchs) != 0:
                for i in range(10):
                    try:
                        temp_match = reversed(self.matchs[i])
                        players = temp_match['players'].split('~~')

                        player_1 = players[0].split(':')
                        player_2 = players[1].split(':')

                        temp_winner = 'A velha' if temp_match['winner'] == ':' else temp_match['winner'].split(':')[0]

                        temp_match_label = '║--%s - %s | %s vs %s | Ganhador: %s--║' % (i, temp_match['date'], player_1[1], player_2[1], temp_winner)
                        self.bot.get_message_with_one_space(temp_match_label)
                    except IndexError:
                        break

                self.bot.send_message()
            else:
                self.bot.get_message('║--*Nenhum registro disponível AINDA*--║')

            return
        elif inp == 'ranking':
            self.bot.get_message_with_one_space('║-------*Old Lady - Ranking*-------║')
            self.bot.get_space()
            self.bot.get_message_with_one_space('║-----------*Burguesia*----------║')

            for i in range(10):
                temp_title = 'Buiu'
                temp_rank = self.players[i]
                temp_victorys = temp_rank['victorys']

                if i == 0:
                    temp_title = 'Mestre'
                elif i == 1:
                    temp_title = 'Primo'
                elif i == 2:
                    temp_title = 'Greiso'
                elif i > 7:
                    temp_title = 'Fahrid'

                if i == 3:
                    self.bot.get_space()
                    self.bot.get_message_with_one_space('║-------Prolerariado-------║')

                label_victory = 'vitórias' if temp_victorys > 1 else 'vitória'
                
                temp_label_rank = '║---*%sº | %s: %s | %s ' +  '%s*---║' % label_victory  

                if i == 1 or i == 2:
                    temp_label_rank = temp_label_rank.replace('*', '_')
                elif i > 2:
                    temp_label_rank = temp_label_rank.replace('*', '')

                self.bot.get_message_with_one_space(temp_label_rank % ((i+1), temp_title, temp_rank['label'], temp_victorys))

            self.bot.send_message()
            return
        # elif len(inp) != 6:
        #     self.bot.get_message('Meu queridão, nova regra... Obrigatório o nome ter 6 caracteres, GO')
        #     return

        if temp_vacancies == 0 and not temp_user_ingame:
            self.bot.get_message('Sai fora %s, que ce nem ta no game, licença' % user.split()[0])
            return
        elif temp_vacancies > 0:

            if temp_user_ingame:
                self.bot.get_message('Tu já ta no game, idiota')
                return

            temp_added = False

            for i in self.players:
                if i['number'] == number:
                    temp_added = True
                    break

            if not temp_added:
                self.players.append({'number': number, 'label': inp, 'victorys': 0})

            x_o = random.randint(0, 2)
            x_taked = True if temp_vacancies == 1 and temp_users[0]['char'] == 'x' else False

            #x = False if x_o != 0 and not x_taked else True
            char = 'x' if (not x_taked and (temp_vacancies == 1 or x_o == 1)) else '◎'

            temp_users.append({'number': number, 'label': inp, 'char': char})

            self.bot.get_message('Fala, "_%s_" vai ser o %s' % (inp, char.upper()))
            
            temp_label_response = 'Os campeões foram selecionados, que inicie o combate!'

            if temp_vacancies == 2:
                temp_label_response = 'Eae, quem vai ser o oponente???'
        
            self.bot.get_message(temp_label_response)

            temp_game['vacancies'] -= 1
            return
        elif temp_user_ingame:
            if temp_game['last_move'] == user:
                self.bot.get_message('%s, não é sua vez, queta o facho ai' % user)
                return

            temp_idx = None

            try:
                temp_idx = int(inp) - 1

                if temp_idx < 0 > 9:
                    raise ValueError
            except ValueError:
                self.bot.get_message('Truta... Vai se foder, só números de 1 a 9, carai')
                return

            if temp_game['game'][temp_idx] != ' - ':
                self.bot.get_message('Ai não né meu pia, ta me tirando smc??')
                return

            temp_game['game'][temp_idx] = '%s' % temp_user_char
            temp_game['last_move'] = user

            self.load_board(temp_slots, temp_users[0]['label'], temp_users[1]['label'], 3)

            j = temp_user_char
            temp_winner = ''

            cb = [0, 0, 0, 1, 2, 2, 3, 6]
            app = [1, 3, 4, 3, 2, 3, 1, 1]
            old = True
            finished = False

            for i, k in enumerate(cb):
                same = empty = False
                update = True
                first_char = ''
                line = []
                empty_len = empty_id = 0
                value = k

                for j in range(3):
                    char = ''

                    if j == 0:
                        first_char = char = temp_slots[value]
                    else:
                        value += app[i]
                        char = temp_slots[value]

                        if char != ' - ' and first_char == char:
                            if update:
                                same = True
                        else:
                            same = update = False
                            #break

                    if char == ' - ':
                        empty = True
                        empty_id = j
                        empty_len += 1

                    line.append(char)

                if old:
                    if empty_len == 1:
                        local_same = False
                        last_char = ''

                        for k in line:
                            if line[empty_id] == k:
                                continue
                            elif last_char == '':
                                last_char = k
                            elif last_char == k:
                                local_same = True

                        if local_same:
                            old = False
                    elif empty_len > 1 and old:
                        old = False

                if not same:
                    continue
                else:
                    finished = True
                    old = False
                    break

            winner = loser = num_winner = ''

            if finished or old:
                for i in temp_users:
                    if i['number'] == number:
                        winner = i['label']
                        num_winner = i['number']
                    else:
                        loser = i['label']

                if not old:
                    for i in self.players:
                        if i['number'] == number:
                            i['victorys'] += 1
                            break

                self.players = sorted(self.players, key = lambda i: i['victorys'], reverse=True)
                self.save_match(temp_users, winner, num_winner)
                self.save_ranking()
                self.finish_game(winner, loser, old, temp_game)


    def chess_game(self, user, inp, current_conversation, temp_game):
        if inp == 'board':
            self.load_board(temp_game['game'], 'Sasuke', 'Sakura', 8)
            return

    def load_board(self, game, user_one, user_two, board_size):
        game_name = 'Jogo da Old Lady'

        if board_size == 8:
            game_name = 'Xadrezin'

        self.bot.get_message_with_one_space('║------ *%s* ------║' % game_name)
        self.bot.get_message_with_one_space('║------ _%s_ *vs* _%s_ ------║' % (user_one, user_two))

        bz = board_size + 1

        for i in range(1, bz):
            k = (i * (bz-1))
            temp_slots_board = '                 ║'
            
            temp_slots_board = temp_slots_board[board_size:]
            
            for i in range(1, bz):
                temp_slots_board += '%s║' % game[k-(bz-i)]

            self.bot.get_message_with_one_space(temp_slots_board)
        
        self.bot.send_message()

    def finish_game(self, winner, loser, old, game):
        temp_message = self.searchs_after_win[random.randint(0, len(self.searchs_after_win) -  1)]

        if not old:
            self.bot.get_message('Boa *_%s_*, mais uma vitória pra conta!!' % winner)
            self.bot.get_message('Já o *_%s_*, mais uma derrota pra conta, parabéns!' % winner)
        else:
            self.bot.get_message('Deu veia smc??? Assa, ceis ta tirano po')
            temp_message = self.searchs_after_veia[random.randint(0, len(self.searchs_after_veia) -  1)]

        # self.bot.get_image(temp_message)
        self.erase_game(game)

    def erase_game(self, game):
        game['game'] = [x for x in self.game_pixels]
        game['players'] = []
        game['vacancies'] = 2
        game['last_move'] = ''

    def load_ranking(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        for ranking in root:
            rank = ranking.attrib['stats']

            self.players.append({'label': rank.split('~~')[0], 'victorys': int(rank.split('~~')[1]), 'number': rank.split('~~')[2]})
        
        self.players = sorted(self.players, key = lambda i: i['victorys'], reverse=True) 
    
    def load_matchs(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        for match in root:
            date = match[0].text
            players = match[1].text
            winner = match[2].text
            board = match[3].text
            
            self.matchs.append({'date': date, 'players': players, 'winner': winner, 'board': board})

    def save_match(self, users, winner, num_winner):
        path = self.get_database_matchs_old_path
        
        tree = ET.parse(path)
        root = tree.getroot()

        match = ET.SubElement(root, 'id', id=len(self.matchs))

        temp_date = str(self.get_time_and_date())
        temp_players = '%s:%s:%s~~%s:%s:%s' % (users[0]['number'], users[0]['label'], users[0]['char'], users[1]['number'], users[1]['label'], users[1]['char'])
        temp_winner = '%s:%s' % (str(num_winner), winner)

        ET.SubElement(match, "date").text = temp_date
        ET.SubElement(match, "players").text = temp_players
        ET.SubElement(match, "winner").text = temp_winner
        ET.SubElement(match, "board").text = str(self.game_pixels)

        ET.ElementTree(root).write(path, encoding="UTF-8", xml_declaration=True)
        self.matchs.append({'date': temp_date, 'players': temp_players, 'winner': temp_winner, 'board': str(self.game_pixels)})

    def save_ranking(self):
        path = self.get_database_ranking_old_path
        
        root = ET.Element('ranking')
        
        temp_ranking = [self.players[x] for x in range(10)]

        for i in temp_ranking:
            ET.SubElement(root, 'rank', stats='%s~~%s~~%s' % (i['label'], i['victorys'], i['number']))

        ET.ElementTree(root).write(path, encoding="UTF-8", xml_declaration=True)

    def create_rankings(self):
        path = self.get_database_ranking_old_path
        root = ET.Element('ranking')

        for i in range(10):
            ET.SubElement(root, 'rank', stats='player~~0~~0')

        ET.ElementTree(root).write(path, encoding="UTF-8", xml_declaration=True)

    def create_matchs(self):
        path = self.get_database_matchs_old_path
        root = ET.Element('matchs')

        # for i in range(10):
        #     ET.SubElement(root, 'rank', stats='player~~0~~0')

        ET.ElementTree(root).write(path, encoding="UTF-8", xml_declaration=True)