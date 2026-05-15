import PySimpleGUI as sg
import subprocess

sg.theme('DarkBlue3')

TIMEOUT = 120
AGREEMENTS = ['--accept-source-agreements']

HEADER_MAP = {
    'nome': 'name',
    'versão': 'version', 'versao': 'version',
    'disponível': 'available', 'disponivel': 'available',
    'origem': 'source',
}


def winget(args, flags=None):
    cmd = ['winget'] + (flags or []) + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        out = r.stdout
        if r.stderr:
            out += '\n' + r.stderr
        return out
    except subprocess.TimeoutExpired:
        return 'Erro: Comando excedeu o tempo limite (120s)'
    except FileNotFoundError:
        return 'Erro: winget não encontrado no PATH'
    except Exception as e:
        return f'Erro: {e}'


def parse_table(output):
    lines = output.strip().split('\n')
    if len(lines) < 3:
        return []
    sep = None
    for i, line in enumerate(lines):
        if line.strip() and all(c in ' -' for c in line):
            sep = i
            break
    if sep is None:
        return []
    s_line, h_line = lines[sep], lines[sep - 1]
    starts, ends = [], []
    j = 0
    while j < len(s_line):
        if s_line[j] == '-':
            start = j
            while j < len(s_line) and s_line[j] == '-':
                j += 1
            ends.append(j)
            starts.append(start)
        else:
            j += 1
    if not starts:
        return []
    headers = []
    for s, e in zip(starts, ends):
        h = h_line[s:e].strip().lower()
        headers.append(HEADER_MAP.get(h, h))
    data = []
    for line in lines[sep + 1:]:
        if not line.strip():
            continue
        row = {}
        for i, (s, e) in enumerate(zip(starts, ends)):
            val = line[s:e].strip() if s < len(line) else ''
            if i < len(headers):
                row[headers[i]] = val
        if any(v.strip() for v in row.values()):
            data.append(row)
    return data


def fmt(p):
    return f"{p.get('name', '?')}  ({p.get('id', '?')})"


# Layout
FONT = 'Helvetica'
TAB_FONT = (FONT, 10)
BTN_SZ = (24, 1)

tab1 = [
    [sg.Text('Buscar pacotes para instalar:', font=(FONT, 10))],
    [sg.Input(size=(70, 1), key='-SEARCH-', pad=(0, 5)),
     sg.Button('Buscar', size=(10, 1))],
    [sg.Listbox([], size=(100, 14), key='-SEARCH_RES-', pad=(0, 5))],
    [sg.Button('Instalar Selecionado', key='-INSTALL-', size=BTN_SZ)],
]

tab2 = [
    [sg.Button('Listar Instalados', key='-LIST-', size=(20, 1), pad=(0, 5))],
    [sg.Listbox([], size=(100, 14), key='-INSTALLED_RES-', pad=(0, 5))],
    [sg.Button('Desinstalar Selecionado', key='-UNINSTALL-', size=BTN_SZ)],
]

tab3 = [
    [sg.Button('Verificar Atualizações', key='-UPDATES-', size=(22, 1), pad=(0, 5)),
     sg.Button('Atualizar Tudo', key='-UPGRADE_ALL-', size=(18, 1), pad=(0, 5))],
    [sg.Listbox([], size=(100, 14), key='-UPDATES_RES-', pad=(0, 5))],
    [sg.Button('Instalar Atualização Selecionada', key='-UPGRADE-', size=(30, 1))],
]

tab4 = [
    [sg.Text('', size=(1, 6))],
    [sg.Text('Exporte ou importe listas de pacotes\nem formato JSON.',
             font=(FONT, 11), justification='center')],
    [sg.Text('', size=(1, 3))],
    [sg.Column([
        [sg.Button('Exportar Pacotes', key='-EXPORT-', size=(24, 2)),
         sg.Button('Importar Pacotes', key='-IMPORT-', size=(24, 2))],
    ], justification='center')],
]

layout = [
    [sg.Text('Winget GUI', font=(FONT, 20))],
    [sg.HorizontalSeparator()],
    [sg.TabGroup([
        [sg.Tab('Pesquisar & Instalar', tab1, font=TAB_FONT),
         sg.Tab('Instalados', tab2, font=TAB_FONT),
         sg.Tab('Atualizações', tab3, font=TAB_FONT),
         sg.Tab('Exportar / Importar', tab4, font=TAB_FONT)],
    ])],
    [sg.Output(size=(100, 10), key='-OUT-', pad=(0, 5))],
    [sg.Text('Criado por: Daniel Gonçalves', font=(FONT, 8))],
]

