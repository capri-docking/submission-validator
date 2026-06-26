# submission-validator

[![ci](https://github.com/capri-docking/submission-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/capri-docking/submission-validator/actions/workflows/ci.yml)

Validate CAPRI (Critical Assessment of PRedicted Interactions) docking submission PDB files.

See [CHECKS.md](CHECKS.md) for the list of validation checks.

## Install

We recommend using [`uv`](https://docs.astral.sh/uv/)

```bash
uv venv .venv --python-3.14
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Usage

```bash
submission-validator <path-to-pdb-file>
```

Each check prints a ✅/❌ line. Failing checks also show a short message explaining what went wrong.

### Fix common format issues

Pass `--fix <output>` to apply `pdb_tidy` (from pdb-tools) to the input file, write the cleaned
version to `<output>`, and re-validate automatically:

```bash
submission-validator input.pdb --fix fixed.pdb
```

## Web app (browser)

The validator also runs entirely in the browser via [Pyodide](https://pyodide.org) — no server
required, no data leaves your machine.

**Prerequisites:** Node.js ≥ 20 on PATH.

**Start the dev server:**

```bash
source .venv/bin/activate
cd web && npm install && npm run dev
```

`npm run dev` builds a wheel from the local Python package then starts the Vite dev server. Open
the URL printed in the terminal.

**Production build:**

```bash
cd web
npm run build   # outputs to web/dist/
```

The `web/dist/` directory is a self-contained static site. The GitHub Actions workflow
(`.github/workflows/pages.yml`) deploys it to GitHub Pages automatically on every push to `main`.

The web UI mirrors the CLI: it shows a per-check overview with pass/fail status and error details,
and — when validation fails — offers a **Try to fix** button that runs `pdb_tidy` in-browser and
lets you download the repaired file if the fix succeeds.
