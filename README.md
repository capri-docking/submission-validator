# submission-validator

[![ci](https://github.com/capri-docking/submission-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/capri-docking/submission-validator/actions/workflows/ci.yml)

Validate CAPRI (Critical Assessment of PRedicted Interactions) docking submission PDB files.

See [CHECKS.md](CHECKS.md) for the list of validation checks.

## Install

```bash
uv sync --extra dev
```

## Usage

```bash
uv run submission-validator <path-to-pdb-file>
```
