import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPlanner } from "../api/planner";
import { isAuthenticated } from "../api/api";

function Planner() {
    const [planner, setPlanner] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate("/login");
            return;
        }

        getPlanner()
            .then(data => {
                setPlanner(data);
                setLoading(false);
            })
            .catch(() => {
                setLoading(false);
            });
    }, [navigate]);

    if (loading) {
        return <h2>Loading...</h2>;
    }

    if (!planner) {
        return <h2>No study plan found.</h2>;
    }

    return (
        <div className="page">
            <h1>Weekly Study Planner</h1>
            <div className="result-card">
                <h2>AI Study Plan</h2>
                <pre>{planner.study_plan}</pre>
            </div>
            <div className="result-card">
                <h2>Summary</h2>
                <p>
                    <strong>Priority Subject:</strong> {planner.priority_subject}
                </p>
                <p>
                    <strong>Learning Style:</strong> {planner.learning_style}
                </p>
                <p>
                    <strong>Academic Goal:</strong> {planner.academic_goal}
                </p>
            </div>
        </div>
    );
}

export default Planner;