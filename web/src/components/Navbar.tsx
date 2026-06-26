const LINKS = [
  { label: "CAPRI", href: "https://www.ebi.ac.uk/pdbe/complex-pred/capri/" },
  { label: "GitHub", href: "https://github.com/capri-docking/submission-validator" },
];

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-300 px-4 py-3 z-10">
      <div className="max-w-xl mx-auto flex items-center justify-between">
        <span className="text-sm font-semibold text-gray-800">
          CAPRI Submission Validator
        </span>
        <div className="flex items-center gap-4">
          {LINKS.map(({ label, href }) => (
            <a
              key={href}
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-gray-500 hover:text-gray-900 transition-colors"
            >
              {label}
            </a>
          ))}
        </div>
      </div>
    </nav>
  );
}
