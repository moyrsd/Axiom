import React, { useState } from "react";
import { Message } from "@/interface/Interface";

const PromptBox = ({
  onNewMessage,
}: {
  onNewMessage: (message: Message) => void;
}) => {
  const [query, setQuery] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isSubmitting) return;

    setIsSubmitting(true);
    onNewMessage({ content: `**Question:**\n${query}`, isUser: true });

    try {
      const response = await fetch(
        `/api/ask?question=${encodeURIComponent(query)}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) throw new Error("Request failed");
      const data = await response.json();

      onNewMessage({
        content: data.answer || "No answer found in documents",
        isUser: false,
      });
    } catch (error) {
      onNewMessage({
        content: "Error getting response",
        isUser: false,
      });
    } finally {
      setIsSubmitting(false);
      setQuery("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 ">
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about your PDF..."
          className="flex-1 bg-gray-800 text-white p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isSubmitting}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Sending..." : "Ask"}
        </button>
      </div>
    </form>
  );
};

export default PromptBox;
