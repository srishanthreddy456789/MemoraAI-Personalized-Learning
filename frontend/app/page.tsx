export default function Home() {
  return (
    <div className="h-screen flex">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white p-4">
        <h2 className="text-xl font-bold mb-4">MemoraAI</h2>
        <button className="w-full bg-gray-800 p-2 rounded">
          + New Chat
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 p-6 overflow-y-auto">
          <div className="mb-4">
            <p className="text-sm text-gray-500">Assistant</p>
            <div className="bg-gray-100 p-3 rounded">
              Hi! I’m your AI teacher 👋
            </div>
          </div>
        </div>

        {/* Input box */}
        <div className="border-t p-4 flex gap-2">
          <input
            className="flex-1 border rounded p-2"
            placeholder="Ask something..."
          />
          <button className="bg-black text-white px-4 rounded">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}