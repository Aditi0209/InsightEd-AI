import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import BASE_URL, { getAuthHeaders, isAuthenticated } from "../api/api";
import { getPerformance } from "../api/performance";

import {
    FaChartLine,
    FaClipboardList,
    FaRobot,
    FaComments,
    FaBookOpen,
    FaPlusCircle
} from "react-icons/fa";

function Dashboard() {

    const [student, setStudent] = useState(null);
    const [performance, setPerformance] = useState(null);

    const navigate = useNavigate();

    function handleLogout() {

        localStorage.removeItem("token");
        localStorage.removeItem("student_id");

        navigate("/login");

    }

    useEffect(() => {

        if (!isAuthenticated()) {

            navigate("/login");
            return;

        }

        fetch(`${BASE_URL}/student`, {

            headers: getAuthHeaders()

        })
            .then(res => res.json())
            .then(data => setStudent(data))
            .catch(err => console.log(err));

        getPerformance()
            .then(data => {

                console.log("Performance API:", data);

                setPerformance(data.performance_summary);

            })
            .catch(err => console.log(err));

    }, [navigate]);

    if (!student) {

        return (

            <h2 style={{ padding: "50px" }}>
                Loading...
            </h2>

        );

    }

    return (

        <div className="dashboard">

            {/* Header */}

            <div className="dashboard-header">

                <div>

                    <h1>
                        Welcome back, {student.name} 👋
                    </h1>

                    <p>

                        Class {student.student_class}

                        {" • "}

                        {student.target_exam} Aspirant

                    </p>

                </div>

                <button

                    className="logout-btn"

                    onClick={handleLogout}

                >

                    Logout

                </button>

            </div>

            {/* Summary Cards */}

            <div className="summary-cards">

                <div className="summary-card score-card">

                    <h4>Overall Score</h4>

                    <h2>

                        {performance
                            ? `${performance.average_score}%`
                            : "--"}

                    </h2>

                    <div className="progress-bar">

                        <div

                            className="progress-fill"

                            style={{
                                width: performance
                                    ? `${performance.average_score}%`
                                    : "0%"
                            }}

                        ></div>

                    </div>

                </div>

                <div className="summary-card strong-card">

                    <h4>Strongest Subject</h4>

                    <h2>

                        {performance
                            ? performance.strongest_subject
                            : "--"}

                    </h2>

                    <p>

                        Keep up the excellent work 🚀

                    </p>

                </div>

                <div className="summary-card weak-card">

                    <h4>Needs Attention</h4>

                    <h2>

                        {performance
                            ? performance.weakest_subject
                            : "--"}

                    </h2>

                    <p>

                        Focus more this week 📚

                    </p>

                </div>

            </div>

            {/* Quick Actions */}

            <div className="quick-actions">

                <h2>

                    ⚡ Quick Actions

                </h2>

                <div className="quick-buttons">

                    <button
                        onClick={() => navigate("/add-test")}
                    >
                        ➕ Add Test
                    </button>

                    <button
                        onClick={() => navigate("/performance")}
                    >
                        📊 View Performance
                    </button>

                    <button
                        onClick={() => navigate("/planner")}
                    >
                        📅 Study Plan
                    </button>

                    <button
                        onClick={() => navigate("/tutor")}
                    >
                        🤖 Ask AI Tutor
                    </button>

                </div>

            </div>

            {/* Feature Cards */}

            <div className="dashboard-cards">

                <div

                    className="dashboard-card"

                    onClick={() => navigate("/add-test")}

                >

                    <FaPlusCircle className="card-icon" />

                    <h3>Add Test</h3>

                    <p>Add your latest test scores.</p>

                </div>

                <div

                    className="dashboard-card"

                    onClick={() => navigate("/performance")}

                >

                    <FaChartLine className="card-icon" />

                    <h3>Performance</h3>

                    <p>Analyze strengths & weaknesses.</p>

                </div>

                <div

                    className="dashboard-card"

                    onClick={() => navigate("/planner")}

                >

                    <FaClipboardList className="card-icon" />

                    <h3>Study Planner</h3>

                    <p>Generate personalized weekly plans.</p>

                </div>

                <div

                    className="dashboard-card"

                    onClick={() => navigate("/diagnostic")}

                >

                    <FaBookOpen className="card-icon" />

                    <h3>Diagnostic</h3>

                    <p>Update your learning profile.</p>

                </div>

                <div

                    className="dashboard-card"

                    onClick={() => navigate("/tutor")}

                >

                    <FaRobot className="card-icon" />

                    <h3>AI Tutor</h3>

                    <p>Ask academic doubts instantly.</p>

                </div>

                <div

                    className="dashboard-card"

                    onClick={() => navigate("/feedback")}

                >

                    <FaComments className="card-icon" />

                    <h3>Feedback</h3>

                    <p>Receive personalized guidance.</p>

                </div>

            </div>

        </div>

    );

}

export default Dashboard;