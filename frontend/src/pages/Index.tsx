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

// ✅ FIXED: Import API_BASE from centralized config instead of hardcoded localhost
import { API_BASE } from "@/lib/api";

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

    if (!token) {
      navigate("/login", { replace: true });
      return;
    }

    // ✅ FIXED: Use API_BASE env variable instead of hardcoded localhost
    fetch(`${API_BASE}/health`)
      .catch(() => {
        localStorage.removeItem("token");
        navigate("/login", { replace: true });
      });

  }, [navigate]);

  // ---------------- FETCH SESSIONS ----------------
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const token = localStorage.getItem("token");

        // ✅ FIXED: Use API_BASE env variable instead of hardcoded localhost
        const res = await fetch(`${API_BASE}/sessions`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error("Session fetch failed");

        const data = await res.json();
        setSessions(data);

      } catch (err) {
        console.error("Session error:", err);
        localStorage.removeItem("token");
        navigate("/login");
      }
    };

    fetchSessions();
  }, [navigate]);

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

      // ✅ FIXED: Use API_BASE env variable instead of hardcoded localhost
      const response = await fetch(
        `${API_BASE}/chat`,
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

    } catch (err) {
      console.error("Chat error:", err);
    }
  };

  // ---------------- LOGOUT ----------------
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    navigate("/login");
  };

  // ---------------- NEW CHAT ----------------
  const handleNewChat = () => {
    setCurrentSessionId(null);
    setMessages([]);
    setActiveChatId(null);
    setMessageInput("");
  };

  // ---------------- SELECT SESSION ----------------
  const handleSelectSession = (sessionId: string) => {
    setActiveChatId(sessionId);
    setCurrentSessionId(sessionId);
    setMessages([]);
  };

  const userEmail = localStorage.getItem("email") || "User";

  return (
    <div className={`h-screen flex overflow-hidden ${dark ? "bg-zinc-950 text-white" : "bg-white text-black"}`}>
      {/* Sidebar */}
      {sidebarOpen && (
        <div className={`w-64 flex flex-col border-r ${dark ? "bg-zinc-900 border-zinc-800" : "bg-gray-50 border-gray-200"}`}>
          {/* Sidebar Header */}
          <div className="flex items-center justify-between p-4 border-b border-zinc-800">
            <div className="flex items-center gap-2">
              <Brain size={20} className="text-purple-400" />
              <span className="font-semibold text-sm">MemoraAI</span>
            </div>
            <button onClick={() => setSidebarOpen(false)} className="text-zinc-400 hover:text-white transition">
              <PanelLeftClose size={16} />
            </button>
          </div>

          {/* New Chat Button */}
          <div className="p-3">
            <button
              onClick={handleNewChat}
              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium transition"
            >
              <Plus size={16} />
              New Chat
            </button>
          </div>

          {/* Search */}
          <div className="px-3 pb-3">
            <div className="flex items-center gap-2 px-3 py-2 bg-zinc-800 rounded-lg">
              <Search size={14} className="text-zinc-400" />
              <input
                type="text"
                placeholder="Search chats..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-transparent text-sm text-white placeholder-zinc-400 outline-none w-full"
              />
            </div>
          </div>

          {/* Sessions List */}
          <div className="flex-1 overflow-y-auto px-2 space-y-1">
            {filteredChats.length === 0 ? (
              <p className="text-xs text-zinc-500 text-center py-4">No sessions yet</p>
            ) : (
              filteredChats.map((chat) => (
                <button
                  key={chat.id}
                  onClick={() => handleSelectSession(chat.id)}
                  className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-left transition ${
                    activeChatId === chat.id
                      ? "bg-zinc-700 text-white"
                      : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
                  }`}
                >
                  <MessageSquare size={14} />
                  <span className="truncate">{chat.title || "Untitled Chat"}</span>
                </button>
              ))
            )}
          </div>

          {/* Footer */}
          <div className="p-3 border-t border-zinc-800">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-zinc-800 transition text-left">
                  <UserCircle size={20} className="text-zinc-400 flex-shrink-0" />
                  <span className="text-sm text-zinc-300 truncate flex-1">{userEmail}</span>
                  <MoreHorizontal size={14} className="text-zinc-500" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent side="top" className="w-48 bg-zinc-800 border-zinc-700">
                <DropdownMenuItem className="text-zinc-300 hover:text-white focus:bg-zinc-700">
                  <UserRoundCog size={14} className="mr-2" />
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem className="text-zinc-300 hover:text-white focus:bg-zinc-700">
                  <Settings size={14} className="mr-2" />
                  Settings
                </DropdownMenuItem>
                <DropdownMenuItem className="text-zinc-300 hover:text-white focus:bg-zinc-700">
                  <HelpCircle size={14} className="mr-2" />
                  Help
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-zinc-700" />
                <DropdownMenuItem
                  onClick={handleLogout}
                  className="text-red-400 hover:text-red-300 focus:bg-zinc-700 cursor-pointer"
                >
                  <LogOut size={14} className="mr-2" />
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <div className={`flex items-center justify-between px-4 py-3 border-b ${dark ? "border-zinc-800" : "border-gray-200"}`}>
          {!sidebarOpen && (
            <button onClick={() => setSidebarOpen(true)} className="text-zinc-400 hover:text-white transition mr-3">
              <PanelLeft size={18} />
            </button>
          )}
          <div className="flex items-center gap-2">
            <Brain size={20} className="text-purple-400" />
            <span className="font-semibold">MemoraAI</span>
          </div>
          <button
            onClick={() => setDark(!dark)}
            className="text-zinc-400 hover:text-white transition"
          >
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center space-y-4">
              <Brain size={48} className="text-purple-400 opacity-60" />
              <div>
                <h2 className="text-2xl font-semibold text-zinc-300">Welcome to MemoraAI</h2>
                <p className="text-zinc-500 mt-1 text-sm">Your personalized AI tutor. Ask me anything to start learning.</p>
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === "student" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-2xl px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                    msg.role === "student"
                      ? "bg-purple-600 text-white"
                      : dark
                      ? "bg-zinc-800 text-zinc-100"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Message Input */}
        <div className={`p-4 border-t ${dark ? "border-zinc-800" : "border-gray-200"}`}>
          <div className={`flex items-end gap-3 rounded-2xl border px-4 py-3 ${dark ? "bg-zinc-900 border-zinc-700" : "bg-gray-50 border-gray-300"}`}>
            <textarea
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
              placeholder="Ask MemoraAI anything..."
              rows={1}
              className="flex-1 bg-transparent text-sm resize-none outline-none placeholder-zinc-500"
            />
            <button
              onClick={sendMessage}
              disabled={!messageInput.trim()}
              className="flex-shrink-0 p-2 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:bg-zinc-700 disabled:cursor-not-allowed text-white transition"
            >
              <Send size={16} />
            </button>
          </div>
          <p className="text-center text-xs text-zinc-600 mt-2">
            MemoraAI can make mistakes. Double-check important information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Index;
