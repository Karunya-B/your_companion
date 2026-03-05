import { useState, useRef, useEffect } from "react";
import { sendChatMessage, getChatHistory, saveChatMessage, resetData } from "../services/api";

function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const endRef = useRef(null);

    // Load chat history on component mount
    useEffect(() => {
        const loadHistory = async () => {
            try {
                const history = await getChatHistory();
                if (history.messages && history.messages.length > 0) {
                    setMessages(history.messages.map(msg => ({
                        role: msg.role,
                        text: msg.content
                    })));
                } else {
                    // Default greeting if no history
                    setMessages([
                        { role: "ai", text: "Good morning! What are you curious about exploring today?" }
                    ]);
                }
            } catch (error) {
                console.error("Failed to load chat history:", error);
                setMessages([
                    { role: "ai", text: "Good morning! What are you curious about exploring today?" }
                ]);
            }
        };
        loadHistory();
    }, []);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = async () => {
        const text = input.trim();
        if (!text || loading) return;

        // Add user message immediately
        const userMessage = { role: "user", text };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            // Save user message to database
            try {
                await saveChatMessage("user", text);
            } catch (saveError) {
                console.error("Failed to save user message:", saveError);
            }

            // Get AI response
            const data = await sendChatMessage(text);
            const aiReply = data.reply;

            // Add AI response
            const aiMessage = { role: "ai", text: aiReply };
            setMessages((prev) => [...prev, aiMessage]);

            // Save AI response to database
            try {
                await saveChatMessage("ai", aiReply);
            } catch (saveError) {
                console.error("Failed to save AI message:", saveError);
            }
        } catch (error) {
            console.error("Chat error:", error);
            setMessages((prev) => [
                ...prev,
                { role: "ai", text: "Sorry, I couldn't process that. Please try again." },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = async () => {
        if (window.confirm("This will clear all your chat history, tasks, and data. Are you sure?")) {
            try {
                await resetData();
                setMessages([
                    { role: "ai", text: "Data reset! Good morning Karunya! What are you curious about exploring today?" }
                ]);
            } catch (error) {
                console.error("Failed to reset data:", error);
                alert("Failed to reset data. Please try again.");
            }
        }
    };

    return (
        <div>
            <div className="page-header">
                <h2>Chat with AI Mentor</h2>
                <p>Talk to your personal companion</p>
                <button 
                    className="btn btn-secondary" 
                    onClick={handleReset}
                    style={{ marginTop: '10px', fontSize: '12px' }}
                >
                    Reset All Data
                </button>
            </div>

            <div className="chat-container">
                <div className="chat-messages">
                    {messages.map((msg, i) => (
                        <div key={i} className={`chat-bubble ${msg.role}`}>
                            {msg.text}
                        </div>
                    ))}
                    {loading && (
                        <div className="chat-bubble ai">
                            <div className="loader" style={{ padding: 0 }}>
                                <div className="spinner" /> Thinking…
                            </div>
                        </div>
                    )}
                    <div ref={endRef} />
                </div>

                <div className="chat-input-area">
                    <input
                        type="text"
                        placeholder="Type a message…"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        disabled={loading}
                    />
                    <button className="btn btn-primary" onClick={handleSend} disabled={loading}>
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Chat;
