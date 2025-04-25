import React, { useState } from "react";
import { Message } from "@/interface/Interface";

const PromptBox = ({
  onNewMessage,
  onFocus,
  setIsSubmitting,
}: {
  onNewMessage: (message: Message) => void;
  onFocus?: () => void;
  setIsSubmitting: (status: boolean) => void;
}) => {
  const [query, setQuery] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSubmitting(true);
    onNewMessage({ content: `**Question:**\n${query}`, isUser: true });

    try {
      const response = await fetch(
        `/api/ask?question=${encodeURIComponent(query)}`,
        { method: "POST" }
      );

      if (!response.ok) throw new Error("Request failed");
      const data = await response.json();

      onNewMessage({
        content:
          data.answer,
        isUser: false,
      });
    } catch (error) {
      onNewMessage({ content: "Error getting response.please refresh the page, Upload something  and try again ", isUser: false });
    } finally {
      setIsSubmitting(false);
      setQuery("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-10xl mx-auto">
      <div className="flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={onFocus}
          placeholder="Upload some documents and ask questions"
          className="flex-1 bg-gray-900 text-white p-3 rounded-xl shadow-lg 
          ring-1 ring-blue-500/25 focus:outline-none 
          focus:ring-4 focus:ring-blue-500/40 focus:ring-offset-2 focus:ring-offset-gray-900
          focus:shadow-[0_0_15px_3px_rgba(159,130,246,0.4)]
          transition duration-300"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-5 py-2 rounded-xl shadow-md 
          hover:bg-blue-500 hover:ring-2 hover:ring-blue-400 transition duration-200"
        >
          Ask
        </button>
      </div>
    </form>
  );
};

export default PromptBox;
