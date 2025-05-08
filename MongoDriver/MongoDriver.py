# Dependencias necessarias
#   pip install pymongo

import atexit

import pymongo


class MDriver:
    def __new__(cls, servidor, banco, colecao, criar_banco=False, criar_colecao=False):
        instancia = super().__new__(cls)
        instancia.finalizou = False
        instancia.servidor = servidor
        instancia.banco = banco
        instancia.colecao = colecao
        instancia.criar_banco = criar_banco
        instancia.criar_colecao = criar_colecao
        instancia.erro = ""

        instancia.validar_parametros()
        if instancia.erro != "":
            print(f"\033[31m{instancia.erro}\033[m")
            return instancia.erro

        try:
            instancia.obj_servidor = pymongo.MongoClient(
                host=f"mongodb://{servidor}:27017/?uuidRepresentation=csharpLegacy",
                serverSelectionTimeoutMS=10,
                connectTimeoutMS=20000
            )
            print(instancia.obj_servidor.list_database_names())
        except Exception as e:
            instancia.erro = f"Não foi possível se conectar no Servidor '{servidor}' - {str(e)}"
            print(f"\033[31m{instancia.erro}\033[m")
            return instancia.erro

        try:
            if banco not in instancia.obj_servidor.list_database_names() and not criar_banco:
                instancia.erro = f"O Banco '{banco}' não existe"
                print(f"\033[31m{instancia.erro}\033[m")
                return instancia.erro
            instancia.obj_banco = instancia.obj_servidor[banco]
        except Exception as e:
            instancia.erro = f"Não foi possível se conectar ao Banco '{banco}' - {str(e)}"
            print(f"\033[31m{instancia.erro}\033[m")
            return instancia.erro

        try:
            if colecao not in instancia.obj_banco.list_collection_names() and not criar_colecao:
                instancia.erro = f"A collection '{colecao}' não existe"
                print(f"\033[31m{instancia.erro}\033[m")
                return instancia.erro
            instancia.obj_colecao = instancia.obj_banco[colecao]
        except Exception as e:
            instancia.erro = f"Não foi possível se conectar na Colecao '{colecao}' - {str(e)}"
            print(f"\033[31m{instancia.erro}\033[m")
            return instancia.erro

        atexit.register(instancia.desconectar)
        return instancia

    def validar_parametros(self):
        if type(self.servidor) != str:
            self.erro += "Servidor deve ser do tipo string\n"

        if type(self.banco) != str:
            self.erro += "Banco deve ser do tipo string\n"

        if type(self.colecao) != str:
            self.erro += "Colecao deve ser do tipo string\n"

        if self.erro != "":
            return self.erro

        if self.servidor.strip() == "":
            self.erro += "Servidor nao pode ser vazio\n"

        if self.banco.strip() == "":
            self.erro +=  "Banco nao pode ser vazio\n"

        if self.colecao.strip() == "":
            self.erro +=  "Colecao nao pode ser vazia\n"

    def __enter__(self):
        # Ao executar with open, posso colocar qualquer coisa aqui que vai executar antes do codigo dentro do with open
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.desconectar()
        self.finalizou = True

    def desconectar(self):
        if not self.finalizou:
            self.obj_servidor.close()

    def __getattr__(self, nome):
        return getattr(self.obj_colecao, nome)
