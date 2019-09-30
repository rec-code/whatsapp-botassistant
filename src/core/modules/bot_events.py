import time
from datetime import datetime

class BotEvent:
    roles = []
    time_to_delete_role = 1440 * 60 # 3 hours to seconds = 10.800 seconds

    def events(self, message, bot):
        print('Mensagem do rolê: ', message)

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

                response = 'Boa rapaziada, gostei de ver... \n' + \
                           temp_label + \
                           '\nConto com vocês, filhos da puta!!!\n' \
                           'Para saber os roles marcados digite: domi role'

                if temp_year == 0:
                    temp_year = date_now.year

                temp_date = datetime(temp_year, temp_month, temp_day, temp_hour, temp_minute)

                self.roles.append({'id': len(self.roles), 'role': temp_label, 'remainder': temp_remainder, 'date': temp_date, 'remaind': temp_remaind, 'conversation': bot.get_conversation()})

                print(len(self.roles))
            except:
                response = 'Mano..... Tu digitou uma caca tão grande, que nem entendi velho, namoral...'

        elif len(message) == 1 and 'role' in message[0]:
            response = 'Gurizão... Não tem nenhum role marcado\n' \
                       'Digite: domi marcar *\'nome do rolê\'* \n' \
                       '*\'local\'* \n' \
                       '*data*(em formato padrão, ex: 15/10/2020, ano opcional) \n' \
                       '*horário* em horas:minutos(24 horas formato, se não o lembrete não vai funcionar)\n' \
                       '*tempo* em *minutos* para alertar antes e depois(opcional, n inclua caso não queira que seja avisado)\n' \
                       'Ex: domi marcar \'fumar um beckão\' \'na baia\' 26/11 16:20 10\n' \
                       'Note que você não precisa colocar rolê no nome do evento e todo rolê marcado, fica disponível para registro, até 24 horas a partir do horário de início do rolê'

            if len(self.roles) > 0:
                response = 'Salve meu meninão, tem um total de %s rolês, deem uma olhada neles gurizada:\n' % len(self.roles)

                for r in self.roles:
                    response += r['role'] + '\n'

                response += '*Qualquer coisa é só chamar, gurizada*'
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
                if time_remaing.seconds <= temp_remaing_to_reach and r['remaind'] == 2 or time_remaing.seconds > temp_remaing_to_reach and time_remaing_second.seconds >= temp_remaing_to_reach and r['remaind'] == 1:
                    r['remaind'] -= 1

                    if r['remaind'] == 0:
                        print('Avisando que o rolê já começou: ', r['role'])
                        temp_resp = 'Faaaaaaaala rapeize, ta tendo rolê já faz '
                    else:
                        print('Avisando que o rolê vai começar: ', r['role'])
                        temp_resp = 'Faaaaaaaala rapeize, vai te rolê em '

                    temp_label_minutes = ' minutos'

                    if int(r['remainder']) == 1:
                        temp_label_minutes = ' minuto'

                    response = temp_resp + str(r['remainder']) + temp_label_minutes +', saca as infos:\n' + \
                        r['role']

                    bot.set_conversation(r['conversation'].id)
                    bot.get_message(response)
                    time.sleep(1)
                    bot.send_message()
            elif time_remaing_second.seconds >= self.time_to_delete_role:
                print('Role %s deletado' % r)
                bot.set_conversation(r['conversation'].id)
                bot.get_message('Rolê id *%s* foi deletado, espero que tenham/estejam curtido/curtindo o bagui, \n*Uma boa pa nóis familia!!!*' % r['id'])
                time.sleep(1)
                bot.send_message()

                del self.roles[r['id']]

                if len(self.roles) != 0:
                    print('Rolês ainda existentes: ', len(self.roles))
                else:
                    print('Nenhum rolê restante')
