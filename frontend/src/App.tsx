import {useEffect, useRef, useState} from "react";
import axios from "axios";
import {v4 as uuidv4} from "uuid";

type Message = {
    role: "user" | "bot";
    text: string;
};

function App() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const sessionIdRef = useRef<string | null>(null);
    const chatEndRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({behavior: "smooth"});
    }, [messages]);

    useEffect(() => {
        const stored = localStorage.getItem("session_id");
        if (!stored) {
            const id = uuidv4();
            localStorage.setItem("session_id", id);
            sessionIdRef.current = id;
        } else {
            sessionIdRef.current = stored;
        }
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg: Message = {role: "user", text: input};
        setMessages((prev) => [...prev, userMsg]);
        setLoading(true);
        setInput("");

        try {
            const res = await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/chat`, {
                session_id: sessionIdRef.current,
                prompt: userMsg.text,
            });

            const botMsg: Message = {role: "bot", text: res.data.response};
            setMessages((prev) => [...prev, botMsg]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                {role: "bot", text: "❌ Something went wrong. Try again later."},
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-gray-900 text-white">
            <header className="text-xl font-bold p-4 border-b border-gray-700 text-center shadow-md">
                Investor Chat Assistant
            </header>

            <div className="flex-1 w-full max-w-[55%] m-auto overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`max-w-[80%] p-3 rounded-lg shadow-md transition-all duration-300 ${
                            msg.role === "user"
                                ? "bg-blue-600 ml-auto animate-fade-in-up"
                                : "bg-gray-700 mr-auto animate-fade-in-up"
                        }`}
                    >
                        <p className="whitespace-pre-wrap">{msg.text}</p>
                    </div>
                ))}
                {loading && (
                    <div
                        className="mr-auto p-3 bg-gray-700 rounded-lg animate-pulse text-gray-300 shadow-md max-w-[60%]">
                        <span className="block w-24 h-4 bg-gray-500 rounded mb-1"/>
                        <span className="block w-20 h-4 bg-gray-600 rounded"/>
                    </div>
                )}
                <div ref={chatEndRef}/>
            </div>

            <form
                onSubmit={handleSubmit}
                className="w-full max-w-2xl mx-auto p-4"
            >
                <div className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your question..."
                        disabled={loading}
                        className="w-full pr-12 pl-4 py-3 rounded-full bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className={`absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full transition ${
                            loading || !input.trim()
                                ? "text-gray-400 cursor-not-allowed"
                                : "text-blue-400 hover:text-blue-600"
                        }`}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-5 w-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M5 12h14M12 5l7 7-7 7"
                            />
                        </svg>
                    </button>
                </div>
            </form>

        </div>
    );
}

export default App;
