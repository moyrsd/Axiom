import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { Message, MessageListProps } from "@/interface/Interface";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeSanitize from "rehype-sanitize";
import "katex/dist/katex.min.css";
import { useIsClient } from "@/hooks/useIsClient"; 


const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const isClient = useIsClient(); // Use this hook to detect client-side rendering

  // Scroll to bottom when messages change
  useEffect(() => {
    if (isClient && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isClient]);

 
  if (!isClient) {
    return (
      <div className="flex-1 overflow-y-auto px-9 space-y-4 max-h-[calc(110vh-200px)] pb-4 pt-0">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.isUser ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-4 rounded-xl px-6 max-w-3xl break-words text-sm shadow-md 
                ${
                  message.isUser
                    ? "bg-gray-900 text-white"
                    : "bg-gray-900 text-white/80"
                }`}
            >
              <div className="prose prose-invert max-w-full">
                {message.content}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-9 space-y-4 max-h-[calc(110vh-200px)] pb-4 pt-0">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`p-4 rounded-xl px-6 max-w-3xl break-words text-sm shadow-md 
              transition-all duration-500 ease-in-out transform hover:-translate-y-1
              ${
                message.isUser
                  ? "bg-gray-900 text-white"
                  : "bg-gray-900 text-white/80"
              }
              ${isClient ? "animate-fadeInUp" : ""}`}
          >
            <div className="prose prose-invert max-w-full">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeRaw, rehypeSanitize, rehypeKatex]}
                components={{
                  // Headings
                  h1: ({ node, ...props }) => (
                    <h1 className="text-xl font-bold mt-4 mb-2" {...props} />
                  ),
                  h2: ({ node, ...props }) => (
                    <h2 className="text-lg font-bold mt-3 mb-2" {...props} />
                  ),
                  h3: ({ node, ...props }) => (
                    <h3 className="text-md font-bold mt-3 mb-1" {...props} />
                  ),
                  h4: ({ node, ...props }) => (
                    <h4
                      className="text-base font-semibold mt-2 mb-1"
                      {...props}
                    />
                  ),
                  h5: ({ node, ...props }) => (
                    <h5
                      className="text-sm font-semibold mt-2 mb-1"
                      {...props}
                    />
                  ),
                  h6: ({ node, ...props }) => (
                    <h6
                      className="text-xs font-semibold mt-2 mb-1"
                      {...props}
                    />
                  ),

                  // Lists
                  li: ({ node, ordered, ...props }) => (
                    <li className="my-1" {...props} />
                  ),
                  ul: ({ node, ...props }) => (
                    <ul className="pl-6 list-disc my-2" {...props} />
                  ),
                  ol: ({ node, ...props }) => (
                    <ol className="pl-6 list-decimal my-2" {...props} />
                  ),

                  // Block elements
                  p: ({ node, ...props }) => <p className="my-2" {...props} />,
                  blockquote: ({ node, ...props }) => (
                    <blockquote
                      className="border-l-4 border-gray-500 pl-4 py-1 my-3 italic"
                      {...props}
                    />
                  ),

                 // Code rendering
                  code: ({ node, inline, className, children, ...props }) => {
                    const match = /language-(\w+)/.exec(className || "");

                    if (inline) {
                      return (
                        <code
                          className="bg-gray-700 px-1 rounded text-xs"
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    }

                    return (
                      <div className="my-3">
                        <pre className="bg-gray-800 p-3 rounded-md overflow-x-auto text-xs w-full">
                          <code className={className} {...props}>
                            {children}
                          </code>
                        </pre>
                      </div>
                    );
                  },

                  // Tables
                  table: ({ node, ...props }) => (
                    <div className="overflow-x-auto my-3">
                      <table
                        className="min-w-full border-collapse border border-gray-700"
                        {...props}
                      />
                    </div>
                  ),
                  thead: ({ node, ...props }) => (
                    <thead className="bg-gray-800" {...props} />
                  ),
                  tbody: ({ node, ...props }) => (
                    <tbody className="divide-y divide-gray-700" {...props} />
                  ),
                  tr: ({ node, ...props }) => (
                    <tr className="divide-x divide-gray-700" {...props} />
                  ),
                  th: ({ node, ...props }) => (
                    <th
                      className="px-4 py-2 text-left text-xs font-medium uppercase"
                      {...props}
                    />
                  ),
                  td: ({ node, ...props }) => (
                    <td className="px-4 py-2 text-sm" {...props} />
                  ),

                  // Inline elements
                  a: ({ node, ...props }) => (
                    <a className="text-blue-400 hover:underline" {...props} />
                  ),
                  strong: ({ node, ...props }) => (
                    <strong className="font-bold" {...props} />
                  ),
                  em: ({ node, ...props }) => (
                    <em className="italic" {...props} />
                  ),
                  img: ({ node, ...props }) => (
                    <img
                      className="max-w-full h-auto rounded my-2"
                      {...props}
                    />
                  ),
                  hr: ({ node, ...props }) => (
                    <hr className="my-4 border-gray-600" {...props} />
                  ),
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

      {/* Invisible element to scroll to */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
