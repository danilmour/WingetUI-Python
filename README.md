# Winget GUI Python

Graphical user interface for the Windows Package Manager (`winget`), built with Python and PySimpleGUI.

## Features

- **Pesquisar & Instalar** — Search for packages via `winget search`, pick from a list, install with one click.
- **Instalados** — List all installed packages (`winget list`), select to uninstall.
- **Atualizações** — Check for available updates (`winget upgrade`), install individually or upgrade all.
- **Exportar/Importar** — Export your installed package list to a JSON file (`winget export`) or import from one (`winget import`).

All operations appear in the output panel at the bottom of the window.

## Requirements

- Windows 10 1809+ or Windows 11 (where `winget` is available)
- Python 3.7+
- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)

## Quick start

```sh
pip install -r requirements.txt
python main.py
```

## Implementation

- Single-file Python app (~240 LOC), no packages or modules.
- Every winget command runs via `subprocess.run(['winget', ...])` — no shell, no injection risk.
- Tabbed interface using `sg.TabGroup` with 4 tabs and a shared output area.
- Winget's tabular output is parsed by detecting column boundaries from the `---` separator line, with a header map to handle Portuguese column names (e.g. `Nome` → `name`).
- Agreement flags (`--accept-source-agreements`, `--accept-package-agreements`) are passed automatically to avoid blocking prompts.
- Commands are synchronous — the GUI waits for winget to finish (120s timeout per call).

Created by Daniel Gonçalves.
