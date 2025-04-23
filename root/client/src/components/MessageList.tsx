import React from "react";
import ReactMarkdown from "react-markdown";
import { Message, MessageListProps } from "@/interface/Interface";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  return (
    <div className="flex-1 overflow-y-auto px-9 space-y-4 max-h-[calc(110vh-150px)]">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`p-4 rounded-xl px-6 max-w-3xl break-words text-sm shadow-md transition-all duration-300 ease-in-out ${
              message.isUser
                ? "bg-gray-900 text-white"
                : "bg-gray-900 text-white/80"
            }`}
          >
            <div className="prose prose-invert max-w-full">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                components={{
                  h1: ({ node, ...props }) => (
                    <h1 className="text-lg font-bold mb-2" {...props} />
                  ),
                  li: ({ node, ...props }) => (
                    <li className="my-1" {...props} />
                  )
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
        </div>
      ))}

      {/* Loading indicator */}
      {isLoading && (
        <div className="flex justify-start">
          <div className="p-4 rounded-xl max-w-3xl text-sm bg-gray-900 text-white shadow-md flex items-center gap-1">
            <span className="text-gray-300">Searching documents</span>
            <span className="animate-bounce">.</span>
            <span className="animate-bounce delay-150">.</span>
            <span className="animate-bounce delay-300">.</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList;
