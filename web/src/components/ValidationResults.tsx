import type { CheckResult, ValidationResult } from "../hooks/usePyodide.ts";

interface Props {
  filename: string;
  result: ValidationResult;
  validating: boolean;
}

function CheckRow({
  name,
  passed,
  message,
}: {
  name: string;
  passed: boolean;
  message: string | null;
}) {
  return (
    <div className="flex items-start justify-between py-2.5 border-b border-gray-100 last:border-0">
      <div className="min-w-0 flex-1">
        <span className="text-sm text-gray-700">{name}</span>
        {!passed && message && (
          <pre className="text-xs text-red-500 mt-1 whitespace-pre-wrap font-mono bg-red-50 rounded p-2 max-h-40 overflow-y-auto">
            {message}
          </pre>
        )}
      </div>
      <span className="text-base shrink-0 ml-4" title={passed ? "Pass" : "Fail"}>
        {passed ? "✅" : "❌"}
      </span>
    </div>
  );
}

function TierSection({
  label,
  checks,
}: {
  label: string;
  checks: Record<string, CheckResult>;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
        {label}
      </p>
      <div className="divide-y divide-gray-100">
        {Object.entries(checks).map(([name, check]) => (
          <CheckRow
            key={name}
            name={name}
            passed={check.passed}
            message={check.message}
          />
        ))}
      </div>
    </div>
  );
}

const OVERVIEW_LABELS: Record<string, string> = {
  "No. models": "Models",
  "No. chains": "Chains",
  "No. residues": "Residues",
  "No. atoms": "Atoms",
  "No. HETATM": "HETATM",
  "Multiple Occ.": "Multiple Occ.",
  "Res. Inserts": "Res. Inserts",
};

function Overview({ data }: { data: Record<string, string> }) {
  const entries = Object.entries(OVERVIEW_LABELS).flatMap(([key, label]) =>
    key in data ? [[label, data[key]] as [string, string]] : []
  );
  if (entries.length === 0) return null;
  return (
    <div className="px-4 py-3 border-b border-gray-100 grid grid-cols-4 gap-x-4 gap-y-2">
      {entries.map(([label, value]) => (
        <div key={label}>
          <p className="text-xs text-gray-400">{label}</p>
          <p className="text-sm font-medium text-gray-700">{value}</p>
        </div>
      ))}
    </div>
  );
}

export function ValidationResults({ filename, result, validating }: Props) {
  const allChecks = [
    ...Object.values(result.tier1),
    ...Object.values(result.tier2),
  ];
  const passed = allChecks.every((c) => c.passed);

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center justify-between">
        <span className="text-sm font-medium text-gray-600 font-mono truncate">
          {filename}
        </span>
        {validating && (
          <span className="text-xs text-blue-500 animate-pulse">
            Validating...
          </span>
        )}
      </div>

      <Overview data={result.overview} />

      <div className="px-4 py-3 space-y-4">
        <TierSection label="Tier 1 — Format & Residues" checks={result.tier1} />
        <TierSection label="Tier 2 — Structure" checks={result.tier2} />
      </div>

      <div
        className={[
          "px-4 py-3 text-sm font-semibold tracking-widest text-center border-t",
          passed
            ? "bg-green-50 text-green-700 border-green-100"
            : "bg-red-50 text-red-700 border-red-100",
        ].join(" ")}
      >
        {passed ? "PASSED" : "FAILED"}
      </div>
    </div>
  );
}
