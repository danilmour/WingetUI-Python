import PySimpleGUI as sg
import os

sg.theme('systemdefault')

# Define the layout of the GUI
layout = [
    [sg.Text('Winget GUI', font=('Helvetica', 20))],
    [sg.Text('_'*60)],

    [sg.Text('Procurar por Pacotes')],
    [sg.Input(size=(30), key='-PROCURAR-'), sg.Button('Procurar')],
    [sg.Output(size=(60, 5), key='-RESULTADO_PESQUISA-')],

    [sg.Text('Instalar Pacote')],
    [sg.Input(size=(30), key='-INSTALAR-'), sg.Button('Instalar')],
    [sg.Output(size=(60, 5), key='-ESTADO_DA_INSTALACAO-')],

    [sg.Text('Desinstalar Pacote')],
    [sg.Input(size=(30), key='-DESINSTALAR-'), sg.Button('Desinstalar')],
    [sg.Output(size=(60, 5), key='-ESTADO_DA_DESINSTALACAO-')],

    [sg.Text('Listar Pacotes Instalados'), sg.Button('Listar')],
    [sg.Output(size=(60, 5), key='-LISTA_DE_PACOTES-')],

    [sg.Text('Criado por: Daniel Gonçalves', font=('Helvetica', 5))]
]

# Create the window
window = sg.Window('Winget GUI', layout)


def instalar_pacote(pacote):
    cmd = f'winget install {pacote}'
    res = os.popen(cmd).read()
    return res


def procurar_pacote(pacote):
    cmd = f'winget search {pacote}'
    res = os.popen(cmd).read()
    return res


def desinstalar_pacote(pacote):
    cmd = f'winget uninstall {pacote}'
    res = os.popen(cmd).read()
    return res


def listar_pacotes():
    cmd = f'winget list'
    res = os.popen(cmd).read()
    return res


# Event loop to process events and interact with the GUI
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    elif event == 'Procurar':
        pacote = values['-PROCURAR-']
        out = procurar_pacote(pacote)
        window['-RESULTADO_PESQUISA-'].update(out)

    elif event == 'Instalar':
        pacote = values['-INSTALAR-']
        out = instalar_pacote(pacote)
        window['-ESTADO_DA_INSTALACAO-'].update(out)

    elif event == 'Desinstalar':
        pacote = values['-DESINSTALAR-']
        out = desinstalar_pacote(pacote)
        window['-ESTADO_DA_DESINSTALACAO-'].update(out)

    elif event == 'Listar':
        out = listar_pacotes()
        window['-LISTA_DE_PACOTES-'].update(out)

# Close the window
window.close()
