import { useState } from "react";
import { logScreenTime } from "../services/api";

function ScreenTime() {
    const [form, setForm] = useState({ app_name: "", duration_minutes: "" });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [logs, setLogs] = useState([]);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const payload = {
                app_name: form.app_name,
                duration_minutes: parseInt(form.duration_minutes),
            };
            const data = await logScreenTime(payload);
            setLogs((prev) => [...prev, data]);
            setResult({ type: "success", msg: "Screen time logged!" });
            setForm({ app_name: "", duration_minutes: "" });
        } catch {
            setResult({ type: "error", msg: "Failed to log screen time." });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="page-header">
                <h2>Screen Time Tracker</h2>
                <p>Track your app usage throughout the day</p>
            </div>

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="form-row">
                        <div className="form-group">
                            <label>App / Activity Name</label>
                            <input
                                type="text"
                                name="app_name"
                                placeholder="YouTube, VS Code, Instagram…"
                                value={form.app_name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Duration (minutes)</label>
                            <input
                                type="number"
                                name="duration_minutes"
                                min="1"
                                placeholder="60"
                                value={form.duration_minutes}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                    <button className="btn btn-primary" disabled={loading}>
                        {loading ? "Saving…" : "Log Screen Time"}
                    </button>
                </form>

                {result && (
                    <div className={`toast ${result.type === "success" ? "toast-success" : "toast-error"}`}>
                        {result.msg}
                    </div>
                )}
            </div>

            {logs.length > 0 && (
                <div className="card">
                    <h3>Today's Logged Screen Time</h3>
                    <ul className="task-list">
                        {logs.map((log, i) => (
                            <li key={i} className="task-item">
                                <span>{log.app_name}</span>
                                <span className="badge badge-medium">{log.duration_minutes} min</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default ScreenTime;
