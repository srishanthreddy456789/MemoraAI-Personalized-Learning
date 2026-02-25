import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Brain,
  PanelLeftClose,
  PanelLeft,
  Plus,
  Search,
  MessageSquare,
  Send,
  Sun,
  Moon,
  Settings,
  LogOut,
  UserRoundCog,
  UserCircle,
  HelpCircle,
  MoreHorizontal,
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const Index = () => {
  const navigate = useNavigate();

  // ---------------- STATE ----------------
  const [sessions, setSessions] = useState<{ id: string; title: string }[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [dark, setDark] = useState(true);

  // ---------------- AUTH GUARD ----------------
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/login");
  }, []);

  // ---------------- FETCH SESSIONS ----------------
  useEffect(() => {
    const fetchSessions = async () => {
      const token = localStorage.getItem("token");

      const res = await fetch(
        "https://memoraai-personalized-learning-m7td.onrender.com/sessions",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (res.ok) {
        const data = await res.json();
        setSessions(data);
      }
    };

    fetchSessions();
  }, []);

  // ---------------- DARK MODE ----------------
  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  // ---------------- FILTER ----------------
  const filteredChats = sessions.filter((chat) =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // ---------------- SEND MESSAGE ----------------
  const sendMessage = async () => {
    if (!messageInput.trim()) return;

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "https://memoraai-personalized-learning-m7td.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            session_id: currentSessionId,
            message: messageInput,
          }),
        }
      );

      if (response.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
        return;
      }

      const data = await response.json();

      // If new session created
      if (!currentSessionId) {
        setCurrentSessionId(data.session_id);

        // Refresh sessions list
        setSessions((prev) => [
          { id: data.session_id, title: messageInput.slice(0, 30) },
          ...prev,
        ]);
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

  // ---------------- LOAD SESSION ----------------
  const loadSession = async (sessionId: string) => {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch(
        `https://memoraai-personalized-learning-m7td.onrender.com/sessions/${sessionId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) return;

      const data = await res.json();

      setCurrentSessionId(sessionId);
      setActiveChatId(sessionId);
      setMessages(Array.isArray(data.messages) ? data.messages : []);
    } catch (err) {
      console.error("Session load error:", err);
    }
  };

  // ---------------- NEW CHAT ----------------
  const startNewChat = () => {
    setCurrentSessionId(null);
    setActiveChatId(null);
    setMessages([]);
  };

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Sidebar */}
      <aside
        className={`flex-shrink-0 flex flex-col border-r border-border bg-sidebar transition-all duration-300 ${
          sidebarOpen ? "w-[280px]" : "w-0 overflow-hidden"
        }`}
      >
        {/* Top */}
        <div className="flex h-[60px] items-center justify-between border-b border-border px-5">
          <div className="flex items-center gap-2.5">
            <Brain
              className="h-6 w-6 text-primary cursor-pointer"
              onClick={startNewChat}
            />
            <span className="text-sm font-semibold text-foreground">
              MemoryAI
            </span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="rounded-md p-1.5 text-muted-foreground hover:bg-sidebar-accent"
          >
            <PanelLeftClose className="h-[18px] w-[18px]" />
          </button>
        </div>

        {/* Middle */}
        <div className="flex flex-col gap-3 border-b border-border p-4">
          <button
            onClick={startNewChat}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
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
              className="w-full rounded-lg border border-border bg-chat-input py-2 pl-9 pr-3 text-sm"
            />
          </div>
        </div>

        {/* Sessions List */}
        <div className="flex-1 overflow-y-auto p-2">
          {filteredChats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => loadSession(chat.id)}
              className={`flex w-full items-center gap-2.5 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
                activeChatId === chat.id
                  ? "bg-sidebar-accent"
                  : "hover:bg-sidebar-accent/60"
              }`}
            >
              <MessageSquare className="h-4 w-4 opacity-50" />
              <span className="truncate">{chat.title}</span>
            </button>
          ))}
        </div>

        {/* User Section */}
        <div className="border-t border-border p-3">
          <button
            onClick={() => {
              localStorage.removeItem("token");
              navigate("/login");
            }}
            className="flex items-center gap-2 text-sm text-destructive"
          >
            <LogOut className="h-4 w-4" />
            Log Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex flex-1 flex-col">
        <header className="flex h-[60px] items-center border-b border-border px-5">
  {!sidebarOpen && (
    <button
      onClick={() => setSidebarOpen(true)}
      className="mr-4 rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
    >
      <PanelLeft className="h-[18px] w-[18px]" />
    </button>
  )}

  <h1 className="text-base font-semibold text-foreground">
    MemoryAI
  </h1>

  <div className="ml-auto flex items-center gap-1">
    {/* 🌙 Dark Mode Toggle */}
    <button
  onClick={() => setDark(!dark)}
  className="relative rounded-md p-1.5 text-muted-foreground transition-all duration-300 hover:bg-secondary hover:text-foreground"
>
  <div
    className={`transition-transform duration-500 ${
      dark ? "rotate-180 scale-110" : "rotate-0"
    }`}
  >
    {dark ? (
      <Sun className="h-[18px] w-[18px]" />
    ) : (
      <Moon className="h-[18px] w-[18px]" />
    )}
  </div>
</button>
     
    {/* ⚙️ Settings Dropdown */}
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground">
          <Settings className="h-[18px] w-[18px]" />
        </button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-48">
        <div className="px-3 py-2 border-b border-border">
  <p className="text-sm font-medium text-foreground">
    {localStorage.getItem("email") || "user@email.com"}
  </p>
  <p className="text-xs text-muted-foreground">
    Logged in
  </p>
</div>
        <DropdownMenuItem
          className="gap-2 cursor-pointer"
          onClick={startNewChat}
        >
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

        <DropdownMenuItem
          className="gap-2 cursor-pointer text-destructive"
          onClick={() => {
            localStorage.removeItem("token");
            navigate("/login");
          }}
        >
          <LogOut className="h-4 w-4" /> Log Out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
    <div className="flex items-center gap-3 ml-3">
  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-primary text-sm font-semibold">
    {localStorage.getItem("email")?.charAt(0).toUpperCase() || "U"}
  </div>
</div>
  </div>
</header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
                    <Brain className="h-7 w-7 text-primary" />
                  </div>

                  <h2 className="text-2xl font-semibold text-foreground">
                    How can I help you today?
                  </h2>

                  <p className="text-sm text-muted-foreground max-w-md">
                    Ask me anything — I'm here to assist with code, ideas, and more.
                  </p>
                </div>
              </div>
            ) : (
              <div className="mx-auto flex max-w-3xl flex-col px-6 py-6 space-y-4">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.role === "student"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-md rounded-2xl px-4 py-2 text-sm ${
                      msg.role === "student"
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Input */}
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
                disabled={!messageInput.trim()}
                className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-40"
              >
                <Send className="h-4 w-4" />
              </button>
          </div>
        </div>
        </div>
      </div>
    </div>
  );
};

export default Index;