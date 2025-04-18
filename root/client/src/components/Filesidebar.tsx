import { useState } from "react";
import CloudUpload from "@mui/icons-material/CloudUpload";
import { FileSidebarProps } from "@/interface/Interface";

const FileSidebar = ({ onUpload }: FileSidebarProps) => {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<{ [key: string]: string }>(
    {}
  );

  const handleFileUpload = async (files: File[]) => {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");
      const result = await response.json();
      setUploadStatus((prev) => ({
        ...prev,
        [files[0].name]: "✅ Uploaded",
      }));
      onUpload(); // Trigger parent callback
    } catch (error) {
      setUploadStatus((prev) => ({
        ...prev,
        [files[0].name]: "❌ Failed",
      }));
    }
  };

  return (
    <div className="w-64 bg-gray-900 text-white h-screen flex flex-col">
      <div className="p-4 border-b border-gray-700 justify-center">
        <h2 className="text-xl font-bold">Axiom</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {files.map((file) => (
          <div
            key={file.name}
            className="flex items-center justify-between p-2 hover:bg-gray-800 rounded"
          >
            <span className="truncate">{file.name}</span>
            <span className="text-sm ml-2">
              {uploadStatus[file.name] || "⏳ Uploading..."}
            </span>
          </div>
        ))}
      </div>

      <label className="p-4 border-t border-gray-700 cursor-pointer hover:bg-gray-800">
        <input
          type="file"
          multiple
          className="hidden"
          onChange={(e) => {
            if (e.target.files) {
              const newFiles = Array.from(e.target.files);
              setFiles((prev) => [...newFiles, ...prev]);
              handleFileUpload(newFiles);
            }
          }}
        />
        <div className="flex items-center gap-2">
          <CloudUpload />
          <span>Upload PDFs</span>
        </div>
      </label>
    </div>
  );
};

export default FileSidebar;
