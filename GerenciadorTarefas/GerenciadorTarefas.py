# Dependencias necessarias
#   pip install pywin32

import os

import win32com.client


class Disparador:
    def __init__(self, tipo, intervalor_repeticao=0, usuario='USERNAME'):
        self.tipo = tipo
        self.intervalor_repeticao = intervalor_repeticao
        self.usuario = usuario


class Acao:
    def __init__(self, nome_arquivo, caminho_absoluto="", argumentos=""):
        self.nome_arquivo = nome_arquivo
        self.caminho_absoluto = caminho_absoluto
        self.argumentos = argumentos


class Tarefa:
    def __init__(self, nome, descricao="", ativo=True, disparadores=[], acoes=[]):
        self.nome = nome
        self.descricao = descricao
        self.ativo = ativo

        # Conectar ao agendador (Vista/Server 2008 and above only)
        self.agendador = win32com.client.Dispatch("Schedule.Service")
        self.agendador.Connect(None, None, None, None)

        # Criar tarefa (ou Atualizar quando a tarefa ja existe)
        self.tarefa = self.agendador.NewTask(0)

        self.definir_disparadores(disparadores)
        self.definir_acoes(acoes)
        self.definir_configuracoes()

        # Informacoes sobre a tarefa
        info = self.tarefa.RegistrationInfo
        info.Author = os.environ.get('USERNAME')
        info.Description = self.descricao

        # Registrar a tarefa
        # Criar ou atualizar, manter o mesmo nome. TASK_CREATE_OR_UPDATE = 6, TASK_LOGON_INTERACTIVE_TOKEN = 3
        t_result = self.agendador.GetFolder("\\").RegisterTaskDefinition(self.nome, self.tarefa, 6, "", "", 3)
        t_result.Enabled = self.ativo

    def definir_disparadores(self, disparadores):
        # Criar triggers
        # Quando o usuario fizer logon TASK_TRIGGER_LOGON = 9
        # Quando a tarefa for criada ou alterada TASK_TRIGGER_CREATE_UPDATE = 7
        for disparador in disparadores:
            if isinstance(disparador, Disparador):
                trigger = self.tarefa.Triggers.Create(disparador.tipo)
                if disparador.usuario.strip() == "":
                    trigger.UserId = os.environ.get('USERNAME')  # current user account
                else:
                    trigger.UserId = os.environ.get(disparador.usuario)
                trigger.Repetition.Interval = f'PT{disparador.intervalor_repeticao}M'

    def definir_acoes(self, acoes):
        # Criar Acoes
        # Iniciar um programa TASK_ACTION_EXEC = 0
        for acao in acoes:
            if isinstance(acao, Acao):
                action = self.tarefa.Actions.Create(0)
                action.ID = self.nome
                action.Path = os.path.join(acao.caminho_absoluto, acao.nome_arquivo)
                if acao.caminho_absoluto.strip() != "":
                    action.WorkingDirectory = acao.caminho_absoluto
                if acao.argumentos.strip() != "":
                    action.Arguments = acao.argumentos

    def definir_configuracoes(self):
        # Configuracoes
        settings = self.tarefa.Settings
        settings.Enabled = True
        settings.Hidden = False
        settings.StartWhenAvailable = True
        settings.DisallowStartIfOnBatteries = False
        settings.StopIfGoingOnBatteries = False
        settings.ExecutionTimeLimit = "PT0S"  # Nao interromper se a tarefa for executada por mais de
        settings.RunOnlyIfIdle = False
        settings.IdleSettings.StopOnIdleEnd = False
        settings.IdleSettings.RestartOnIdle = False

    def deletar(self):
        try:
            # Deletar tarefa se a tarefa nao existe gera erro
            self.agendador.GetFolder("\\").DeleteTask(self.nome, 0)
        except:
            pass


'''
# Exemplo de uso
Tarefa("Teste", disparadores=[Disparador(9, 5)], acoes=[Acao('C:\\Users\\usuario\\Desktop\\Novo Texto.txt')])
'''
