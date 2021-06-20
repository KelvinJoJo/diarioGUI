import PySimpleGUI as sg

import back
import tela


DB = "diario_banco.db"
FONTE = 'timenewroman 13'

diario = tela.Janela((800, 600), 'Diário', FONTE, perguntar_saida=True)

def muda_tema(pagina, tema):
    """ Muda as cores do programa."""

    if pagina == 'primeira_tela':
        sg.theme(tema)
        t, w = diario.primeira_tela()
    elif pagina == 'cadastro':
        sg.theme(tema)
        t, w = diario.cadastro()
    elif pagina == 'login':
        sg.theme(tema)
        t, w = diario.login()
    return t, w


if not back.existe_banco(DB):
    back.criar_banco(DB)

sg.theme('tan')

tela, window = diario.primeira_tela()

while True:
    event, values = window.read()

    # Fechar programa
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == "Sair" or event == sg.WIN_CLOSED) and back.saida(FONTE, icon='images/authentication.ico'):
        break

    # Sobre o programa
    elif event == 'Sobre':
        sg.popup('Com este programa você poderá fazer um cadastro para '
                 'poder logar na sua conta e escrever algo sobre seu '
                 'dia e poderá também ver as suas anotações.', font=FONTE)

    # Tela de cadastro
    elif event == 'Cadastro':
        window.close()
        tela, window = diario.cadastro()

    # Tela de login
    elif event == 'Login':
        window.close()
        tela, window = diario.login()

    # Tela onde escreve mensagem
    elif event == 'Escrever':
        window.close()
        tela, window = diario.escrever()

    # Cadastrar o usuário no banco de dados
    elif event == 'Cadastrar':
        back.cadastrar(values, DB)

    # Logar em uma conta
    elif event == 'Entrar':
       existe, id_user, nome = back.login(values, DB)
       if existe:
           window.close()
           tela, window = diario.area_usuario(nome)

    # Salvar mensagem no banco de dados
    elif event == 'Salvar':
        salvou = back.salvar_msg(values, DB, id_user)
        if salvou:
            window.find_element('-TITULO-').Update('')
            window.find_element('-TEXTO-').Update('')

    # Voltar pra área do usuário
    elif event == 'Voltar' and tela == 'escrever' or event == "Voltar" and tela == "ler":
        window.close()
        tela, window = diario.area_usuario(nome)

    # Voltar pra tela principal
    elif event == 'Voltar' and tela == 'area_usuario':
        window.close()
        tela, window = diario.primeira_tela()
        id = nome = None

    # Botão ler da área do usuário
    elif event == 'Ler':
        lista, titulos = back.ler(DB, id_user)
        window.close()
        tela, window = diario.ler(lista)

    # Botão visualizar da tela ler
    elif event == "Visualizar":
        back.visualizar(values, DB, titulos)
        window.find_element('-NUM-').Update('')

    # Trocar tema das janelas
    elif event == 'Dark':
        if sg.theme() == 'Dark':
            pass
        else:
            window.close()
            tela, window = muda_tema(tela, 'dark')
    elif event == 'Light':
        if sg.theme() == 'Tan':
            pass
        else:
            window.close()
            tela, window = muda_tema(tela, 'Tan')
    elif event == 'Lavanda':
        if sg.theme() == 'LightPurple':
            pass
        else:
            window.close()
            tela, window = muda_tema(tela, 'LightPurple')
    elif event == 'Azul':
        if sg.theme() == 'Python':
            pass
        else:
            window.close()
            tela, window = muda_tema(tela, 'Python')

window.close()
