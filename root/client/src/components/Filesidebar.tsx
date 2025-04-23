import { useState } from "react";
import CloudUpload from "@mui/icons-material/CloudUpload";
import MenuIcon from "@mui/icons-material/Menu";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import { FileSidebarProps } from "@/interface/Interface";

const FileSidebar = ({
  onUpload,
  collapsed,
  setCollapsed,
}: FileSidebarProps & { collapsed: boolean; setCollapsed: (val: boolean) => void }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<{ [key: string]: string }>({});

  const handleFileUpload = async (files: File[]) => {
  const formData = new FormData();
  files.forEach((file) => formData.append('files', file));

  // Initial upload state for all files
  files.forEach((file) => {
    setUploadStatus((prev) => ({ ...prev, [file.name]: '⏳ Uploading...' }));
  });

  // Simulate upload delay
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Update to processing state
  files.forEach((file) => {
    setUploadStatus((prev) => ({ ...prev, [file.name]: '⏳ Processing...' }));
  });

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error('Upload failed');
    
    // Final success state
    files.forEach((file) => {
      setUploadStatus((prev) => ({ ...prev, [file.name]: '✅ Processed' }));
    });
    onUpload();
  } catch (error) {
    // Error state
    files.forEach((file) => {
      setUploadStatus((prev) => ({ ...prev, [file.name]: '❌ Failed' }));
    });
  }
};


  return (
    <div
      className={`relative flex flex-col bg-gray-900 text-white h-full shadow-inner transition-all duration-300 ease-in-out rounded-xl ${
        collapsed ? "w-0" : "w-56"
      }`}
    >
      {/* Menu Toggle Button */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className={`absolute top-6 -right-17 z-30 bg-gray-800 hover:bg-gray-700 text-white p-2 rounded-xl shadow-md transition-all duration-300 ease-in-out border-b border-gray-300 ${
          collapsed ? "opacity-80" : "opacity-100"
        }`}
        title={collapsed ? "Open Sidebar" : "Close Sidebar"}
      >
        {collapsed ? <MenuIcon /> : <MenuOpenIcon />}
      </button>

      {/* Sidebar content (hidden when collapsed) */}
      {!collapsed && (
        <>
          <div className="absolute top-7 left-14 text-4xl font-bold text-white z-10 
          opacity-0 animate-fadeInSlow drop-shadow-glow transition-opacity duration-1500">
            <h2 className="text-xxl font-bold">Axiom</h2>
          </div>

          <div className="flex-1 pt-25 overflow-y-auto p-4 space-y-2">
            {files.map((file) => (
              <div
                key={file.name}
                className="flex items-center justify-between p-2 border-b rounded-xl border-gray-700 hover:bg-gray-800 rounded"
              >
                <span
                  className="truncate max-w-xs "
                  title={file.name}  // Shows full name on hover
                >
                  {file.name}
                </span>
                <span className="text-sm ml-2">
                  {uploadStatus[file.name] || "⏳ Uploading..."}
                </span>
              </div>
            ))}
          </div>

          <label className="p-6 border-t  border-gray-500 cursor-pointer hover:bg-gray-800 rounded-xl relative group">
           <input
             type="file"
             accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.png,.jpg,.jpeg"
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
             <span>Upload file</span>
           </div>
           
           {/* Tooltip shown on hover */}
           <div className="absolute left-1 -translate-x- 0.1 bottom-full mb-2 w-max max-w-xs px-3 py-1 text-sm text-white bg-gray-700 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-50 pointer-events-none">
             Accepted: .pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.png,.jpg,.jpeg
           </div>
        </label>
        </>
      )}
    </div>
  );
};

export default FileSidebar;
