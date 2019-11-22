from core.bot_modules_core import BotModulesCore 

class BotHelp(BotModulesCore):
    def __init__(self, name):
        super(BotHelp, self).__init__(name)

    bot_name = 'Ônikka'

    help_list = [
        'Olá, me chamo *' + bot_name + '*, sou uma assistente virtual para o _WhatsApp_.\n',
        'Essa é a lista de comandos disponíveis para mim:\n\~',
        '*_Digite_*: *Domika* e as opções abaixo ou o que você quiser, caso queira apenas trocar uma ideia:\n',
        '*_Digite_*: *marcar* ou *role* *\'nome do role\'* *\'local do rolê\'*(o nome e local do rolê devem ser entre aspas simples, ou vai bugar total) *data*(divido com a barra(/), ano opcional caso seja o ano atual e.g: 16/11 = 16/11/2019) *horário*(e.g: 4:20, formato em 24 horas) *tempo para alerta*(em minutos, caso queira ser lembrado antes e depois do horário)\n',
        '*_Digite_*: *intera* *\'nome da intera\'* \'*preço da _G_*(em decimais caso quebrado, separado por um *.*(ponto)\' *data*(divido com a barra(/), ano opcional caso seja o ano atual e.g: 16/11 = 16/11/2019) *horário*(e.g: 4:20, formato em 24 horas)\n',
        '*_Digite_*: *aprender* ou *ensinar* *\'PERGUNTA?\'* *\'resposta\'* sem aspas e com *\'?\'*, por favor, para me ensinar algo\n\~',
        '*_Digite_*: *noticias* (opcional *br* ou *brasil* para filtrar apenas do Brasil) para ficar por dentro de tudo\n',
        '*_Digite_*: *tecnologia* para saber o que há de novo no ramo das tech tech!!\n',
        '*_Digite_*: *wiki* ou *wikipedia* para consultar algum artigo na famosa!!\n',
        '*_Digite_*: *google* ou *imagens* para pesquisar no Google Pesquisas ou Imagens!!\n',
        '*_Alerta_*: Caso queira que retorne mais de uma imagem, adicione o parâmetro *-2*(o substitua o 2 pelo número de imagens que deseja retornar. Máximo 10) junto do comando!!\n\~',
        '*_Alerta_*: Domika também atende pelo nome *_domi_*\n',
        #'Alerta: *Ônikka* também atende por outros nomes além de *Oni*, como *Domi*, *Onik*, *Onika*, *Onikk* e *Onikka* \n',
        #'*_Alerta_*: Há também uma outra robô(com base em Watson) disponível, chamada *\'onitson\'*, mas ela apenas troca uma ideia\n',
        #'*_Alerta_*: Da mesma forma que a Oni, ela também atende pelos mesmos nomes, apenas acrescentando _tson_ no final e.g: *domitson*, *onikkatson*'
        #'Digite: *\'cala a boca\'* ou *\'obrigado\'* que eu paro de encher o saco',
    ]