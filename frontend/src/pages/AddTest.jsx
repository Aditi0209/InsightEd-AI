import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { addTest } from "../api/test";
import { isAuthenticated } from "../api/api";

function AddTest() {
    const navigate = useNavigate();
    const [subject, setSubject] = useState("");
    const [topic, setTopic] = useState("");
    const [score, setScore] = useState("");
    const [maxScore, setMaxScore] = useState("100");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate("/login");
        }
    }, [navigate]);

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setMessage("");

        try {
            await addTest({
                subject,
                topic,
                score: Number(score),
                max_score: Number(maxScore)
            });
            setMessage("✅ Test added successfully!");
            setTimeout(() => {
                navigate("/dashboard");
            }, 1200);
        } catch (err) {
            console.error(err);
            setMessage("❌ Failed to add test.");
        }

        setLoading(false);
    }

    return (
        <div className="page">
            <h1>Add Test</h1>
            <div className="result-card">
                <form className="test-form" onSubmit={handleSubmit}>
                    <label>Subject</label>
                    <select
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                        required
                    >
                        <option value="">Select Subject</option>
                        <option>Physics</option>
                        <option>Chemistry</option>
                        <option>Mathematics</option>
                    </select>
                    <label>Topic</label>
                    <input
                        type="text"
                        placeholder="Topic Name"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        required
                    />
                    <label>Score</label>
                    <input
                        type="number"
                        value={score}
                        onChange={(e) => setScore(e.target.value)}
                        required
                    />
                    <label>Maximum Score</label>
                    <input
                        type="number"
                        value={maxScore}
                        onChange={(e) => setMaxScore(e.target.value)}
                        required
                    />
                    <button className="login-btn" disabled={loading}>
                        {loading ? "Saving..." : "Save Test"}
                    </button>
                </form>
                {
                    message &&
                    <p style={{ marginTop: 20, fontWeight: "bold" }}>
                        {message}
                    </p>
                }
            </div>
        </div>
    );
}

export default AddTest;