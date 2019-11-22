import random
from datetime import datetime
import xml.etree.cElementTree as ET

from core.bot_modules_core import BotModulesCore 

class BotSupply(BotModulesCore):
    def __init__(self, name):
        super(BotSupply, self).__init__(name)

    supplys = []
    get_database_supply_path = "databases/supplys.xml"

    cache_responses = [
        'Então velho',
        'Olha...',
        'A lista de compra? Opa',
        'Meu vegano, olha ai',
        'Fala meu novembro choroso',
        'Então meu malagueto',
        'Então meu coração gelado',
    ]

    groups_terms = [
        'O piazada... Frutas e verduras, tlg...',
        'Compra do mês pro restaurante',
        'Compra da família',
        'Intera de churrasco',
        'Churrasco vegano lista de compra',
    ]

    try:
        tree = ET.parse(get_database_supply_path)
        root = tree.getroot()

        for event in root:
            temp_id = int(event.attrib['id'])
            temp_infos = event[0].text
            temp_date = datetime.strptime(event[1].text, '%Y-%m-%d %H:%M:%S')

            temp_price = float(event[2].text)
            temp_conversation = event[3].text
            temp_total = float(event[4].text)

            temp_supplys_str = event[5].text
            temp_supplyers = {}

            if temp_supplys_str != None:
                for sup in temp_supplys_str.split('~~'):
                    temp_s = sup.split(':')

                    temp_supplyers[temp_s[0]] = float(temp_s[1])

            supplys.append({
                'id': len(supplys), 
                'infos': temp_infos, 
                'date': temp_date, 
                'g_price': temp_price, 
                'conversation': temp_conversation,
                'total': temp_total,
                'items': temp_supplyers,
            })
            print('DEBUG LOG:', 'Supply [id:', temp_id, '- conversation:', temp_conversation, '] - loaded')
    except:
        print('DEBUG LOG:', 'No supplys loaded')

    def supply(self, message, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            return

        temp_current_supplys_ammount = bot.get_current_supply_ammount()

        message = message.split('\'')
        temp_supplys_list = self.supplys
        print(message)
        date_now = datetime.now()
        temp_name_conversation = bot.current_conversation['name_conversation']
        temp_supply_id = None
        temp_message_splited = []
        temp_person_name = ''

        if len(message) == 3:
            temp_message_splited = message[2].split()
        elif len(message) == 1:
            temp_message_splited = message[0].split()

        if len(message) != 1:
            try:
                temp_person_name = message[1]
            except:
                bot.get_message('Vei, se pá tu esqueceu de coloca seu nome')
                return

        temp_len_message = 3

        if len(temp_message_splited) == 2 or len(temp_message_splited) == temp_len_message:
            try:
                temp_supply_id = int(temp_message_splited[len(temp_message_splited) - 1])
            except ValueError:

                if temp_current_supplys_ammount == 1:
                    temp_supply_id = 0
                    temp_len_message -= 1
                else:
                    bot.get_message('Algo errado aconteceu... Tem mais de uma intera né? Se sim, ce especificou o id?')
                    return
                
        if len(temp_message_splited) == temp_len_message and temp_supply_id is not None:
            if temp_current_supplys_ammount == 0:
                bot.get_message('Nenhuma lista aqui truta pra ti ta mexendo... Cria uma ai, po')
                return

            if temp_supply_id < 0 or temp_supply_id >= temp_current_supplys_ammount:
                bot.get_message('Id da intera não encontrada, tente novamente guri')
                return

            temp_state = 'items'
            temp_user_value = 0

            # if 'nconfirmar' in temp_message_splited[0]:
            #     temp_state = 'not_confirmeds'
            # elif 'talvez' in temp_message_splited[0]:
            #     temp_state = 'not_confirmeds_yet'

            temp_removing = temp_updating_value = False
            temp_current_supply_id = temp_total = 0

            for r in temp_supplys_list:
                if r['conversation'] != temp_name_conversation:
                    continue
                
                if temp_message_splited[1] == 'deletar' and temp_current_supply_id == temp_supply_id:
                    temp_supplys_list.remove(r)

                    tree = ET.parse(self.get_database_supply_path)
                    root = tree.getroot()

                    for sup in root:
                        temp_id = int(sup.attrib['id'])
                        if temp_id == temp_supply_id:
                            root.remove(sup)
                            break

                    tree = ET.ElementTree(root)
                    tree.write(self.get_database_supply_path, encoding="UTF-8", xml_declaration=True)

                    bot.get_message('Lista deletada, famia')
                    return

                try:
                    temp_user_value = float(temp_message_splited[0])

                    if temp_user_value <= 0:
                        bot.get_message('Velho, o valor não pode ser menor ou igual a zero, né po...')
                        return
                except:
                    bot.get_message('Man, se pá tu digitou o valor que tu vai interar errado')
                    return
                

                if temp_current_supply_id == temp_supply_id:

                    if temp_person_name == 'preço':
                        r['g_price'] = temp_user_value

                        temp_infos = ''
                        
                        print(r['infos'].split('\n'))

                        for part in r['infos'].split('\n'):
                            if 'preço' in part.lower():
                                part = 'Preço da *_G_*: ' + str('R$ *%.2f*' % temp_user_value)

                            temp_infos += ('\n'+part)

                        temp_infos = temp_infos[1:len(temp_infos)]
                        r['infos'] = temp_infos

                        bot.get_message('Opa meu bacanal.. O preço da intera de id *%s* foi atualizado com sucesso, para R$ *%.2f* a grama, pode pá' % (temp_supply_id, temp_user_value))
                        return

                    if not temp_person_name in r[temp_state]:
                        r[temp_state][temp_person_name] = temp_user_value
                        r['total'] += temp_user_value
                    else:
                        if r[temp_state][temp_person_name] != temp_user_value:
                            r['total'] -= r[temp_state][temp_person_name]
                            r['total'] += temp_user_value
                            r[temp_state][temp_person_name] = temp_user_value
                            temp_updating_value = True
                        else:
                            r['total'] -= temp_user_value
                            del r[temp_state][temp_person_name]
                            temp_removing = True

                    temp_list = r[temp_state]
                    temp_total = r['total']
                    break
                
                temp_current_supply_id += 1
            
            temp_pt_br_state = 'dos interados'

            if temp_state == 'items':
                if not temp_removing:
                    bot.get_message('Boa *%s*, R$ _*%.2f*_ conto pra intera, vai da *%s*, demoro???' % (temp_person_name, temp_user_value, self.get_weight_label(temp_user_value / r['g_price'])))
                else:
                    bot.get_message('*%s* retirado da lista da intera' % temp_person_name)


            if len(temp_list) > 0:
                bot.get_message_with_two_spaces('*_Lista %s_*:' % temp_pt_br_state)

                for item in temp_list:  
                    bot.get_message_with_one_space('*%s* - R$ *_%.2f_* = *%s*' % (item, temp_list[item], self.get_weight_label(temp_list[item] / r['g_price'])))
                
                bot.get_message_with_one_space_before('*_Total atual da intera_*: R$ *_%.2f_* contos (*%s*)' % (temp_total, self.get_weight_label(temp_total / r['g_price'])))

                bot.send_message()
            else:
                if temp_state == 'items':
                    bot.get_message('Oloco, nenhum pa intera??')


            tree = ET.parse(self.get_database_supply_path)
            root = tree.getroot()

            temp_current_supply_id = 0

            for sup in root:
                if sup[3].text != temp_name_conversation:
                    continue

                if temp_current_supply_id == temp_supply_id:
                    if temp_state == 'items':
                        if sup[5].text != None:
                            temp_new_string = ''

                            if temp_updating_value or temp_removing:
                                for s in sup[5].text.split('~~'):
                                    temp_splited = s.split(':')

                                    if temp_splited[0] == temp_person_name:
                                        if temp_removing:
                                            continue
                                        else:
                                            temp_splited[1] = temp_user_value

                                    temp_new_string += '~~%s:%s' % (temp_splited[0], temp_splited[1])

                                sup[5].text = temp_new_string[2:len(temp_new_string)]
                            else:                                        
                                sup[5].text += '~~%s:%s' % (temp_person_name, temp_user_value)
                        else:
                            sup[5].text = '%s:%s' % (temp_person_name, temp_user_value)

                        print(sup[5].text)
                        sup[4].text = str(temp_total) 
                        break

                temp_current_supply_id += 1

            tree = ET.ElementTree(root)
            tree.write(self.get_database_supply_path, encoding="UTF-8", xml_declaration=True)
            return

        if len(message) == 5:
            try:
                message[4] = message[4].strip()
                date_time = message[4].split()

                temp_date_splited = date_time[0].split('/')
                temp_day = int(temp_date_splited[0])
                temp_month = int(temp_date_splited[1])
                temp_year = 0

                temp_hour = int(date_time[1].split(':')[0])
                temp_minute = int(date_time[1].split(':')[1])

                if len(temp_date_splited) > 2:
                    temp_year = temp_date_splited[2]

                temp_price = 0

                try:
                    temp_price = float(message[3].strip())

                    if temp_price <= 0:
                        bot.get_message('Velho, o valor da intera não pode ser menor ou igual a zero, né po...')
                        return
                except:
                    bot.get_message('Se pá tu não digitou uma valor de intera incorreto, meu pia...')
                    return
            except:
                bot.get_message('Something went wrong, try again little bastard...')
                return

            if temp_year == 0:
                temp_year = date_now.year

            temp_date = datetime(temp_year, temp_month, temp_day, temp_hour, temp_minute)

            temp_remaing_days = temp_date - date_now

            temp_message_date = 'O dia ' + date_time[0]
            
            if temp_remaing_days.days == 0:
                temp_message_date = 'Hoje'
            elif temp_remaing_days.days == -1:
                temp_message_date = 'Ontem??? Ué idiota'
            elif temp_remaing_days.days == 1:
                temp_message_date = 'Amanhã'

            temp_label = 'Intera: *%s*' % message[1].strip() + \
                         '\nMarcado para: *%s*' % temp_message_date + \
                         '\nPreço da *_G_*: %s' % str('R$ *%.2f*' % temp_price) + \
                         '\nHorário: *%s*' % date_time[1]

            bot.get_message(self.groups_terms[random.randint(0, len(self.groups_terms)-1 )])
            response = temp_label + '\nSigilo hein rapeize, smc... E cuidado com essas poha de radin ai, carai!!!\n'
            #bot.get_message('Para saber os roles marcados digite: domi role')

            temp_supplys_list.append({
                'id': len(temp_supplys_list), 
                'infos': temp_label, 
                'date': temp_date, 
                'g_price': temp_price, 
                'conversation': temp_name_conversation,
                'total': float(0),
                'items': {},
#                    'not_confirmeds': [],
#                    'not_confirmeds_yet': []
                })
            try:
                tree = ET.parse(self.get_database_supply_path)
                root = tree.getroot()
            except:
                root = ET.Element('supplys')

            id_elem = ET.SubElement(root, "supply", id=str(len(temp_supplys_list)-1))

            ET.SubElement(id_elem, "infos").text = str(temp_label)
            ET.SubElement(id_elem, "date").text = str(temp_date)
            ET.SubElement(id_elem, "g_price").text = str(temp_price)
            ET.SubElement(id_elem, "conversation").text = str(temp_name_conversation)
            ET.SubElement(id_elem, "total").text = '0'
            ET.SubElement(id_elem, "items").text = ''

            tree = ET.ElementTree(root)
            tree.write(self.get_database_supply_path, encoding="UTF-8", xml_declaration=True)
            #except:
                #response = 'Tenta de novo ai truta, se pá tu errou algo...'
        elif len(message) == 1 and 'intera' in message[0].lower() or 'inteira' in message[0].lower():
            response = self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + '... Não tem nenhuma lista de compra \n' \
                       'Digite: domi intera \'nome da intera\' \'preço da g(separado por \".\" e.g: *2.5*)\' data horário' \
                       '*\'nome da intera\'* entre aspas simples\n' \
                       '*\'preço da g\'* apenas *números*, caso decimal, coloque um *.* para separar real dos centavos\n' \
                       '*data*(em formato padrão, ex: 20/04/2020, ano opcional) \n' \
                       '*horário* em horas:minutos(24 horas formato)\n' \
                       'Ex: *domi intera \'salada vegan\' \'2.2\' 26/11 16:20*\n' \
                       'Note que você não precisa colocar intera no nome e toda intera, fica disponível para registro, até a data e hora da intera'

            if len(temp_supplys_list) > 0:
                temp_has_supply = False
                temp_current_supply_id = 0
                temp_ammount_role = 1

                if temp_supply_id == None:
                    temp_ammount_role = bot.get_current_supply_ammount()
                elif temp_supply_id < 0 or temp_supply_id >= bot.get_current_supply_ammount():
                    response = 'Id da intera não encontrado, tente novamente guri :-p'

                for r in temp_supplys_list:
                    if r['conversation'] != temp_name_conversation:
                        continue
                    
                    temp_current_supply_id += 1
                    current_supply_id = temp_current_supply_id - 1

                    if temp_supply_id != None and current_supply_id != temp_supply_id:
                        continue

                    if not temp_has_supply:
                        if temp_ammount_role > 1:
                            bot.get_message('Então pia, no sapatin, fraga nas situação:')
                        else:
                            bot.get_message('Vdd pia, a intera ai:')

                        temp_has_supply = True

                    temp_id_role_label = 'Intera id: *%s*' % current_supply_id

                    temp_remaing_days = r['date'] - date_now

                    temp_message_date = 'o dia ' + str(r['date'].date().strftime("%d de %b de %Y"))

                    if temp_ammount_role > 1:
                        temp_message_date = temp_message_date.replace('o dia', 'dia')

                    if temp_remaing_days.days == 0:
                        temp_message_date = 'Hoje'
                    elif temp_remaing_days.days == -1:
                        temp_message_date = 'Ontem'
                    elif temp_remaing_days.days == 1:
                        temp_message_date = 'Amanhã'
                    
                    temp_sentence = r['infos']

                    if temp_ammount_role == 1:
                        bot.get_message_with_two_spaces(temp_id_role_label)

                        for part in temp_sentence.split('\n'):
                            if 'marcado' in part.lower():
                                part = 'Marcado para: *%s*' % temp_message_date

                            bot.get_message_with_two_spaces(part)

                        if r['total'] != 0:
                            bot.get_message_with_keys('*_Total atual da intera_*: R$ *_%.2f_* contos (*%s*)' % (r['total'], self.get_weight_label(r['total'] / r['g_price'])))

                        bot.send_message()

                        if temp_ammount_role == 1:
                            temp_current_id_list = 0

                            for con in r['items']:
                                if temp_current_id_list == 0:
                                    bot.get_message_with_one_space('*_Galera da intera_*:')

                                temp_current_id_list += 1
                                bot.get_message_with_one_space_before('%s - *%s* - R$ *%.2f* contos = *%s*' % (temp_current_id_list, con, r['items'][con], self.get_weight_label(r['items'][con] / r['g_price'])))

                            bot.send_message()
                    else:
                        temp_supply_name = ''

                        for part in temp_sentence.split('\n'):
                            if 'intera' in part.lower():
                                temp_supply_name = part.replace('Intera: ', '')

                        bot.get_message('%s - %s - %s' % (temp_id_role_label, temp_supply_name, temp_message_date))

                if temp_has_supply:
                    # if temp_ammount_role > 1:
                    #     response = 'Para mais detalhes do evento, digite: domi role *<id do role>*'
                    # else:
                    response = 'Eh o bicho famia'

                    # response = '\n*Qualquer coisa ceis joga o cel no mato piazada, smc*'
                    
                    # for part in response.split('\n'):
                    #     bot.get_message_with_one_space(part) 

                    # bot.send_message()
                    # response = ''
        else:
            response = 'Mano, deu algo erradissimo, try again ai meu pastel de palmito...'

        for part in response.split('\n'):
            bot.get_message_with_two_spaces(part)

        bot.send_message()

    def get_weight_label(self, weight):
        temp_weight_division = round(weight / 1000, 3)

        temp_label = 'g'
        temp_result = '%.2f' % weight

        if temp_weight_division >= 1:
            temp_label = 'kg'

            if temp_weight_division % 1 == 0.0:
                temp_result = temp_weight_division
            else:
                temp_result = '%.3f' % temp_weight_division

        return '%s%s' % (temp_result, temp_label)