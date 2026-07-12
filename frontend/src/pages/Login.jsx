import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BASE_URL from "../api/api";

import "../styles/login.css";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        if (!email.trim() || !password.trim()) {
            alert("Please enter email and password");
            return;
        }

        try {
            const response = await fetch(`${BASE_URL}/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.detail || "Login failed");
                return;
            }

            const data = await response.json();

            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("student_id", data.student_id);
            localStorage.setItem("student_name", data.name);

            navigate("/dashboard");
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
                    <h2>Student Login</h2>
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
                    <button onClick={handleLogin}>Login</button>
                    <p style={{ marginTop: "1rem", fontSize: "0.9rem" }}>
                        Don't have an account?{" "}
                        <span
                            style={{ color: "#4f46e5", cursor: "pointer", fontWeight: "600" }}
                            onClick={() => navigate("/register")}
                        >
                            Register here
                        </span>
                    </p>
                </div>
            </div>
            </div>
    );
}

export default Login;