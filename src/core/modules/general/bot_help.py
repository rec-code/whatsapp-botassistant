from core.bot_modules_core import BotModulesCore 

class BotHelp(BotModulesCore):
    def __init__(self, name):
        super(BotHelp, self).__init__(name)

    bot_name = 'Ônikka'

    def get_help(self, module):
        if module == '':
            return [
                'Olá, me chamo *' + self.bot_name + '*, sou uma assistente virtual para o _WhatsApp_.\n',
                'Essa é a lista de comandos disponíveis para mim:\n\\~',
                '*_Digite_*: Todo comando deve ter *Domika* junto, ou ela não irá _escutar_:\n',

                self.events_help[0],
                self.supply_help[0],
                self.learn_help[0],
                self.news_help[0],
                self.wiki_help[0],
                self.google_help[0],
                self.media_help[0],

                '*_Digite_*: Caso queira mais informações sobre o módulo, acrescente *ajuda* ou *help* no final para mais detalhe e.g: _domi media ajuda_\n',
                '*_Alerta_*: Domika também atende pelo nome *_domi_*\n',
                '*_Alerta_*: Não necessariamente precisa escrever algum comando em específico, pode apenas perguntar qualquer coisa e trocar uma ideia com ela.\n'
                #'Alerta: *Ônikka* também atende por outros nomes além de *Oni*, como *Domi*, *Onik*, *Onika*, *Onikk* e *Onikka* \n',
                #'*_Alerta_*: Há também uma outra robô(com base em Watson) disponível, chamada *\'onitson\'*, mas ela apenas troca uma ideia\n',
                #'*_Alerta_*: Da mesma forma que a Oni, ela também atende pelos mesmos nomes, apenas acrescentando _tson_ no final e.g: *domitson*, *onikkatson*'
                #'Digite: *\'cala a boca\'* ou *\'obrigado\'* que eu paro de encher o saco',
            ]
        else:
            for h in self.available_helps:
                if h['label'] == module.lower():
                    temp = h['helps']
                    temp.insert(0, 'Lista de comandos para o módulo *%s*:\n' % h['label'].capitalize())
                    return temp

        return None

    events_help = [
        '*_Digite_*: *marcar* ou *role* *\'nome do role\'* *\'local do rolê\'*(o nome e local do rolê devem ser entre aspas simples, ou vai bugar total) *data*(divido com a barra(/), ano opcional caso seja o ano atual e.g: 16/11 = 16/11/2019) *horário*(e.g: 4:20, formato em 24 horas) *tempo para alerta*(em minutos, caso queira ser lembrado antes e depois do horário)\n',
    ]

    supply_help = [
        '*_Digite_*: *intera* *\'nome da intera\'* \'*preço da _G_*(em decimais caso quebrado, separado por um *.*(ponto)\' *data*(divido com a barra(/), ano opcional caso seja o ano atual e.g: 16/11 = 16/11/2019) *horário*(e.g: 4:20, formato em 24 horas)\n',

    ]

    learn_help = [
        '*_Digite_*: *aprender* ou *ensinar* *\'PERGUNTA?\'* *\'resposta\'* sem aspas e com *\'?\'*, por favor, para me ensinar algo\n\\~',

    ]

    news_help = [
        '*_Digite_*: *noticias* (opcional *br* ou *brasil* para filtrar apenas do Brasil) para ficar por dentro de tudo\n',
        '*_Digite_*: *tecnologia* para saber as notícias de tecnologias!!\n',

    ]

    wiki_help = [
        '*_Digite_*: *wiki* ou *wikipedia* para consultar algum artigo na famosa!!\n',

    ]

    google_help = [
        '*_Digite_*: *google* ou *imagens* para pesquisar no Google Pesquisas ou Imagens!!\n',
        '*_Alerta_*: Caso queira que retorne mais de uma imagem ou especificar a quantidade de resultado no Google, adicione o parâmetro *-2*(o substitua o 2 pelo número de imagens que deseja retornar. Máximo 10) junto do comando!!\n\\~',

    ]

    media_help = [
        '*_Digite_*: *youtube*, *spotify*, *twitter* ou outra rede social, para pesquisar uma musica, video ou perfil em alguma rede social'
    ]

    available_helps = [
        {
            'label': 'evento',
            'helps': events_help
        },
        {
            'label': 'intera',
            'helps': supply_help
        },
        {
            'label': 'aprender',
            'helps': learn_help
        },
        {
            'label': 'noticia',
            'helps': news_help
        },
        {
            'label': 'wikipedia',
            'helps': wiki_help
        },
        {
            'label': 'google',
            'helps': google_help
        },
        {
            'label': 'media',
            'helps': media_help
        }]