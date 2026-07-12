import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getFeedback } from "../api/feedback";
import { isAuthenticated } from "../api/api";

function Feedback() {
    const [feedback, setFeedback] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate("/login");
            return;
        }

        getFeedback()
            .then(data => {
                setFeedback(data);
                setLoading(false);
            })
            .catch(() => {
                setLoading(false);
            });
    }, [navigate]);

    if (loading) {
        return <h2>Loading...</h2>;
    }

    if (!feedback) {
        return <h2>No feedback available.</h2>;
    }

    return (
        <div className="page">
            <h1>Personalized Feedback</h1>
            <div className="result-card">
                <h2>AI Mentor Feedback</h2>
                <pre>{feedback.feedback}</pre>
            </div>
            <div className="result-card">
                <h2>Student Overview</h2>
                <p>
                    <strong>Learning Style:</strong> {feedback.diagnostic_profile.learning_style}
                </p>
                <p>
                    <strong>Academic Goal:</strong> {feedback.diagnostic_profile.academic_goal}
                </p>
                <p>
                    <strong>Average Score:</strong> {feedback.performance_summary.average_score}
                </p>
            </div>
        </div>
    );
}

export default Feedback;