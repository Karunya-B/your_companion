import { useState } from "react";
import { logReflection } from "../services/api";

function Reflection() {
    const [content, setContent] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!content.trim() || loading) return;
        setLoading(true);
        setResult(null);

        try {
            const data = await logReflection(content);
            setResult({ type: "success", feedback: data.ai_feedback });
            setContent("");
        } catch {
            setResult({ type: "error", feedback: "Failed to save reflection." });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="page-header">
                <h2>Daily Reflection</h2>
                <p>Write about your day and get mentoring feedback</p>
            </div>

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>How was your day?</label>
                        <textarea
                            placeholder="Today I studied for two hours and then lost motivation…"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                        />
                    </div>
                    <button className="btn btn-primary" disabled={loading || !content.trim()}>
                        {loading ? "Saving…" : "Submit Reflection"}
                    </button>
                </form>

                {result && (
                    <div className={`toast ${result.type === "success" ? "toast-success" : "toast-error"}`}>
                        {result.type === "success" ? (
                            <>
                                <strong>AI Feedback:</strong> {result.feedback}
                            </>
                        ) : (
                            result.feedback
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Reflection;
