from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from os.path import basename, isfile
from smtplib import SMTP
from ssl import create_default_context


class NEmail:
    def __init__(self, mensagem, de, para, senha, usuario="", anexos=[]):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = de
            msg["To"] = para
            msg['Date'] = formatdate(localtime=True)
            msg["Subject"] = mensagem

            if usuario.strip() == "":
                usuario = de

            for f in anexos or []:
                if isfile(f):
                    with open(f, "rb") as fil:
                        part = MIMEApplication(fil.read(), Name=basename(f))
                    # After the file is closed
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                    msg.attach(part)
                else:
                    print(f"Arquivo {f} nao encontrado")

            context = create_default_context()
            with SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context)
                server.login(usuario, senha)
                server.sendmail(de, para, msg.as_string())

        except Exception as e:
            print(e)


'''
# Exemplo de uso
NEmail("ola", "de@email.com.br", "para@email.com.br", "senha1234", anexos=['C:\\Users\\usuario\\Desktop\\Novo Texto.txt'])
'''
