import PySimpleGUI as sg


iconDiario = 'images/authentication.ico'
imgAtenção = 'images/atencao.ico'
menu_def = [['&Opções', ['&Cadastro', '&Login', '&Sair']],
            ['&Ajuda', ['&Tema', ['Light', 'Dark', 'Lavanda', 'Azul'], '&Sobre']]]

class Janela():
    """ Classe para representar telas."""

    def __init__(self, tamanho_tela=(), nome_tela='', fonte='', perguntar_saida=False):
        self.area = tamanho_tela
        self.nome = nome_tela
        self.fonte = fonte
        self.saida = perguntar_saida


    def primeira_tela(self):
        """ Primeira tela exibida."""

        layout = [[sg.Menu(menu_def)],
                  [sg.Text("Seja bem-vindo(a) ao diário!", justification='center', size=(400, 1),
                           pad=((0, 0), (100, 50)))],
                  [sg.Image("images/images.png")]]

        return 'primeira_tela', sg.Window("Diario", layout, enable_close_attempted_event=self.saida, size=self.area,
                                          element_justification='center', icon=iconDiario, font=self.fonte)


    def cadastro(self):
        """ Tela para fazer cadastro."""

        frame_layout = [[sg.Text('Nome:', size=(15, 1), pad=((0, 10), (50, 0))),
                         sg.In(pad=((0, 15), (50, 0)), key='-CAD_NOME-')],
                        [sg.Text('Senha:', size=(15, 1), pad=((0, 5), (20, 20))),
                         sg.In(password_char='*', key='-CAD_SENHA-')],
                        [sg.Text('Confirme a senha:', size=(15, 1), pad=((0, 10), (0, 50))),
                         sg.In(pad=((0, 0), (0, 50)), password_char='*', key='-CAD_SENHA_CONF-')]]

        layout = [[sg.Menu(menu_def)],
                  [sg.Frame('Cadastro', frame_layout, pad=((0, 0), (50)))],
                  [sg.Button('Cadastrar', size=(11, 1), )]]

        return 'cadastro', sg.Window('Diário', layout, enable_close_attempted_event=self.saida, size=self.area,
                                     text_justification='right', element_justification='center', icon=iconDiario,
                                     font=self.fonte)


    def login(self):
        """ Tela para fazer login."""

        frame_layout = [[sg.Text('Nome:', size=(7, 1), pad=((0, 10), (50, 0))),
                         sg.In(pad=((0, 15), (50, 0)), key='-LOG_NOME-')],
                        [sg.Text('Senha:', size=(7, 1), pad=((0, 10), (20, 50))),
                         sg.In(pad=((0, 15), (20, 50)), password_char='*', key='-LOG_SENHA-')]]

        layout = [[sg.Menu(menu_def)],
                  [sg.Frame('Login', frame_layout, pad=((0, 0), (50)))],
                  [sg.Button('Entrar', size=(11, 1))]]

        return 'login', sg.Window('Diário', layout, enable_close_attempted_event=self.saida, size=self.area,
                                  text_justification='right', element_justification='center', icon=iconDiario,
                                  font=self.fonte)


    def area_usuario(self, nome=None):
        """ Tela do usuário ao logar."""

        layout = [[sg.Text(f"{str(nome).title()}'s daily")],
                  [sg.Text('_' * 100)],
                  [sg.Text('\n' * 8)],
                  [sg.Text('Msg aleatoria', size=(800, 1), justification='center')],
                  # Aqui vai ter 2 tabs, uma para mensagens de outras pessoas e outra personalizada do usuario
                  [sg.Text('\n' * 8)],
                  [sg.Text('_' * 100)],
                  [sg.Text()],
                  [sg.Button('Escrever', size=(12, 2), pad=((180, 0), (0, 0))),
                   sg.Button('Ler', size=(12, 2), pad=((50, 0), (0, 0))),
                   sg.Button('Voltar', size=(12, 2), pad=((50, 0), (0, 0)))]]

        return 'area_usuario', sg.Window('Diário', layout, size=self.area, icon=iconDiario,
                                         enable_close_attempted_event=self.saida, font=self.fonte)


    def escrever(self):
        frame_layout = [[sg.Text('Titulo:')],
                        [sg.InputText(key='-TITULO-')],
                        [sg.Text()],
                        [sg.Text('Mensagem:')],
                        [sg.Multiline(key='-TEXTO-', default_text='Querido diário...', size=(100, 15))]]

        layout = [[sg.Frame('', frame_layout, pad=((0, 0), (40, 0)))],
                  [sg.Button('Salvar', size=(11, 1), pad=((0, 15), (60, 0))),
                   sg.Button('Voltar', size=(11, 1), pad=((15, 0), (60, 0)))]]

        return 'escrever', sg.Window('Diário', layout, size=self.area, element_justification='center', icon=iconDiario,
                                     enable_close_attempted_event=self.saida, font=self.fonte)


    def ler(self, lista):
        layout = [[sg.Text("N°", pad=((120, 0), (0, 0))),
                   sg.Text("Título", pad=((70, 0), (0, 0))),
                   sg.Text("Data", pad=((160, 0), (0, 0)))],
                  [sg.Listbox(lista, size=(200, 15), key='-BOX-', pad=(100, 0))],
                  [sg.Text('_' * 100)],
                  [sg.Text()],
                  [sg.Text("Digite o número da mensagem desejada:", size=(55, 1),
                           justification='right'), sg.In(size=(5, 1), key='-NUM-')],
                  [sg.Text()],
                  [sg.Button("Visualizar", pad=((270, 0), 0)), sg.Button("Voltar", size=(8, 1), pad=((80, 0), 0))]]

        return 'ler', sg.Window(self.nome, layout, size=self.area, enable_close_attempted_event=self.saida,
                                icon=iconDiario, font=self.fonte)
