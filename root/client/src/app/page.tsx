"use client";
import { useState } from "react";
import FileSidebar from "@/components/Filesidebar";
import PromptBox from "@/components/PromptBox";
import MessageList from "@/components/MessageList";
import { Message } from "@/interface/Interface";
import { useEffect } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [hasFiles, setHasFiles] = useState(true);

  const handleNewMessage = (message: Message) => {
    setMessages((prev) => [...prev, message]);
  };

  useEffect(() => {
    const controller = new AbortController();
    
    fetch('http://localhost:8000/removetempfiles', {
      method: 'POST',
      signal: controller.signal
    })
      .then(response => {
        if (!response.ok) throw new Error('Failed to clear temp files');
        console.log('Temp files cleanup triggered');
      })
      .catch(error => console.error('Cleanup error:', error));

    return () => controller.abort();
  }, []); // Cleans the server request to remove temp files

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100">
      <FileSidebar onUpload={() => setHasFiles(true)} />

      <div className="flex-1 flex flex-col">
        {!hasFiles ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            Upload Files to start chatting
          </div>
        ) : (
          <MessageList messages={messages} />
        )}

        {hasFiles && <PromptBox onNewMessage={handleNewMessage} />}
      </div>
    </div>
  );
}
