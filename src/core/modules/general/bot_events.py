import time, random
from datetime import datetime
import xml.etree.cElementTree as ET

class BotEvent:
    print('DEBUG CORE: Initializing Events Bot...')
    enabled = True

    roles = []
    time_to_delete_role = 1440 * 60 # 24 hours to seconds = 10.800 seconds
    get_database_role_path = "databases/roles.xml"
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
        'Huuuuuum, hoje tem rataria é???????'
        'Ratones, uma boa pa nois',
        'Placdum meus exterminadores',
    ]

    # try:
    #     tree = ET.parse(get_database_role_path)
    #     root = tree.getroot()

    #     for event in root:
    #         temp_id = int(event.attrib['id'])
    #         temp_infos = event[0].text
    #         temp_remainder = int(event[1].text)
    #         temp_date = datetime.strptime(event[2].text, '%Y-%m-%d %H:%M:%S')
    #         temp_remaind = int(event[3].text)
    #         temp_conversation = event[4].text
    #         roles.append({'id': temp_id, 'infos': temp_infos, 'remainder': temp_remainder, 'date': temp_date, 'remaind': temp_remaind, 'conversation': temp_conversation})
    #         print('DEBUG LOG:', 'Evento id:', temp_id, 'carregado')
    # except:
    print('DEBUG LOG:', 'No events to load')

    def events(self, message, bot):
        if not self.enabled:
            bot.get_message('Eventos desabilitado temporariamente')
            return

        message = message.split('\'')

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
                    temp_year = temp_date_splited[2]

                temp_place = message[3].strip()

                date_now = datetime.now()

                temp_message_date = 'o dia ' + date_time[0]

                if (temp_day == date_now.day and temp_month == date_now.month) and (temp_year == 0 or temp_year == date_now.year):
                    temp_message_date = 'hoje'

                temp_label = 'Rolê: *' + message[1].strip() + \
                             '*\nMarcado para: *' + temp_message_date + \
                             '*\nLocal: *' + temp_place + \
                             '*\nHorário: *' + date_time[1] + '*'

                temp_remaind = 0

                if temp_remainder >= 0:
                    temp_label_minutes = ' minutos'

                    if temp_remainder == 1:
                        temp_label_minutes = ' minuto'

                    temp_label += '\nAvisar *' + str(temp_remainder) + temp_label_minutes + '* antes e depois do horário'
                    temp_remaind = 2

                response = self.groups_terms[random.randint(0, len(self.groups_terms)-1 )] + '\n' + \
                           temp_label + \
                           '\nConto com vocês, filhos da puta!!!\n' \
                           'Para saber os roles marcados digite: domi role'

                if temp_year == 0:
                    temp_year = date_now.year

                temp_date = datetime(temp_year, temp_month, temp_day, temp_hour, temp_minute)

                self.roles.append({'id': len(self.roles), 'infos': temp_label, 'remainder': temp_remainder, 'date': temp_date, 'remaind': temp_remaind, 'conversation': bot.get_conversation().id})

                try:
                    tree = ET.parse(self.get_database_role_path)
                    root = tree.getroot()
                except:
                    root = ET.Element('roles')

                id_elem = ET.SubElement(root, "role", id=str(len(self.roles)-1))

                ET.SubElement(id_elem, "info").text = str(temp_label)
                ET.SubElement(id_elem, "remainder").text = str(temp_remainder)
                ET.SubElement(id_elem, "date").text = str(temp_date)
                ET.SubElement(id_elem, "remaind").text = str(temp_remaind)
                ET.SubElement(id_elem, "conversation").text = str(bot.get_conversation().id)

                tree = ET.ElementTree(root)
                tree.write(self.get_database_role_path, encoding="UTF-8", xml_declaration=True)
            except:
                response = 'Mano..... Tu digitou uma caca tão grande, que nem entendi velho, namoral...'
        elif len(message) == 1 and 'role' in message[0]:
            response = self.cache_responses[random.randint(0, len(self.cache_responses)-1 )] + '... Não tem nenhum role marcado\n' \
                       'Digite: domi marcar *\'nome do rolê\'* \n' \
                       '*\'local\'* \n' \
                       '*data*(em formato padrão, ex: 15/10/2020, ano opcional) \n' \
                       '*horário* em horas:minutos(24 horas formato, se não o lembrete não vai funcionar)\n' \
                       '*tempo* em *minutos* para alertar antes e depois(opcional, n inclua caso não queira que seja avisado)\n' \
                       'Ex: domi marcar \'fumar um beckão\' \'na baia\' 26/11 16:20 10\n' \
                       'Note que você não precisa colocar rolê no nome do evento e todo rolê marcado, fica disponível para registro, até 24 horas a partir do horário de início do rolê'

            if len(self.roles) > 0:
                temp_sentence = 'Salve meu meninão, deem uma olhada nos roles ai gurizada:\n'
                temp_at_least_one = False
                
                for r in self.roles:
                    if bot.get_conversation().id == r['conversation']:
                        temp_at_least_one = True
                        temp_sentence += r['infos'] + '\n'

                temp_sentence += '*Qualquer coisa é só chamar, gurizada*'

                if temp_at_least_one:
                    response = temp_sentence
        else:
            response = 'Iiii pia, deu alguma merda, n consegui marca o rolê não...'

        bot.get_message(response)
        time.sleep(1)
        bot.send_message()

    def check_events(self, bot):

        temp_now = datetime.now()

        for r in self.roles:
            time_remaing_second = temp_now - r['date']

            if r['remaind'] > 0:
                temp_remaing_to_reach = int(r['remainder']) * 60
                time_remaing = r['date'] - temp_now

                if time_remaing.days <= 0 and (time_remaing.seconds <= temp_remaing_to_reach and r['remaind'] == 2 or time_remaing.seconds > temp_remaing_to_reach and time_remaing_second.seconds >= temp_remaing_to_reach and r['remaind'] == 1):
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
                    bot.get_message(response)
                    time.sleep(1)
                    bot.send_message()
            elif time_remaing_second.seconds >= self.time_to_delete_role:
                print('DEBUG LOG: Role %s deletado' % r)
                bot.set_conversation(r['conversation'])
                bot.get_message('Rolê id *%s* foi deletado, espero que tenham/estejam curtido/curtindo o bagui, \n*Uma boa pa nóis familia!!!*' % r['id'])
                time.sleep(1)
                bot.send_message()

                del self.roles[r['id']]

                if len(self.roles) != 0:
                    print('DEBUG LOG: Rolês ainda existentes: ', len(self.roles))
                else:
                    print('DEBUG LOG: Nenhum rolê restante')

    def command(self, arg):
        self.enabled = True if arg == 'true' else False
        
    print('DEBUG CORE: Events Bot Initialized...')
