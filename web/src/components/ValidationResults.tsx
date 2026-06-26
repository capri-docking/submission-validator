import type { ValidationResult } from "../hooks/usePyodide.ts";

interface Props {
  filename: string;
  result: ValidationResult;
  validating: boolean;
}

function CheckRow({ name, passed }: { name: string; passed: boolean }) {
  return (
    <div className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
      <span className="text-sm text-gray-700">{name}</span>
      <span className="text-base" title={passed ? "Pass" : "Fail"}>
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
  checks: Record<string, boolean>;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
        {label}
      </p>
      <div className="divide-y divide-gray-100">
        {Object.entries(checks).map(([name, passed]) => (
          <CheckRow key={name} name={name} passed={passed} />
        ))}
      </div>
    </div>
  );
}

export function ValidationResults({ filename, result, validating }: Props) {
  const allChecks = [
    ...Object.values(result.tier1),
    ...Object.values(result.tier2),
  ];
  const passed = allChecks.every(Boolean);

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
