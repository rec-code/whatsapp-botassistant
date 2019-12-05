from core.bot_modules_core import BotModulesCore 

class BotHelp(BotModulesCore):
    def __init__(self, name, bot):
        super(BotHelp, self).__init__(name, bot)

    def get_help(self, module):
        if module == '':
            return [
                'Olá, me chamo *' + self.my_name + '*, sou uma assistente virtual para o _WhatsApp_.\n',
                'Essa é a lista de comandos disponíveis para mim:\n\\~',
                '*_Digite_*: Todo comando deve ter *Domika* junto, ou ela não irá _escutar_:\n',

                self.events_help[0],
                self.supply_help[0],
                self.learn_help[0],
                self.news_help[0],
                self.wiki_help[0],
                self.google_help[0],
                self.media_help[0],
                self.game_help[0],
                self.mes_help[0],
                
                '*_Digite_*: Caso queira mais informações sobre o módulo, acrescente *<ajuda>* ou *<help>* no final para mais detalhe e.g: _domi media ajuda_\n',
                '*_Dica_*: Domika também atende pelo nome *_domi_*\n',
                '*_Dica_*: Não necessariamente precisa escrever algum comando em específico, pode apenas perguntar qualquer coisa e trocar uma ideia com ela(Não garantido sentido no que ela dizer).\n'
                #'Alerta: *Ônikka* também atende por outros nomes além de *Oni*, como *Domi*, *Onik*, *Onika*, *Onikk* e *Onikka* \n',
                #'*_Alerta_*: Há também uma outra robô(com base em Watson) disponível, chamada *\'onitson\'*, mas ela apenas troca uma ideia\n',
                #'*_Alerta_*: Da mesma forma que a Oni, ela também atende pelos mesmos nomes, apenas acrescentando _tson_ no final e.g: *domitson*, *onikkatson*'
                #'Digite: *\'cala a boca\'* ou *\'obrigado\'* que eu paro de encher o saco',
            ]
        else:
            for h in self.available_helps:
                if module.lower() in h['label']:
                    temp = h['helps']
                    temp.insert(0, 'Lista de comandos para o módulo *%s*:\n' % h['label'].capitalize())
                    return temp

        return None

    events_help = [
        '*_Digite_*: *marcar* ou *role* *<\'nome do role\'>* *<\'local do rolê\'>*(o nome e local do rolê devem ser entre aspas simples, ou vai bugar total) *<data>*(divido com a barra(/), ano opcional caso seja o ano atual e.g: 16/11 = 16/11/2019) *<horário>*(e.g: 4:20, formato em 24 horas) *<tempo para alerta>*(em minutos, caso queira ser lembrado antes e depois do horário)\n',
        '*_Exemplo_*: domi marcar \'Churasquin top\' \'na casa do falet\' 25/12 16:20 15'
    ]

    supply_help = [
        '*_Digite_*: *intera* *\'nome da intera\'* \'*<preço da _grama_>*(em decimais caso quebrado, separado por um *.*(ponto)\' *<data>*(divido com a barra(/), ano opcional caso seja o ano atual e.g: 16/11 = 16/11/2019) *<horário>*(e.g: 4:20, formato em 24 horas)\n',
        '*_Exemplo_*: domi intera \'flores de galeano\' \'1.2\' 25/12 16:20'
    ]

    learn_help = [
        '*_Digite_*: *aprender* ou *ensinar* *<\'pergunta*?*\'>* *<\'resposta\'>* sem aspas e com *\'?\'*, por favor, para me ensinar algo\n\\~',
        '*_Exemplo_*: domi ensinar Qual a substância mais ingerida no mundo e sofre repressão e proibição por causa de nada? A famosa maconha, pae'
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
        '*_Dica_*: Caso queira que retorne mais de uma imagem ou especificar a quantidade de resultado no Google, adicione o parâmetro *<-2>*(o substitua o 2 pelo número de imagens que deseja retornar. Máximo 10) junto do comando!!\n\\~',

    ]

    media_help = [
        '*_Digite_*: *youtube*, *spotify*, *twitter* ou outra rede social, para pesquisar uma musica, video ou perfil em alguma rede social'
    ]

    game_help = [
        '*_Digite_*: *jogo*, *game* ou *veia* junto do parâmetro --(seu nome caso não tenha iniciado o game ou a a casa q irá jogar(de 1 a 9))\n'
        '*_Exemplo_*: domi jogo --Rochelle(caso ninguém ou tenha alguém esperando, esse é o comando para selecionar um lado) ou domi jogo --5 para jogar na casa _5_'
    ]

    mes_help = [
        '*_Digite_*: *mensagem* ou *message* <seu nome ou _anon_ para ser anônimo> --Grupo ou Conversa --Quem quer mencionar --Assunto --Mensagem\n'
        '*_Exemplo_*: domi message --anon --DomiDev --geral --Oi --Te amo'
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
        },
        {
            'label': 'jogo',
            'helps': game_help
        },
        {
            'label': 'trombeta',
            'helps': mes_help
        }
        ]