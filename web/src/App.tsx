import { useState } from "react";
import { usePyodide } from "./hooks/usePyodide.ts";
import type { ValidationResult } from "./hooks/usePyodide.ts";
import { FileUpload } from "./components/FileUpload.tsx";
import { ValidationResults } from "./components/ValidationResults.tsx";
import { LoadingSpinner } from "./components/LoadingSpinner.tsx";
import { Navbar } from "./components/Navbar.tsx";

export default function App() {
  const { ready, loading, loadingMessage, error, validate } = usePyodide();
  const [result, setResult] = useState<ValidationResult | null>(null);
  const [filename, setFilename] = useState<string>("");
  const [validating, setValidating] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);

  async function handleFile(content: string, name: string) {
    if (!validate) return;
    setFilename(name);
    setResult(null);
    setValidationError(null);
    setValidating(true);
    try {
      const r = await validate(content);
      setResult(r);
    } catch (err) {
      setValidationError(err instanceof Error ? err.message : String(err));
    } finally {
      setValidating(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 pt-20 px-4 pb-24">
      <Navbar />
      <div className="max-w-xl mx-auto space-y-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-5">
          <div className="space-y-1">
            <h2 className="text-base font-semibold text-gray-800">
              Validate your docking submission
            </h2>
            <p className="text-sm text-gray-500">
              Upload a PDB file to check whether your CAPRI docking submission
              meets the required format and structural criteria. Checks are
              run locally in your browser — no data leaves your machine.
            </p>
          </div>

          {(loading || error) && (
            <div>
              {loading && <LoadingSpinner message={loadingMessage} />}
              {error && (
                <p className="text-sm text-red-600">
                  Failed to load Python environment: {error}
                </p>
              )}
            </div>
          )}

          <FileUpload disabled={!ready} onFile={(c, n) => void handleFile(c, n)} />

          {validationError && (
            <p className="text-sm text-red-600">
              Validation error: {validationError}
            </p>
          )}

          {result && (
            <ValidationResults
              filename={filename}
              result={result}
              validating={validating}
            />
          )}

          {validating && !result && (
            <div className="flex justify-center py-4">
              <LoadingSpinner message="Running validation checks..." />
            </div>
          )}
        </div>
      </div>

      <footer className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-3 px-4">
        <p className="max-w-xl mx-auto text-center text-xs text-gray-400">
          &copy; {new Date().getFullYear()} CAPRI — Critical Assessment of
          Predicted Interactions &middot; built by{" "}
          <a
            href="https://rvhonorato.me"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:text-gray-600"
          >
            Rodrigo V Honorato
          </a>
        </p>
      </footer>
    </div>
  );
}
