import PySimpleGUI as sg
import sqlite3


FONTE = 'timenewroman 13'
iconDiario = 'images/authentication.ico'
imgAtenção = 'images/atencao.ico'

def existe_banco(arquivo):
    """Verifica se existe o arquivo .db"""

    try:
        a = open(arquivo, "r")
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criar_banco(arquivo):
    """Cria banco de dados"""

    banco, cursor = db_con(arquivo)

    cursor.execute("CREATE TABLE usuarios ("
                   "'id' INTEGER NOT NULL UNIQUE,"
                   "'nickname'	TEXT NOT NULL UNIQUE,"
                   "'senha'TEXT NOT NULL,"
                   "PRIMARY KEY('id' AUTOINCREMENT));" #adicionar um campo para sexo
    )

    cursor.execute("CREATE TABLE depoimentos ("
                   "'id_user' INTEGER NOT NULL,"
                   "'titulo'TEXT NOT NULL UNIQUE,"
                   "'texto' TEXT NOT NULL,"
                   "'data' TEXT NOT NULL,"
                   "FOREIGN KEY('id_user') REFERENCES 'usuarios'('id'));"
    )

    cursor.close()
    banco.close()


def db_con(db):
    """Conexão com banco de dados"""

    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    return banco, cursor


def salvar_msg(values, db, id):
    """
    Salva as mensagens no banco de dados.
    :param values: dicionario de valores do PySimpleGUI
    :type values: (dict)
    :param db: caminho do banco de dados
    :type : (str)
    :param id: id do usuário
    :type id: (int)
    """
    titulo = str(values['-TITULO-']).title()
    msg = str(values['-TEXTO-']).capitalize()
    if titulo == '' or msg == '':
        sg.popup("Falta preencher os campos", font=FONTE, title='AVISO', icon=imgAtenção)
    else:
        banco, cursor = db_con(db)
        try:
            cursor.execute(f"INSERT INTO depoimentos VALUES ('{id}', '{titulo}', '{msg}', strftime('%d/%m/%Y'))")
        except Exception as e:
            sg.popup(f"erro:\n[{e}]", font=FONTE, title='AVISO', icon=imgAtenção)
            return False
        else:
            banco.commit()
            sg.popup("mensagem salva!", font=FONTE, title='AVISO', icon=imgAtenção)
            return True
        finally:
            cursor.close()
            banco.close()


def cadastrar(values, db):
    """
    Cadastra o usuário no banco de dados.
    :param values: dicionario de valores do PySimpleGUI
    :type values: (dict)
    :param db: caminho do banco de dados
    :type : (str)
    """

    if values['-CAD_NOME-'] == '' or values['-CAD_SENHA-'] == '' or values['-CAD_SENHA_CONF-'] == '':
        sg.popup_ok('Preencha os campos!', font=FONTE, title='AVISO',
                    icon=imgAtenção)
    elif len(values['-CAD_SENHA-']) < 6:
        sg.popup_ok('A senha precisa ter 6 caracteres ou mais!', font=FONTE, title='AVISO', icon=imgAtenção)
    elif values['-CAD_SENHA-'] != values['-CAD_SENHA_CONF-']:
        sg.popup_ok('As senhas não são iguais!', font=FONTE, title='AVISO', icon=imgAtenção)
    elif len(values['-CAD_NOME-']) < 5:
        sg.popup_ok('O nome de usuário não pode ter menos de que 5 caracteres!', font=FONTE, title='AVISO',
                    icon=imgAtenção)
    else:
        try:
            banco, cursor = db_con(db)
        except sqlite3.OperationalError:
            sg.popup_ok("Ocorreu um erro inseperado!\nReinicie o programa, se o problema percistir\nreinicie o pc.",
                        font=FONTE, title='AVISO', icon=imgAtenção)
        except Exception as e:
            sg.popup_ok(f'Erro ao conectar com o banco de dados!\n{e}', font=FONTE, title='AVISO',
                        icon=imgAtenção)
        else:
            try:
                cursor.execute(
                    f"INSERT INTO usuarios ('nickname', 'senha') VALUES ('{values['-CAD_NOME-']}', '{values['-CAD_SENHA-']}');")
            except sqlite3.IntegrityError:
                sg.popup_ok("O nome de usuário já existe!", font=FONTE, title='AVISO', icon=imgAtenção)
            else:
                banco.commit()
                sg.popup_ok(f"Usuário {values['-CAD_NOME-']} foi cadastrado!", font=FONTE, title='AVISO',
                            icon=imgAtenção)
        finally:
            banco.close()


