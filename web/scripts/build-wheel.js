// Builds a wheel from the Python package and writes a manifest.json so the
// browser app can resolve the versioned filename at runtime.
import { execSync } from "node:child_process";
import { readdirSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import { resolve, join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(__dirname, "../..");
const wheelsDir = resolve(__dirname, "../public/wheels");

try {
  rmSync(wheelsDir, { recursive: true });
} catch {
  // doesn't exist yet
}
mkdirSync(wheelsDir, { recursive: true });

console.log("Building submission-validator wheel...");
execSync(`uv build --wheel --out-dir "${wheelsDir}"`, {
  cwd: rootDir,
  stdio: "inherit",
});

const wheels = readdirSync(wheelsDir).filter((f) => f.endsWith(".whl"));
if (wheels.length === 0) throw new Error("uv build produced no .whl file");

writeFileSync(
  join(wheelsDir, "manifest.json"),
  JSON.stringify({ wheel: wheels[0] }, null, 2) + "\n"
);

console.log(`Wheel ready: ${wheels[0]}`);
