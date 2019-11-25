from core.bot_modules_core import BotModulesCore 
import time, random
from datetime import datetime
import xml.etree.cElementTree as ET

class BotEvent(BotModulesCore):
    def __init__(self, name):
        super(BotEvent, self).__init__(name)

    roles = []

    time_to_delete_role = 1440 * 60 # 24 hours to seconds = 86.400 seconds
    label_time_delete_role = int((time_to_delete_role / 60) / 60)
    print('DEBUG CORE: Setted [%s hours - %s seconds] to delete the role...' % (label_time_delete_role, time_to_delete_role))
    get_database_role_path = "databases/roles.xml"
    get_database_roles_done_path = "databases/roles_done.xml"

    cache_responses = [
        'Fala mestre',
        'Po, uma bagona monstra, né não mestre, mas xofala',
        'Então gurizão',
        'Fala meus pentelhos',
        'Meus obliterados',
        'Então meu cheetos bola',
        'Fala amor da minha vida',
    ]

    groups_terms = [
        'Boa meus felas, ai eu do valor',
        'Ai sim mestres, bagona monstra né não',
        'Huuuuuum, hoje tem rataria é???????',
        'Ratones, uma boa pa nois',
        'Placdum meus exterminadores',
    ]

    try:
        tree = ET.parse(get_database_role_path)
        root = tree.getroot()

        for event in root:
            temp_id = int(event.attrib['id'])
            temp_infos = event[0].text
            temp_remainder = int(event[1].text)
            temp_date = datetime.strptime(event[2].text, '%Y-%m-%d %H:%M:%S')
            temp_remaind = int(event[3].text)
            temp_conversation = event[4].text

            temp_confirmeds = event[5].text
            temp_confirmeds = [] if temp_confirmeds == None else temp_confirmeds.split('~~')

            temp_not_confirmeds = event[6].text
            temp_not_confirmeds = [] if temp_not_confirmeds == None else temp_not_confirmeds.split('~~')

            temp_not_confirmed_yet = event[7].text
            temp_not_confirmed_yet = [] if temp_not_confirmed_yet == None else temp_not_confirmed_yet.split('~~')

            roles.append({
                'id': temp_id, 
                'infos': temp_infos, 
                'remainder': temp_remainder, 
                'date': temp_date, 
                'remaind': temp_remaind, 
                'conversation': temp_conversation,
                'confirmeds': temp_confirmeds,
                'not_confirmeds': temp_not_confirmeds,
                'not_confirmeds_yet': temp_not_confirmed_yet
                })
            print('DEBUG LOG:', 'Event [id:', temp_id, '- conversation:', temp_conversation, '] - loaded')
    except:
        print('DEBUG LOG:', 'No events loaded')

    def events(self, message, bot):
        if not self.enabled or self.is_in_black_list(bot.current_conversation['name_conversation']):
            bot.get_message('Eventos desabilitado temporariamente')
            return
        
        temp_current_role_ammount = bot.get_current_role_ammount()

        message = message.split('\'')
        date_now = datetime.now()
        temp_roles_list = self.roles
        temp_name_conversation = bot.current_conversation['name_conversation']
        temp_role_id = None

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
                temp_role_id = int(temp_message_splited[len(temp_message_splited) - 1])
            except ValueError:

                if temp_current_role_ammount == 1:
                    temp_role_id = 0
                    temp_len_message -= 1
                else:
                    bot.get_message('Algo errado aconteceu... Tem mais de um rolê né? Se sim, ce especificou o id?')
                    return

        if len(temp_message_splited) == temp_len_message and temp_role_id is not None:
            if temp_current_role_ammount == 0:
                bot.get_message('Nenhum rolê ativo no momento pra ti ta confirmando ou não tua presença')
                return

            if temp_role_id < 0 or temp_role_id >= temp_current_role_ammount:
                bot.get_message('Id do rolê não encontrado, tente novamente guri :-p')
                return

            temp_state = 'confirmeds'

            if 'nconfirmar' in temp_message_splited[0]:
                temp_state = 'not_confirmeds'
            elif 'talvez' in temp_message_splited[0]:
                temp_state = 'not_confirmeds_yet'

            temp_current_role_id = 0
            temp_removing = False

            for r in temp_roles_list:
                if r['conversation'] != temp_name_conversation:
                    continue
                
                if temp_message_splited[1] == 'deletar' and temp_current_role_id == temp_role_id:
                    temp_roles_list.remove(r)
                    
                    tree = ET.parse(self.get_database_role_path)
                    root = tree.getroot()

                    for eve in root:
                        if temp_current_role_id == temp_role_id:
                            root.remove(eve)
                            break

                    tree = ET.ElementTree(root)
                    tree.write(self.get_database_role_path, encoding="UTF-8", xml_declaration=True)
                    
                    try:
                        tree = ET.parse(self.get_database_roles_done_path)
                        root = tree.getroot()
                    except:
                        root = ET.Element('roles_done')

                    id_elem = ET.SubElement(root, "role_done", id=str(r['id']))

                    ET.SubElement(id_elem, "info").text = str(r['infos'])
                    ET.SubElement(id_elem, "remainder").text = str(r['remainder'])
                    ET.SubElement(id_elem, "date").text = str(r['date'])
                    ET.SubElement(id_elem, "remaind").text = str(r['remaind'])
                    ET.SubElement(id_elem, "conversation").text = str(r['conversation'])
                    ET.SubElement(id_elem, "confirmeds").text = str(r['confirmeds'])
                    ET.SubElement(id_elem, "notconfirmeds").text = str(r['not_confirmeds'])
                    ET.SubElement(id_elem, "notconfirmedyet").text = str(r['not_confirmeds_yet'])

                    tree = ET.ElementTree(root)
                    tree.write(self.get_database_roles_done_path, encoding="UTF-8", xml_declaration=True)

                    bot.get_message('Role deletado, famia')
                    return

                if temp_current_role_id == temp_role_id:
                    if not temp_person_name in r[temp_state]:
                        r[temp_state].append(temp_person_name)
                    else:
                        r[temp_state].remove(temp_person_name)
                        temp_removing = True

                    temp_list = r[temp_state]
                    break

                temp_current_role_id += 1
            
            temp_pt_br_state = 'de confirmados'

            if temp_state == 'confirmeds':
                if not temp_removing:
                    bot.get_message('Boa *%s*, confirmado no rolê, chaaama <3' % temp_person_name)
                else:
                    bot.get_message(':-\\ *%s* retirado da lista de confirmados </3' % temp_person_name)

            elif temp_state == 'not_confirmeds':
                if not temp_removing:
                    bot.get_message('Oloco *%s*, ce nem vai memo?? Mas porigre então :-\\' % temp_person_name)
                else:
                    bot.get_message(':-O *%s* retirado da lista de não confirmados... Vai pia pro baile nééé?? Confirma ai, carai <3' % temp_person_name)

                temp_pt_br_state = 'de não confirmados'
            elif temp_state == 'not_confirmeds_yet':
                if not temp_removing:
                    bot.get_message('Huuuum... *%s*, se pá tu vai então?? Pode' % temp_person_name)
                else:
                    bot.get_message(':-| *%s* retirado da lista de uma possível confirmação... Cola pro bagui, fi </3' % temp_person_name)

                temp_pt_br_state = 'dos que talvez irão'

            if len(temp_list) > 0:
                bot.get_message_with_one_space('Lista %s:' % temp_pt_br_state)

                for item in temp_list:
                    bot.get_message_with_one_space(item) 

                bot.send_message()
            else:
                if temp_state == 'confirmeds':
                    bot.get_message('Oloco, ninguém vai cola famia? :\\')
                elif temp_state == 'not_confirmeds':
                    bot.get_message('Aiii sim heeein, espero que estejam todos confirmando a presença!!')
                else:
                    bot.get_message('Espero que saia do talvez para o SIM HEEEIn!!')


            tree = ET.parse(self.get_database_role_path)
            root = tree.getroot()

            temp_current_role_id = 0

            for event in root:
                if event[4].text != temp_name_conversation:
                    continue

                if temp_current_role_id == temp_role_id:

                    if temp_state == 'confirmeds':
                        if event[5].text != None:
                            event[5].text += '~~%s' % temp_person_name
                        else:
                            event[5].text = temp_person_name

                        break
                    elif temp_state == 'not_confirmeds':
                        if event[6].text != None:
                            event[6].text += '~~%s' % temp_person_name
                        else:
                            event[6].text = temp_person_name

                        break
                    else:
                        if event[7].text != None:
                            event[7].text += '~~%s' % temp_person_name
                        else:
                            event[7].text = temp_person_name

                        break
                
                temp_current_role_id += 1

            tree = ET.ElementTree(root)
            tree.write(self.get_database_role_path, encoding="UTF-8", xml_declaration=True)
            return

        if len(message) == 5:
            try:
                message[4] = message[4].strip()
                date_time = message[4].split()
                temp_remainder = -1

                if len(date_time) > 2:
                    temp_remainder = int(date_time[2])

                temp_date_splited = date_time[0].split('/')
                temp_day = int(temp_date_splited[0])
                temp_month = int(temp_date_splited[1])
                temp_year = 0

                temp_hour = int(date_time[1].split(':')[0])
                temp_minute = int(date_time[1].split(':')[1])

                if len(temp_date_splited) > 2:
                    temp_year = int(temp_date_splited[2])

                temp_place = message[3].strip()

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

                temp_label = 'Rolê: *%s*' % message[1].strip()
                
                if temp_place != '':
                    temp_label += '\nLocal: *%s*' % temp_place
                
                temp_label += '\nMarcado para: *%s*' % temp_message_date
                temp_label += '\nHorário: *%s*' % date_time[1]

                temp_remaind = 0

                if temp_remainder >= 0:
                    temp_label_minutes = ' minutos'

                    if temp_remainder == 1:
                        temp_label_minutes = ' minuto'

                    temp_label += '\nAvisar *' + str(temp_remainder) + temp_label_minutes + '* antes e depois do horário'
                    temp_remaind = 2

                bot.get_message(self.groups_terms[random.randint(0, len(self.groups_terms)-1 )])
                response = temp_label + '\nConto com vocês, filhos da puta!!!\n'
                #bot.get_message('Para saber os roles marcados digite: domi role')

                temp_roles_list.append({
                    'id': len(temp_roles_list), 
                    'infos': temp_label, 
                    'remainder': temp_remainder, 
                    'date': temp_date, 
                    'remaind': temp_remaind, 
                    'conversation': temp_name_conversation,
                    'confirmeds': [],
                    'not_confirmeds': [],
                    'not_confirmeds_yet': []
                    })

                try:
                    tree = ET.parse(self.get_database_role_path)
                    root = tree.getroot()
                except:
                    root = ET.Element('roles')

                id_elem = ET.SubElement(root, "role", id=str(len(temp_roles_list)-1))

                ET.SubElement(id_elem, "info").text = str(temp_label)
                ET.SubElement(id_elem, "remainder").text = str(temp_remainder)
                ET.SubElement(id_elem, "date").text = str(temp_date)
                ET.SubElement(id_elem, "remaind").text = str(temp_remaind)
                ET.SubElement(id_elem, "conversation").text = str(temp_name_conversation)
                ET.SubElement(id_elem, "confirmeds").text = ''
                ET.SubElement(id_elem, "notconfirmeds").text = ''
                ET.SubElement(id_elem, "notconfirmedyet").text = ''

                tree = ET.ElementTree(root)
                tree.write(self.get_database_role_path, encoding="UTF-8", xml_declaration=True)
            except:
                response = 'Mano..... Tu digitou uma caca tão grande, que eu nem entendi velho, namoral...'
        elif len(message) == 1 and 'role' in message[0].lower() or 'rolê' in message[0].lower() or 'lembrete' in message[0].lower():
            response = self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + '... Não tem nenhum role marcado \n' \
                       'Digite: domi marcar <\'nome do role\'> <\'local\'> <data> <horário> _<tempo lembrete>_\~' \
                       '*\'nome do rolê(ou lembrete)\'* entre aspas simples\n' \
                       '*\'local\'* também entre aspas simples(caso queira criar apenas um lembrete, coloque as aspas vazias *\'\'*\n' \
                       '*data* (em formato padrão, separado por barra(*/*), ex: _15/10/2020_, ano opcional(pegará o ano atual, caso não especificado))\n' \
                       '*horário* (em formato padrão, separado hora e minutos por dois pontos(*:*), ex: _16:20_, formato em 24 horas)\n' \
                       '*tempo* (em *minutos* para alertar antes e depois do horário do evento(opcional, n inclua caso não queira ser avisado))\n\~' \
                       'Ex: *domi marcar \'fumar um beckão\' \'na baia\' 24/11 16:20 10*\n' \
                       'Note que você não precisa colocar rolê no nome do evento e todo rolê marcado, fica disponível para registro, até *%s horas* a partir do horário de início do rolê <3' % self.label_time_delete_role

            if len(temp_roles_list) > 0:
                temp_has_event = False
                temp_current_role_id = 0
                temp_ammount_role = 1

                if temp_role_id == None:
                    temp_ammount_role = bot.get_current_role_ammount()
                elif temp_role_id < 0 or temp_role_id >= bot.get_current_role_ammount():
                    response = 'Id do rolê não encontrado, tente novamente guri :-p'

                for r in temp_roles_list:
                    if r['conversation'] != temp_name_conversation:
                        continue
                    
                    temp_current_role_id += 1
                    current_role_id = temp_current_role_id - 1

                    if temp_role_id != None and current_role_id != temp_role_id:
                        continue

                    if not temp_has_event:
                        if temp_ammount_role > 1:
                            bot.get_message('Salve meu meninão, da uma checada maneira nos rolês ai <3:')
                        else:
                            bot.get_message('Fala guri, da um zói no rolê ai <3:')

                        temp_has_event = True

                    temp_id_role_label = 'Rolê id: *%s*' % current_role_id

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

                        bot.send_message()

                        if temp_ammount_role == 1:

                            temp_current_id_list = 0
                            for con in r['confirmeds']:
                                if temp_current_id_list == 0:
                                    bot.get_message_with_two_spaces('*Irão comparecer* <3')

                                temp_current_id_list += 1
                                bot.get_message_with_one_space('%s - %s' % (temp_current_id_list, con))

                            temp_current_id_list = 0
                            for not_con_yet in r['not_confirmeds_yet']:
                                if temp_current_id_list == 0:
                                    bot.get_message_with_one_space_before_and_after('*Talvez comparecerão* :-|')

                                temp_current_id_list += 1
                                bot.get_message_with_one_space('%s - %s' % (temp_current_id_list, not_con_yet))

                            temp_current_id_list = 0
                            for not_con in r['not_confirmeds']:
                                if temp_current_id_list == 0:
                                    bot.get_message_with_one_space_before_and_after('*Não irão comparecer* :-(')

                                temp_current_id_list += 1
                                bot.get_message_with_one_space('%s - %s' % (temp_current_id_list, not_con))

                            if temp_current_id_list != 0:
                                bot.send_message()
                    else:
                        temp_role_name = ''

                        for part in temp_sentence.split('\n'):
                            if 'rolê' in part.lower():
                                temp_role_name = part.replace('Rolê: ', '')

                        bot.get_message('%s - %s - %s' % (temp_id_role_label, temp_role_name, temp_message_date))

                if temp_has_event:
                    if temp_ammount_role > 1:
                        response = 'Para mais detalhes do evento, digite: domi role *<id do role>*'
                    else:
                        response = ''
                    
                    # for part in response.split('\n'):
                    #     bot.get_message_with_one_space(part) 

                    # bot.send_message()
                    # response = ''
        else:
            response = 'Iiii pia, deu alguma merda, n consegui marca o rolê não...'
        
        #if response != '':
        for i in response.split('\~'):
            for part in i.split('\n'):
                bot.get_message_with_two_spaces(part)

            bot.send_message()

    def check_events(self, bot):
        temp_now = datetime.now()
        conv_amounts = {}

        for r in self.roles:
            time_remaing_second = temp_now - r['date']
            time_remaing = r['date'] - temp_now
            
            if r['remaind'] > 0:
                temp_remaing_to_reach = int(r['remainder']) * 60

                if time_remaing.days < 1 and time_remaing.days > -2 and (time_remaing.seconds <= temp_remaing_to_reach and r['remaind'] == 2 or time_remaing.seconds > temp_remaing_to_reach and time_remaing_second.seconds >= temp_remaing_to_reach and r['remaind'] == 1):
                    r['remaind'] -= 1

                    if r['remaind'] == 0:
                        print('DEBUG LOG: Avisando que o rolê já começou: ', r['infos'])
                        temp_resp = self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', ta tendo rolê já faz '
                    else:
                        print('DEBUG LOG: Avisando que o rolê vai começar: ', r['infos'])
                        temp_resp = self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + ', vai te rolê em '

                    temp_label_minutes = ' minutos'

                    if int(r['remainder']) == 1:
                        temp_label_minutes = ' minuto'

                    response = temp_resp + str(r['remainder']) + temp_label_minutes +', saca as infos:\n' + \
                        r['infos']

                    bot.set_conversation(r['conversation'])
                    #bot.get_message(response)
                    temp_message_date = ''
                    
                    if time_remaing.days == 0:
                        temp_message_date = 'Hoje'
                    elif time_remaing.days == -1:
                        temp_message_date = 'Ontem'
                    elif time_remaing.days == 1:
                        temp_message_date = 'Amanhã'

                    for part in response.split('\n'):
                        if 'marcado' in part.lower():
                            part = 'Marcado para: *%s*' % temp_message_date

                        bot.get_message_with_two_spaces(part)

                    bot.send_message()
                    break
            
            if time_remaing_second.days >= 1:
                print('DEBUG LOG: Role %s deletado' % r)
                bot.set_conversation(r['conversation'])
                bot.get_message('Salve meus raposos, lembra do role:')

                for part in r['infos'].split('\n'):
                    if 'rolê' in part.lower():
                        temp_role_name = part.replace('Rolê: ', '')
                    
                temp_message_date = 'o dia ' + str(r['date'].date().strftime("%d de %b de %Y"))
                
                if time_remaing.days == 0:
                    temp_message_date = 'Hoje'
                elif time_remaing.days == -1:
                    temp_message_date = 'Ontem'
                elif time_remaing.days == 1:
                    temp_message_date = 'Amanhã'

                for part in r['infos'].split('\n'):
                    if 'marcado' in part.lower():
                        temp_message_date = 'Marcado para: %s' % temp_message_date

                bot.get_message('Rolê %s - *%s*' % (temp_role_name, temp_message_date))
                bot.get_message('Então... Ele foi deletado. Espero que tenham/estejam curtido/curtindo o bagui, \n*Uma boa pa nóis famia!!!*')

                #self.events('domi deletar role %s')
                tree = ET.parse(self.get_database_role_path)
                root = tree.getroot()

                for eve in root:
                    if int(eve.attrib['id']) == r['id']:
                        root.remove(eve)
                        break

                tree = ET.ElementTree(root)
                tree.write(self.get_database_role_path, encoding="UTF-8", xml_declaration=True)
                
                try:
                    tree = ET.parse(self.get_database_roles_done_path)
                    root = tree.getroot()
                except:
                    root = ET.Element('roles_done')

                id_elem = ET.SubElement(root, "role", id=str(r['id']))

                ET.SubElement(id_elem, "info").text = str(r['infos'])
                ET.SubElement(id_elem, "remainder").text = str(r['remainder'])
                ET.SubElement(id_elem, "date").text = str(r['date'])
                ET.SubElement(id_elem, "remaind").text = str(r['remaind'])
                ET.SubElement(id_elem, "conversation").text = str(r['conversation'])
                ET.SubElement(id_elem, "confirmeds").text = str(r['confirmeds'])
                ET.SubElement(id_elem, "notconfirmeds").text = str(r['not_confirmeds'])
                ET.SubElement(id_elem, "notconfirmedyet").text = str(r['not_confirmeds_yet'])

                tree = ET.ElementTree(root)
                tree.write(self.get_database_roles_done_path, encoding="UTF-8", xml_declaration=True)

                self.roles.remove(r)

                if len(self.roles) != 0:
                    print('DEBUG LOG: Rolês ainda existentes: ', len(self.roles))
                else:
                    print('DEBUG LOG: Nenhum rolê restante')
                break