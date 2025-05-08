# Dependencias necessarias
#   pip install winotify

import os
from os.path import isfile
import sys

from winotify import Notifier, Registry, Notification


class NWindows:
    def __init__(self, titulo="", msg="", grupo="Notificação", icone="", executar=""):
        self.grupo = grupo
        self.titulo = titulo
        self.msg = msg
        self.icone = icone
        self.executar = executar

        self.notificar()

    def notificar(self):
        notifier = Notifier(
            Registry(app_id="test", executable=self.executar, script_path=f'"{os.path.abspath(sys.argv[0])}"')
        )

        @notifier.register_callback
        def fn_callback():
            pass

        if self.icone.strip() != "" and not isfile(self.icone):
            self.icone = ""

        notifier.start()
        notification = Notification(
            app_id=self.grupo,
            title=self.titulo,
            msg=self.msg,
            icon=self.icone,
            launch=notifier.callback_to_url(fn_callback)
        )

        notification.show()

'''
# Exemplo de uso
NWindows("Teste", "ola", icone="C:\\Users\\usuario\\Desktop\\Sem título.png", executar="C:\\Program Files\\Notepad++\\notepad++.exe")
'''
