import os

import PySimpleGUI as Sg

Sg.theme("systemdefault")

layout = [
    [Sg.Text("Instalar Software", font=("Helvetica", 15))],
    [Sg.Button("Instalar Google Chrome"),
     Sg.Button("Instalar Visual Studio Code"),
     Sg.Button("Instalar Adobe Acrobat Reader"),
     Sg.Button("Instalar Virtualbox"),
     Sg.Button("Instalar VLC")],
    [Sg.Text("Instalar Outro Software", font=("Helvetica", 15))],
    [Sg.Input(key="-PACOTE-"), Sg.Button("Instalar")],
    [Sg.Text("Atualizações", font=("Helvetica", 15))],
    [Sg.Button("Procurar Atualizações"), Sg.Button("Instalar Atualizações")],
    [Sg.Text("", key="-MENSAGEM-")]
]

window = Sg.Window("Winget GUI", layout)


def validar_codigo(codigo, sucesso, falha):
    if codigo == 0:
        window["-MENSAGEM-"].update(sucesso)
    else:
        window["-MENSAGEM-"].update(falha)


def install_app(aplicacao):
    retorno = os.system(f"winget install {aplicacao}")
    validar_codigo(retorno, "Instalado com sucesso!", "Ocorreu um erro.")


while True:
    event, values = window.read()
    if event == Sg.WIN_CLOSED:
        break

    if event == "Procurar Atualizações":
        code = os.system("winget upgrade")
        validar_codigo(code, "Não há Atualizações Pendentes.", "Ocorreu um erro.")

    if event == "Instalar Atualizações":
        code = os.system("winget upgrade --all")
        validar_codigo(code, "Atualizações Instaladas com Sucesso!", "Ocorreu um erro.")

    if event == "Instalar Google Chrome":
        install_app("google.chrome")

    if event == "Instalar Visual Studio Code":
        install_app("vscode")

    if event == "Instalar Adobe Acrobat Reader":
        install_app("XPDP273C0XHQH2")

    if event == "Instalar Virtualbox":
        install_app("virtualbox")

    if event == "Instalar VLC":
        install_app("\"VLC media player\"")

    if event == "Instalar":
        install_app(values["-PACOTE-"])

window.close()
