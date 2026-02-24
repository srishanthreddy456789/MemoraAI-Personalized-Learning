"use client";

import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);

  const sendMessage = async () => {
    alert("SEND BUTTON CLICKED");
    if (!input.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // 🔐 If your endpoint is protected, add:
          // "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          session_id: currentSessionId,
          message: input,
        }),
      });

      const data = await response.json();

      // If backend created new session
      if (!currentSessionId) {
        setCurrentSessionId(data.session_id);
      }

      setMessages((prev) => [
        ...prev,
        { role: "student", content: input },
        { role: "teacher", content: data.reply },
      ]);

      setInput("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleNewChat = () => {
    setCurrentSessionId(null);
    setMessages([]);
  };

  return (
    <div className="h-screen flex bg-[#0e0f14] text-white">
      
      {/* LEFT SIDE — SIDEBAR */}
      <div className="w-72 bg-[#15161c] border-r border-gray-800 flex flex-col">

        {/* Top Section */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-800">
          <span className="text-xl">🧠</span>
          <span className="text-gray-400 cursor-pointer">✕</span>
        </div>

        {/* Middle Section */}
        <div className="p-4 space-y-3 border-b border-gray-800">
          <button
            onClick={handleNewChat}
            className="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded-lg text-sm"
          >
            + New Chat
          </button>

          <div className="bg-[#1e2028] px-3 py-2 rounded-lg text-sm text-gray-400">
            Search chats
          </div>
        </div>

        {/* Bottom Section — Static for now */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          <div className="hover:bg-[#1e2028] p-2 rounded-md cursor-pointer">
            Time Complexity
          </div>
          <div className="hover:bg-[#1e2028] p-2 rounded-md cursor-pointer">
            Recursion Basics
          </div>
        </div>
      </div>

      {/* RIGHT SIDE — MAIN */}
      <div className="flex-1 flex flex-col relative">

        {/* Top Bar */}
        <div className="h-16 flex items-center px-6 border-b border-gray-800 text-lg font-semibold">
          MemoryAI
        </div>

        {/* Chat Area */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {messages.length === 0 ? (
            <div className="text-gray-400">
              Chat messages will appear here...
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.role === "student" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`px-4 py-2 rounded-xl max-w-md ${
                    msg.role === "student"
                      ? "bg-indigo-600"
                      : "bg-[#1e2028]"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Input Section */}
      <div className="absolute bottom-6 left-0 w-full flex justify-center px-6 z-50">
        <div className="bg-[#1e2028] border border-gray-700 rounded-2xl px-6 py-4 flex items-center gap-4 shadow-2xl max-w-3xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
            placeholder="Message MemoryAI..."
            className="flex-1 bg-transparent outline-none text-sm text-white placeholder-gray-500"
          />

          <button
            onClick={sendMessage}
            className="bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-xl text-sm font-medium"
          >
            Send
          </button>
        </div>
      </div>
      </div>
    </div>
  );
}