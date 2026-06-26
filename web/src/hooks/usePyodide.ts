import { useState, useEffect } from "react";

interface PyodideFS {
  mkdir: (path: string) => void;
  writeFile: (path: string, data: string) => void;
}

interface PyCallable {
  (arg: string): string;
}

interface PyGlobals {
  get: (name: string) => PyCallable | undefined;
}

interface PyodideInstance {
  runPythonAsync: (code: string) => Promise<unknown>;
  loadPackage: (name: string | string[]) => Promise<void>;
  globals: PyGlobals;
  FS: PyodideFS;
}

export interface ValidationResult {
  tier1: Record<string, boolean>;
  tier2: Record<string, boolean>;
  overview: Record<string, string>;
}

export interface UsePyodideReturn {
  ready: boolean;
  loading: boolean;
  loadingMessage: string;
  error: string | null;
  validate: ((pdbContent: string) => Promise<ValidationResult>) | null;
}

const PYODIDE_VERSION = "0.27.0";
const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

const SETUP_CODE = `
import json
from pathlib import Path
from submission_validator.validator import run_tier1_checks, run_tier2_checks
from submission_validator.overview import get_overview

def validate(pdb_content):
    path = Path("/tmp/upload.pdb")
    path.write_text(pdb_content)
    t1 = run_tier1_checks(path)
    t2 = run_tier2_checks(path)
    overview = get_overview(path)
    return json.dumps({"tier1": t1, "tier2": t2, "overview": overview})
`;

export function usePyodide(): UsePyodideReturn {
  const [ready, setReady] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loadingMessage, setLoadingMessage] = useState(
    "Loading Python environment..."
  );
  const [error, setError] = useState<string | null>(null);
  const [pyodide, setPyodide] = useState<PyodideInstance | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function init() {
      try {
        setLoadingMessage("Loading Python environment...");

        const { loadPyodide } = (await import(
          /* @vite-ignore */
          `${PYODIDE_CDN}pyodide.mjs`
        )) as {
          loadPyodide: (opts: {
            indexURL: string;
          }) => Promise<PyodideInstance>;
        };

        const py = await loadPyodide({ indexURL: PYODIDE_CDN });
        if (cancelled) return;

        setLoadingMessage("Loading numpy...");
        await py.loadPackage(["numpy", "micropip"]);
        if (cancelled) return;

        setLoadingMessage("Installing packages...");
        const base = import.meta.env.BASE_URL;
        const manifest = await fetch(`${base}wheels/manifest.json`).then(
          (r) => r.json() as Promise<{ wheel: string }>
        );
        const wheelUrl = new URL(
          `${base}wheels/${manifest.wheel}`,
          window.location.href
        ).href;

        await py.runPythonAsync(`
          import micropip
          await micropip.install("pdb-tools")
          await micropip.install("${wheelUrl}")
        `);
        if (cancelled) return;

        setLoadingMessage("Initializing validator...");
        await py.runPythonAsync(SETUP_CODE);
        if (cancelled) return;

        console.log("Pyodide ready");
        setPyodide(py);
        setReady(true);
        setLoading(false);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : String(err));
          setLoading(false);
        }
      }
    }

    void init();
    return () => {
      cancelled = true;
    };
  }, []);

  const validate = pyodide
    ? async (pdbContent: string): Promise<ValidationResult> => {
        const pyValidate = pyodide.globals.get("validate");
        if (!pyValidate) throw new Error("validate function not available");
        const resultJson = pyValidate(pdbContent);
        return JSON.parse(resultJson) as ValidationResult;
      }
    : null;

  return { ready, loading, loadingMessage, error, validate };
}