def login(values, db):
    """
    Realiza o login do usuário.
    :param values: dicionario de valores do PySimpleGUI
    :type values: (dict)
    :param db: caminho do banco de dados
    :type : (str)
    """

    if values['-LOG_NOME-'] == '' or values['-LOG_SENHA-'] == '':
        sg.popup_ok('Esta operação não permite os campos vazios!', font=FONTE, title='AVISO', icon=imgAtenção)
        return False, None, None
    else:
        banco, cursor = db_con(db)
        try:
            cursor.execute(f"SELECT * FROM usuarios WHERE nickname = '{values['-LOG_NOME-']}' AND senha = '{values['-LOG_SENHA-']}'")
        except Exception as e:
            sg.popup_ok(f'Erro ao conectar com o banco de dados!\n{e}', font=FONTE, title='AVISO', icon=imgAtenção)
            return False, None, None
        else:
            resp = cursor.fetchall()[0]
            if resp:
                id = resp[0]
                nome = resp[1]
                return True, id, nome
            else:
                sg.popup_ok('Usuário e/ou senha incorreto(s)!', font=FONTE, title='AVISO', icon=imgAtenção)
                return False, None, None
        finally:
            banco.close()


def saida(fonte, icon):
    """
    Popup de saida.
    :param fonte: tipo e/ou tamanho da fonte.
    :type fonte: (str int)
    :param icon: icone no title bar.
    :type icon: (str)
    """
    resp = sg.popup_yes_no("Deseja realmente sair?", title='Sair', text_color='orange', font=fonte, icon=icon)
    if resp == 'Yes':
        return True
    else:
        return False


def ler(db, id):
    """
    Consulta titulo e data dos depoimentos do usuário.
    :param db: caminho do banco de dados
    :type : (str)
    :param id: id do usuário
    :type id: (int)
    :return: 1. listagem dos titulos e data de cada depoimento formatado e com um 'id'
             2. titulos e datas consultados diretos do banco de dados
    """

    banco, cursor = db_con(db)
    try:
        cursor.execute(f"SELECT titulo, data FROM depoimentos WHERE id_user = '{id}'")
    except Exception as e:
        banco.close()
        sg.popup(f"erro {e}", font=FONTE, title='AVISO', icon=imgAtenção)
    else:
        titulos = cursor.fetchall()

        listagem = []

        for k, v in enumerate(titulos):
            listagem.append(f"{k + 1:^13}| {str(v[0]).capitalize():<50}| {v[1]:<30}")
    return listagem, titulos


def visualizar(values, db, titulos):
    """
    Visualiza a mensagem selecionada.
    :param values: dicionario de valores do PySimpleGUI
    :type values: (dict)
    :param db: caminho do banco de dados
    :type db: (str)
    :param titulos: titulos e datas consultados diretos do banco de dados
    :type titulos: (list)
    """
    banco, cursor = db_con(db)
    if not str(values['-NUM-']).isnumeric():
        sg.popup("Insira um valor válido!!", font=FONTE, title='AVISO', icon=imgAtenção)
    elif int(values['-NUM-']) - 1 >= len(titulos) or int(values['-NUM-']) - 1 < 0:
        sg.popup("Não exite mensagem com este indice!", font=FONTE, title='AVISO', icon=imgAtenção)
    else:
        escolha = int(values['-NUM-']) - 1
        cursor.execute(f"SELECT titulo, texto FROM depoimentos WHERE titulo = '{titulos[escolha][0]}'")
        result = cursor.fetchall()[0]
        sg.Print(f"\t\t\t{str(result[0]).title()}", "_" * 80, f"\n\t{str(result[1]).capitalize()}",
                 font='arial 11')
