import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BASE_URL from "../api/api";

import "../styles/login.css";

function Register() {
    const [studentId, setStudentId] = useState("");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [studentClass, setStudentClass] = useState("");
    const [targetExam, setTargetExam] = useState("");

    const navigate = useNavigate();

    const handleRegister = async () => {
        if (!studentId || !name || !email || !password || !studentClass) {
            alert("Please fill all required fields");
            return;
        }

        try {
            const response = await fetch(`${BASE_URL}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    student_id: studentId,
                    name,
                    email,
                    password,
                    student_class: studentClass,
                    target_exam: targetExam || null,
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.detail || "Registration failed");
                return;
            }

            alert("Registration successful! Please login.");
            navigate("/login");
        } catch (error) {
            console.log(error);
            alert("Unable to connect to server.");
        }
    };

    return (
        <div className="login-container">
            <div className="login-left">
                <h1>Academic Mentor AI</h1>
                <p>
                    Personalized AI-powered academic guidance
                    designed to improve learning outcomes.
                </p>
                <ul>
                    <li>AI Tutor powered by NCERT</li>
                    <li>Performance Analytics</li>
                    <li>Personalized Study Planner</li>
                    <li>Weekly Feedback</li>
                </ul>
            </div>
            <div className="login-right">
                <div className="login-card">
                    <h2>Student Registration</h2>
                    <input
                        type="text"
                        placeholder="Enter Student ID"
                        value={studentId}
                        onChange={(e) => setStudentId(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Enter Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    <input
                        type="email"
                        placeholder="Enter Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Enter Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Enter Class"
                        value={studentClass}
                        onChange={(e) => setStudentClass(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Enter Target Exam (Optional)"
                        value={targetExam}
                        onChange={(e) => setTargetExam(e.target.value)}
                    />
                    <button onClick={handleRegister}>Register</button>
                    <p style={{ marginTop: "1rem", fontSize: "0.9rem" }}>
                        Already have an account?{" "}
                        <span
                            style={{ color: "#4f46e5", cursor: "pointer", fontWeight: "600" }}
                            onClick={() => navigate("/login")}
                        >
                            Login here
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Register;
