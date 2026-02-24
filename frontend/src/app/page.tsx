"use client";

export default function Home() {
  return (
    <div className="h-screen flex bg-[#0e0f14] text-white">

      {/* LEFT SIDE — SIDEBAR */}
<div className="w-72 bg-[#15161c] border-r border-gray-800 flex flex-col">

  {/* Top Section — Logo + Close Icon */}
  <div className="h-16 flex items-center justify-between px-4 border-b border-gray-800">
    <span className="text-xl">🧠</span>
    <span className="text-gray-400 cursor-pointer">✕</span>
  </div>

  {/* Middle Section — New Chat + Search */}
  <div className="p-4 space-y-3 border-b border-gray-800">
    <button className="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded-lg text-sm">
      + New Chat
    </button>

    <div className="bg-[#1e2028] px-3 py-2 rounded-lg text-sm text-gray-400">
      Search chats
    </div>
  </div>

  {/* Bottom Section — Chat List */}
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

  {/* Top Section */}
  <div className="h-16 flex items-center px-6 border-b border-gray-800 text-lg font-semibold">
    MemoryAI
  </div>

  {/* Middle Chat Area */}
  <div className="flex-1 p-6 overflow-y-auto">
    <div className="text-gray-400">
      Chat messages will appear here...
    </div>
  </div>

  {/* Floating Input */}
  <div className="absolute bottom-6 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6">
    <div className="bg-[#1e2028] border border-gray-700 rounded-2xl px-6 py-4 flex items-center gap-4 shadow-2xl">

      <input
        type="text"
        placeholder="Message MemoryAI..."
        className="flex-1 bg-transparent outline-none text-sm text-white placeholder-gray-500"
      />

      <button className="bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-xl text-sm font-medium">
        Send
      </button>

    </div>
  </div>

</div>
    </div>
  );
}