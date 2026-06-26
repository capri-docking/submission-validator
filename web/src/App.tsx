import { useState } from "react";
import { usePyodide } from "./hooks/usePyodide.ts";
import type { ValidationResult } from "./hooks/usePyodide.ts";
import { FileUpload } from "./components/FileUpload.tsx";
import { ValidationResults } from "./components/ValidationResults.tsx";
import { LoadingSpinner } from "./components/LoadingSpinner.tsx";

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
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            CAPRI Submission Validator
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Validate docking PDB submissions in your browser — no server
            required.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-5">
          <div className="min-h-5">
            {loading && <LoadingSpinner message={loadingMessage} />}
            {error && (
              <p className="text-sm text-red-600">
                Failed to load Python environment: {error}
              </p>
            )}
            {ready && (
              <p className="text-sm text-green-600">
                Python environment ready.
              </p>
            )}
          </div>

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

        <p className="text-center text-xs text-gray-400">
          Runs entirely in your browser via{" "}
          <a
            href="https://pyodide.org"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:text-gray-600"
          >
            Pyodide
          </a>
          . No data is uploaded - your results remain confidential.
        </p>
      </div>
    </div>
  );
}
