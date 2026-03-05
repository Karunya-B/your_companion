import { useState, useEffect } from "react";
import { fetchDailyGuidance } from "../services/api";

function Dashboard() {
    const [guidance, setGuidance] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        fetchDailyGuidance()
            .then((data) => setGuidance(data))
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    const loadBadge = (level) => {
        const key = level?.toLowerCase() || "medium";
        return <span className={`badge badge-${key}`}>{level}</span>;
    };

    return (
        <div>
            <div className="page-header">
                <h2>Dashboard</h2>
                <p>Your daily AI guidance at a glance</p>
            </div>

            {loading && (
                <div className="loader">
                    <div className="spinner" />
                    Generating your daily guidance…
                </div>
            )}

            {error && <div className="toast toast-error">⚠️ {error}</div>}

            {guidance && (
                <>
                    <div className={`stress-banner ${guidance.stress_warning ? "warning" : "ok"}`}>
                        {guidance.stress_warning
                            ? "⚠️ Stress detected — consider taking it easy today."
                            : "✅ You're looking balanced today. Keep it up!"}
                    </div>

                    <div className="card">
                        <h3>AI Message</h3>
                        <p style={{ lineHeight: 1.65, color: "var(--text-secondary)" }}>
                            {guidance.message}
                        </p>
                    </div>

                    <div className="card">
                        <h3>Suggested Task Flow</h3>
                        {guidance.suggested_tasks?.length > 0 ? (
                            <ul className="task-list">
                                {guidance.suggested_tasks.map((task, i) => (
                                    <li key={i} className="task-item">
                                        <span>{task.description}</span>
                                        {loadBadge(task.cognitive_load)}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p style={{ color: "var(--text-muted)" }}>
                                No tasks logged yet. Add some tasks to get started!
                            </p>
                        )}
                    </div>
                </>
            )}
        </div>
    );
}

export default Dashboard;
