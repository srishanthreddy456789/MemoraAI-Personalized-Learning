import { useState, useEffect } from "react";
import { Brain, PanelLeftClose, PanelLeft, Plus, Search, MessageSquare, Send, Sun, Moon, Settings, LogOut, UserRoundCog, UserCircle, HelpCircle, MoreHorizontal } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

const chatHistory = [
  { id: 1, title: "How to build a SaaS landing page" },
  { id: 2, title: "React performance optimization tips" },
  { id: 3, title: "Database schema design patterns" },
  { id: 4, title: "Tailwind CSS advanced techniques" },
  { id: 5, title: "TypeScript generics explained" },
  { id: 6, title: "API authentication best practices" },
  { id: 7, title: "CI/CD pipeline setup guide" },
  { id: 8, title: "Microservices architecture overview" },
  { id: 9, title: "GraphQL vs REST comparison" },
  { id: 10, title: "Docker containerization basics" },
  { id: 11, title: "Cloud deployment strategies" },
  { id: 12, title: "State management in React" },
];

const Index = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [activeChatId, setActiveChatId] = useState<number | null>(null);
  const [dark, setDark] = useState(true);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const filteredChats = chatHistory.filter((chat) =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  );
const [messages, setMessages] = useState<any[]>([]);
const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
const sendMessage = async () => {
  if (!messageInput.trim()) return;

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Add Authorization here if needed
      },
      body: JSON.stringify({
        session_id: currentSessionId,
        message: messageInput,
      }),
    });

    const data = await response.json();

    if (!currentSessionId) {
      setCurrentSessionId(data.session_id);
    }

    setMessages((prev) => [
      ...prev,
      { role: "student", content: messageInput },
      { role: "teacher", content: data.reply },
    ]);

    setMessageInput("");
  } catch (error) {
    console.error("Send error:", error);
  }
};

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Sidebar */}
      <aside
        className={`flex-shrink-0 flex flex-col border-r border-border bg-sidebar transition-all duration-300 ${
          sidebarOpen ? "w-[280px]" : "w-0 overflow-hidden"
        }`}
      >
        {/* Sidebar Top */}
        <div className="flex h-[60px] items-center justify-between border-b border-border px-5">
          <div className="flex items-center gap-2.5">
            <Brain className="h-6 w-6 text-primary cursor-pointer" onClick={() => window.location.reload()} />
            <span className="text-sm font-semibold text-foreground">MemoryAI</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-sidebar-accent hover:text-foreground"
          >
            <PanelLeftClose className="h-[18px] w-[18px]" />
          </button>
        </div>

        {/* Sidebar Middle */}
        <div className="flex flex-col gap-3 border-b border-border p-4">
          <button className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">
            <Plus className="h-4 w-4" />
            New Chat
          </button>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search chats"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-border bg-chat-input py-2 pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary/50 focus:outline-none focus:ring-1 focus:ring-primary/30 transition-colors"
            />
          </div>
        </div>

        {/* Sidebar Bottom - Chat List */}
        <div className="flex-1 overflow-y-auto p-2">
          <div className="flex flex-col gap-0.5">
            {filteredChats.map((chat) => (
              <button
                key={chat.id}
                onClick={() => setActiveChatId(chat.id)}
                className={`flex w-full items-center gap-2.5 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
                  activeChatId === chat.id
                    ? "bg-sidebar-accent text-foreground"
                    : "text-sidebar-foreground hover:bg-sidebar-accent/60 hover:text-foreground"
                }`}
              >
                <MessageSquare className="h-4 w-4 flex-shrink-0 opacity-50" />
                <span className="truncate">{chat.title}</span>
              </button>
            ))}
          </div>
        </div>

        {/* User Section */}
        <div className="border-t border-border p-3">
          <div className="flex items-center gap-3 rounded-lg px-3 py-2.5 transition-colors hover:bg-sidebar-accent cursor-pointer">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-primary text-sm font-semibold">
              J
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">John Doe</p>
              <p className="text-xs text-muted-foreground truncate">john@example.com</p>
            </div>
            <MoreHorizontal className="h-4 w-4 text-muted-foreground flex-shrink-0" />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Top Header */}
        <header className="flex h-[60px] items-center border-b border-border px-5">
          {!sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(true)}
              className="mr-4 rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
            >
              <PanelLeft className="h-[18px] w-[18px]" />
            </button>
          )}
          <h1 className="text-base font-semibold text-foreground">MemoryAI</h1>
          <div className="ml-auto flex items-center gap-1">
            <button
              onClick={() => setDark(!dark)}
              className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
            >
              {dark ? <Sun className="h-[18px] w-[18px]" /> : <Moon className="h-[18px] w-[18px]" />}
            </button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground">
                  <Settings className="h-[18px] w-[18px]" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem className="gap-2 cursor-pointer">
                  <Plus className="h-4 w-4" /> New Chat
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="gap-2 cursor-pointer">
                  <UserCircle className="h-4 w-4" /> Account Details
                </DropdownMenuItem>
                <DropdownMenuItem className="gap-2 cursor-pointer">
                  <UserRoundCog className="h-4 w-4" /> Switch Account
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="gap-2 cursor-pointer">
                  <HelpCircle className="h-4 w-4" /> Help
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="gap-2 cursor-pointer text-destructive">
                  <LogOut className="h-4 w-4" /> Log Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Middle Chat Area */}
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto flex max-w-3xl flex-col px-6 py-6 space-y-4">
            {messages.length === 0 ? (
              <>
                <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
                  <Brain className="h-7 w-7 text-primary" />
                </div>
                <h2 className="text-2xl font-semibold text-foreground">
                  How can I help you today?
                </h2>
                <p className="text-sm text-muted-foreground">
                  Ask me anything — I'm here to assist with code, ideas, and more.
                </p>
              </>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.role === "student" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-md rounded-2xl px-4 py-2 text-sm ${
                      msg.role === "student"
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary text-foreground"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Bottom Floating Input */}
        <div className="px-6 pb-6 pt-2">
          <div className="mx-auto max-w-3xl">
            <div className="flex items-end gap-3 rounded-2xl border border-chat-input-border bg-chat-input p-3 shadow-lg shadow-[hsl(var(--chat-float-shadow))]">
              <textarea
                rows={1}
                placeholder="Message MemoryAI..."
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                onInput={(e) => {
                  const target = e.target as HTMLTextAreaElement;
                  target.style.height = "auto";
                  target.style.height = Math.min(target.scrollHeight, 160) + "px";
                }}
                className="flex-1 resize-none bg-transparent py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
              />
              <button
                onClick={sendMessage}
                className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-40"
                disabled={!messageInput.trim()}
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
            <p className="mt-2 text-center text-xs text-muted-foreground/60">
              MemoryAI can make mistakes. Consider checking important info.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
