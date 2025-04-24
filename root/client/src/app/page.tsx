"use client";
import { useState } from "react";
import FileSidebar from "@/components/Filesidebar";
import PromptBox from "@/components/PromptBox";
import MessageList from "@/components/MessageList";
import { Message } from "@/interface/Interface";
import { useEffect } from 'react';
import { delete_files } from "./actions/delete_tempfile";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [hasFiles, setHasFiles] = useState(true);
  const [hasAsked, setHasAsked] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const handleNewMessage = (message: Message) => {
    setMessages((prev) => [...prev, message]);
    if (!hasAsked && message.isUser) setHasAsked(true);
  };

  useEffect(() => {
    delete_files()
  }, []); // Cleans the server request to remove temp files

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100 overflow-hidden gap-0.5 px-1 pt-1 pb-1">
      {/* File Sidebar */}
      <FileSidebar
        onUpload={() => setHasFiles(true)}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
      />

      {/* Main content */}
      <div className="flex-1 flex flex-col bg-gray-900 rounded-xl shadow-inner relative overflow-hidden">
        {/* Axiom logo when sidebar is collapsed */}
        {sidebarCollapsed && (
          <div className="absolute top-7 left-20 text-2xl font-bold text-white z-10 
          opacity-0 animate-fadeInSlow drop-shadow-glow transition-opacity duration-1000">
          Axiom
        </div>
        )}

        {/* Logo above prompt box before asking */}
        {!hasAsked && (
          <div className="absolute left-1/2 transform -translate-x-1/2 top-[15%] z-20 transition-all duration-700 ease-in-out flex flex-col items-center text-center opacity-70">
            <img
              src="/logo_icon.png"
              alt="Logo"
              className="h-40 w-40 animate-fadeIn mx-auto"
            />
            <h1 className="mt-1 text-2xl font-bold text-white pb-2">Welcome to Axiom Labs</h1>
          </div>
        )}

        {!hasFiles ? (
          <div className="flex items-center justify-center h-full text-gray-500 text-lg font-medium">
            <div className="bg-gray-00 p-6 rounded-xl shadow-md">
              Upload files to start chatting.
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto px-4 py-2 pb-6 pt-4">
            <div className="bg-gray-800 rounded-2xl p-4 shadow-inner h-full ">
              <MessageList messages={messages} isLoading={isSubmitting}/>
            </div>
          </div>
        )}

        {hasFiles && (
          <div
            className={`absolute left-1/2 transform -translate-x-1/2 z-20 w-full 
              max-w-3xl transition-all duration-350 px-4 ${
                hasAsked
                  ? "top-[95%] -translate-y-full mb-4"
                  : "top-1/2 -translate-y-1/2"
              }`}
          >
            <PromptBox onNewMessage={handleNewMessage} setIsSubmitting={setIsSubmitting} />
          </div>
        )}
      </div>
    </div>
  );
}
