# submission-validator

[![ci](https://github.com/capri-docking/submission-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/capri-docking/submission-validator/actions/workflows/ci.yml)

Validate CAPRI (Critical Assessment of PRedicted Interactions) docking submission PDB files.

See [CHECKS.md](CHECKS.md) for the list of validation checks.

## Install

We commend using [`uv`](https://docs.astral.sh/uv/)

```bash
uv venv .venv --python-3.14
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Usage

```bash
submission-validator <path-to-pdb-file>
```

## Web app (browser)

The validator also runs entirely in the browser via [Pyodide](https://pyodide.org) — no server required.

**Prerequisites:** Node.js ≥ 20 on PATH.

**Start the dev server:**

```bash
source .venv/bin/activate
cd web && npm install && npm run dev
```

`npm run dev` builds a wheel from the local Python package then starts the Vite dev server. Open the URL printed in the terminal.

**Production build:**

```bash
cd web
npm run build   # outputs to web/dist/
```

The `web/dist/` directory is a self-contained static site. The GitHub Actions workflow (`.github/workflows/pages.yml`) deploys it to GitHub Pages automatically on every push to `main`.