window = sg.Window('Winget GUI', layout, size=(880, 680), resizable=True, finalize=True)
window['-SEARCH-'].bind('<Return>', '_ENTER')

search_pkgs = []
installed_pkgs = []
updates_pkgs = []

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # Search
    if event in ('Buscar', '-SEARCH-_ENTER'):
        q = values['-SEARCH-'].strip()
        if not q:
            print('Digite um termo para buscar.')
            continue
        print(f'Buscando "{q}"...')
        out = winget(['search', q])
        search_pkgs = parse_table(out)
        if not search_pkgs:
            print(out)
        else:
            window['-SEARCH_RES-'].update([fmt(p) for p in search_pkgs])
            print(f'Encontrados {len(search_pkgs)} pacote(s).')

    # Install
    elif event == '-INSTALL-':
        sel = values['-SEARCH_RES-']
        if not sel:
            print('Selecione um pacote na lista.')
            continue
        display_list = [fmt(p) for p in search_pkgs]
        if sel[0] not in display_list:
            print('Pacote não encontrado na lista. Faça uma nova busca.')
            continue
        idx = display_list.index(sel[0])
        pid = search_pkgs[idx].get('id', '')
        print(f'Instalando {pid}...')
        out = winget(['install', pid, '--accept-package-agreements'], AGREEMENTS)
        print(out)

    # List installed
    elif event == '-LIST-':
        print('Listando pacotes instalados...')
        out = winget(['list'])
        installed_pkgs = parse_table(out)
        if not installed_pkgs:
            print(out)
        else:
            window['-INSTALLED_RES-'].update([fmt(p) for p in installed_pkgs])
            print(f'Encontrados {len(installed_pkgs)} pacote(s) instalados.')

    # Uninstall
    elif event == '-UNINSTALL-':
        sel = values['-INSTALLED_RES-']
        if not sel:
            print('Selecione um pacote na lista.')
            continue
        display_list = [fmt(p) for p in installed_pkgs]
        if sel[0] not in display_list:
            print('Pacote não encontrado. Liste os instalados novamente.')
            continue
        idx = display_list.index(sel[0])
        pid = installed_pkgs[idx].get('id', '')
        print(f'Desinstalando {pid}...')
        out = winget(['uninstall', pid], AGREEMENTS)
        print(out)

    # Check updates
    elif event == '-UPDATES-':
        print('Verificando atualizações...')
        out = winget(['upgrade'])
        updates_pkgs = parse_table(out)
        if not updates_pkgs:
            print(out)
        else:
            window['-UPDATES_RES-'].update([fmt(p) for p in updates_pkgs])
            print(f'Encontradas {len(updates_pkgs)} atualização(ões).')

    # Upgrade single
    elif event == '-UPGRADE-':
        sel = values['-UPDATES_RES-']
        if not sel:
            print('Selecione uma atualização na lista.')
            continue
        display_list = [fmt(p) for p in updates_pkgs]
        if sel[0] not in display_list:
            print('Atualização não encontrada. Verifique novamente.')
            continue
        idx = display_list.index(sel[0])
        pid = updates_pkgs[idx].get('id', '')
        print(f'Atualizando {pid}...')
        out = winget(['upgrade', pid, '--accept-package-agreements'], AGREEMENTS)
        print(out)

    # Upgrade all
    elif event == '-UPGRADE_ALL-':
        print('Atualizando todos os pacotes...')
        out = winget(['upgrade', '--all', '--accept-package-agreements'], AGREEMENTS)
        print(out)

    # Export
    elif event == '-EXPORT-':
        path = sg.popup_get_file('Salvar exportação como', save_as=True,
                                  file_types=(('JSON', '*.json'),))
        if path:
            print(f'Exportando para {path}...')
            out = winget(['export', '-o', path], AGREEMENTS)
            print(out)

    # Import
    elif event == '-IMPORT-':
        path = sg.popup_get_file('Selecionar arquivo de importação',
                                  file_types=(('JSON', '*.json'),))
        if path:
            print(f'Importando de {path}...')
            out = winget(['import', '-i', path], AGREEMENTS)
            print(out)

window.close()
