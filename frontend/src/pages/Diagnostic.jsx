import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { submitDiagnostic } from "../api/diagnostic";
import { isAuthenticated } from "../api/api";

function Diagnostic() {
    const [form, setForm] = useState({
        confidence_level: "",
        study_hours_per_day: "",
        academic_goal: "",
        preferred_learning_style: "",
        self_feedback: ""
    });
    const [result, setResult] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate("/login");
        }
    }, [navigate]);

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    }

    async function handleSubmit() {
        const response = await submitDiagnostic(form);
        setResult(response);
    }

    return (
        <div className="page">
            <h1>Learning Diagnostic</h1>
            <div className="result-card">
                <input
                    name="confidence_level"
                    placeholder="Confidence Level"
                    onChange={handleChange}
                />
                <br/><br/>
                <input
                    name="study_hours_per_day"
                    placeholder="Study Hours Per Day"
                    onChange={handleChange}
                />
                <br/><br/>
                <input
                    name="academic_goal"
                    placeholder="Academic Goal"
                    onChange={handleChange}
                />
                <br/><br/>
                <input
                    name="preferred_learning_style"
                    placeholder="Learning Style"
                    onChange={handleChange}
                />
                <br/><br/>
                <textarea
                    rows="5"
                    name="self_feedback"
                    placeholder="Describe your learning difficulties"
                    onChange={handleChange}
                />
                <br/><br/>
                <button className="login-btn" onClick={handleSubmit}>
                    Generate Profile
                </button>
            </div>
            {
                result &&
                <div className="result-card">
                    <h2>Learning Profile</h2>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
            }
        </div>
    );
}

export default Diagnostic;