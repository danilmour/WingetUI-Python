# WingetUI-Python

**Windows-only.** Wraps `winget` (Windows Package Manager CLI) via `subprocess.run`. Python code can be edited cross-platform but only works on Windows with `winget` on PATH.

## Structure

- `main.py` — single-file PySimpleGUI app (~200 LOC). No packages or modules.
- `requirements.txt` — lists `PySimpleGUI`.

## Features

| Tab | Functions |
|---|---|
| Pesquisar & Instalar | Search packages, results in a selectable listbox, install selected |
| Instalados | List installed packages in a listbox, uninstall selected |
| Atualizações | Check updates, install single update, upgrade all |
| Exportar/Importar | Export/import package lists via JSON file dialog |

## Run

```sh
pip install -r requirements.txt
python main.py
```

## Commands & config

No build, test, typecheck, or formatter commands. No pre-commit hooks. No `pyproject.toml` or `setup.py`.

### CI

GitHub Actions workflow (`.github/workflows/validate.yml`) runs on push/PR to `main`:
- `python -m py_compile main.py` — syntax check
- `ruff check main.py` — linting

## UI language

Portuguese (labels: "Buscar", "Instalar", "Desinstalar", "Listar", "Atualizações", "Exportar", "Importar").

## Implementation notes

- All winget commands use `subprocess.run(['winget', ...])` with a list of args — no shell is spawned, so shell injection is not possible.
- Tabbed layout via `sg.TabGroup` with 4 tabs. A single `sg.Output` at the bottom captures all `print()` output.
- Winget's tabular output is parsed by detecting column positions from the `---` separator line, then extracting values by position. A `HEADER_MAP` handles Portuguese column headers (e.g. `Nome` → `name`).
- Agreement flags `--accept-source-agreements` and `--accept-package-agreements` are passed to prevent blocking prompts.
- All commands block the GUI until winget completes (no async). 120s timeout per command.
