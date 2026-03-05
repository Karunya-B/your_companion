import { useState } from "react";
import { logSleepData } from "../services/api";

function HealthTracker() {
    const [form, setForm] = useState({
        sleep_hours: "",
        energy_level: "",
        mood: "",
        exercise_minutes: "",
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const payload = {
                sleep_hours: parseFloat(form.sleep_hours),
                energy_level: parseInt(form.energy_level),
                mood: form.mood,
                exercise_minutes: parseInt(form.exercise_minutes || 0),
            };
            await logSleepData(payload);
            setResult({ type: "success", msg: "Health data logged successfully!" });
            setForm({ sleep_hours: "", energy_level: "", mood: "", exercise_minutes: "" });
        } catch {
            setResult({ type: "error", msg: "Failed to log health data." });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="page-header">
                <h2>Health Tracker</h2>
                <p>Log your sleep, energy, and exercise</p>
            </div>

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="form-row">
                        <div className="form-group">
                            <label>Sleep Hours</label>
                            <input
                                type="number"
                                name="sleep_hours"
                                step="0.5"
                                min="0"
                                max="24"
                                placeholder="7.5"
                                value={form.sleep_hours}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Energy Level (1–10)</label>
                            <input
                                type="number"
                                name="energy_level"
                                min="1"
                                max="10"
                                placeholder="7"
                                value={form.energy_level}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Mood</label>
                            <input
                                type="text"
                                name="mood"
                                placeholder="Happy, Tired, Stressed…"
                                value={form.mood}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Exercise (minutes)</label>
                            <input
                                type="number"
                                name="exercise_minutes"
                                min="0"
                                placeholder="30"
                                value={form.exercise_minutes}
                                onChange={handleChange}
                            />
                        </div>
                    </div>

                    <button className="btn btn-primary" disabled={loading}>
                        {loading ? "Saving…" : "Log Health Data"}
                    </button>
                </form>

                {result && (
                    <div className={`toast ${result.type === "success" ? "toast-success" : "toast-error"}`}>
                        {result.msg}
                    </div>
                )}
            </div>
        </div>
    );
}

export default HealthTracker;
