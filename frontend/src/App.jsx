import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Reflection from "./pages/Reflection";
import HealthTracker from "./pages/HealthTracker";
import ScreenTime from "./pages/ScreenTime";
import "./App.css";

const NAV_ITEMS = [
    { key: "dashboard", label: "Dashboard", icon: "📊" },
    { key: "chat", label: "Chat", icon: "💬" },
    { key: "reflection", label: "Reflection", icon: "📝" },
    { key: "health", label: "Health Tracker", icon: "🩺" },
    { key: "screen", label: "Screen Time", icon: "📱" },
];

function App() {
    const [page, setPage] = useState("dashboard");

    const renderPage = () => {
        switch (page) {
            case "dashboard":
                return <Dashboard />;
            case "chat":
                return <Chat />;
            case "reflection":
                return <Reflection />;
            case "health":
                return <HealthTracker />;
            case "screen":
                return <ScreenTime />;
            default:
                return <Dashboard />;
        }
    };

    return (
        <div className="app-layout">
            <aside className="sidebar">
                <div className="sidebar-brand">
                    <h1>Your Companion</h1>
                    <span>AI Mentor Dashboard</span>
                </div>
                <ul className="sidebar-nav">
                    {NAV_ITEMS.map((item) => (
                        <li key={item.key}>
                            <a
                                href="#"
                                className={page === item.key ? "active" : ""}
                                onClick={(e) => {
                                    e.preventDefault();
                                    setPage(item.key);
                                }}
                            >
                                <span className="icon">{item.icon}</span>
                                {item.label}
                            </a>
                        </li>
                    ))}
                </ul>
            </aside>
            <main className="main-content">{renderPage()}</main>
        </div>
    );
}

export default App;
