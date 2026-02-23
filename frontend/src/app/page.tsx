"use client";

export default function Home() {
  return (
    <div className="h-screen flex bg-[#1b1a1a] text-gray-200">

      {/* Sidebar */}
      <aside className="w-[250px] bg-[#111010] border-r border-gray-800 flex flex-col">
        
        {/* Logo */}
        <div className="pl-10 pr-6 py-6 border-b border-gray-800">
          <h1 className="text-2xl font-bold text-indigo-400 tracking-tight">
            🧠 MemoraAI
          </h1>
        </div>

        {/* New Chat Button */}
        <div className="px-6 py-5">
          <button className="w-full bg-indigo-600 hover:bg-indigo-700 transition-all duration-200 py-4 rounded-2xl text-lg font-semibold shadow-md">
            + New Chat
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-1 px-5 space-y-3 overflow-y-auto text-lg">
          
          {/* Active Chat */}
          <div className="px-5 py-4 rounded-2xl bg-[#252323] cursor-pointer">
            Time Complexity
          </div>

          {/* Hover Effect Chat */}
          <div className="px-5 py-4 rounded-2xl cursor-pointer transition-all duration-200 hover:bg-indigo-600/20 hover:text-indigo-400">
            Recursion Basics
          </div>

          <div className="px-5 py-4 rounded-2xl cursor-pointer transition-all duration-200 hover:bg-indigo-600/20 hover:text-indigo-400">
            Dynamic Programming
          </div>

        </div>

        {/* Footer */}
        <div className="text-base text-gray-500 text-center py-5 border-t border-gray-800">
          Free • Local • Private
        </div>
      </aside>


      {/* Main */}
      <main className="flex-1 flex flex-col">

        {/* Header */}
        <header className="border-b border-gray-800 px-10 py-6">
          <h2 className="text-2xl font-semibold text-gray-300">
            AI Teacher
          </h2>
        </header>

        {/* Center Welcome */}
        <div className="flex-1 flex items-center justify-center px-6">
          <div className="text-center max-w-3xl space-y-6">
            <h3 className="text-3xl font-semibold text-indigo-400">
              Hi! I’m your personal AI teacher 👋
            </h3>
            <p className="text-lg text-gray-400 leading-relaxed">
              Ask me anything — I’ll adapt to your learning level.
            </p>
          </div>
        </div>

        {/* Bigger Input Bar */}
       <div className="border-t border-gray-800 px-6 py-6">
  <div className="w-full">
    <div className="flex items-center bg-[#252323] border border-gray-700 rounded-3xl px-8 h-[45px]">
      
      <input
        className="w-[85%] flex-1 bg-transparent outline-none text-2xl placeholder-gray-400 h-full"
        placeholder="Message MemoraAI..."
      />

      <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-10 h-[40px] rounded-2xl text-xl font-semibold ml-10">
        Send
      </button>

    </div>
  </div>
</div>

      </main>

    </div>
  );
}