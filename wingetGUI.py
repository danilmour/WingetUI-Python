import PySimpleGUI as sg
import subprocess

sg.theme("systemdefault")

layout = [
    [sg.Text("Winget - Interface Gráfica", font=("Helvetica", 20))],
    [sg.Text("Instalar Software", font=("Helvetica", 15))],
    [sg.Button("Instalar Google Chrome"), sg.Button("Instalar Visual Studio Code"), sg.Button("Instalar Adobe Acrobat Reader"), sg.Button("Instalar Virtualbox"), sg.Button("Instalar VLC")],
    [sg.Text("Instalar Outro Software", font=("Helvetica", 15))],
    [sg.Input(key="-PACOTE-"), sg.Button("Instalar")],
    [sg.Text("Atualizações", font=("Helvetica", 15))],
    [sg.Button("Procurar Atualizações"), sg.Button("Instalar Atualizações")],
    [sg.Text("", key="-MENSAGEM-")]
]

window = sg.Window("Winget GUI", layout)


def validarCodigo(codigo, sucesso, falha):
    if codigo == 0:
        window["-MENSAGEM-"].update(sucesso)
    else:
        window["-MENSAGEM-"].update(falha)


def installApp(aplicacao):
    code = subprocess.call(["winget", "install", aplicacao, "--accept-package-agreements"])
    validarCodigo(code, "Instalado com sucesso!", "Ocorreu um erro.")


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "Procurar Atualizações":
        code = subprocess.call(["winget", "upgrade"])

        validarCodigo(code, "Não há Atualizações Pendentes.",
                      "Ocorreu um erro.")

    if event == "Instalar Atualizações":
        code = subprocess.call(["winget", "upgrade", "--all"])

        validarCodigo(code, "Atualizações Instaladas com Sucesso!",
                      "Ocorreu um erro.")

    if event == "Instalar Google Chrome":
        installApp("google.chrome")

    if event == "Instalar Visual Studio Code":
        installApp("vscode")

    if event == "Instalar Adobe Acrobat Reader":
        installApp("XPDP273C0XHQH2")

    if event == "Instalar Virtualbox":
        installApp("virtualbox")

    if event == "Instalar VLC":
        installApp("VLC media player")

    if event == "Instalar":
        installApp(values["-PACOTE-"])

window.close()
