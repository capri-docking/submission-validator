import { useRef, useState } from "react";

interface Props {
  disabled: boolean;
  onFile: (content: string, filename: string) => void;
}

export function FileUpload({ disabled, onFile }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function readFile(file: File) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result;
      if (typeof content === "string") onFile(content, file.name);
    };
    reader.readAsText(file);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) readFile(file);
    e.target.value = "";
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    if (disabled) return;
    const file = e.dataTransfer.files[0];
    if (file) readFile(file);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    if (!disabled) setDragging(true);
  }

  function handleDragLeave() {
    setDragging(false);
  }

  return (
    <div
      onClick={() => !disabled && inputRef.current?.click()}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      className={[
        "border-2 border-dashed rounded-lg px-8 py-10 text-center transition-colors",
        disabled
          ? "border-gray-200 text-gray-300 cursor-not-allowed"
          : dragging
            ? "border-blue-400 bg-blue-50 cursor-copy text-blue-600"
            : "border-gray-300 hover:border-blue-400 hover:bg-gray-50 cursor-pointer text-gray-500",
      ].join(" ")}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdb,.ent,.txt"
        className="hidden"
        disabled={disabled}
        onChange={handleChange}
      />
      <p className="text-sm font-medium">
        {disabled
          ? "Waiting for Python environment..."
          : "Drop a PDB file here, or click to browse"}
      </p>
      <p className="text-xs mt-1 opacity-60">Accepts .pdb, .ent, or plain text PDB files</p>
    </div>
  );
}
