"use client";
import { useState } from "react";
import FileSidebar from "@/components/Filesidebar";
import PromptBox from "@/components/PromptBox";
import MessageList from "@/components/MessageList";
import { Message } from "@/interface/Interface";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [hasFiles, setHasFiles] = useState(true);

  const handleNewMessage = (message: Message) => {
    setMessages((prev) => [...prev, message]);
  };

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
