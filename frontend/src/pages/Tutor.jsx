import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { askTutor } from "../api/chat";
import { isAuthenticated } from "../api/api";

function Tutor() {
    const [question, setQuestion] = useState("");
    const [chatHistory, setChatHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const bottomRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate("/login");
        }
    }, [navigate]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });
    }, [chatHistory]);

    async function handleAsk() {
        if (!question.trim()) return;

        setLoading(true);

        try {
            const response = await askTutor(question);
            let aiAnswer = "";

            if (response.tutor?.answer) {
                aiAnswer = response.tutor.answer;
            } else if (response.feedback?.feedback) {
                aiAnswer = response.feedback.feedback;
            } else if (response.performance?.analysis) {
                aiAnswer = response.performance.analysis;
            } else if (response.planner?.study_plan) {
                aiAnswer = response.planner.study_plan;
            } else {
                aiAnswer = "No response generated.";
            }

            setChatHistory(prev => [
                ...prev,
                { question, answer: aiAnswer }
            ]);

            setQuestion("");
        } catch (error) {
            console.error(error);
            setChatHistory(prev => [
                ...prev,
                { question, answer: "Unable to contact AI Tutor." }
            ]);
        }

        setLoading(false);
    }

    return (
        <div className="page">
            <h1>🤖 Academic AI Tutor</h1>
            <p style={{ marginBottom: "30px", color: "#6b7280" }}>
                Ask any question from Physics, Chemistry or Mathematics.
            </p>
            <div className="result-card">
                <textarea
                    rows="5"
                    className="chat-input"
                    placeholder="Example: Explain Newton's Laws with examples."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button
                    className="login-btn"
                    onClick={handleAsk}
                    style={{ marginTop: "20px" }}
                >
                    Ask AI
                </button>
            </div>
            {
                loading &&
                <div className="chat-message ai-message">
                    <h3>🤖 Academic Mentor AI</h3>
                    <p>Thinking...</p>
                </div>
            }
            {
                chatHistory.map((chat, index) => (
                    <div key={index}>
                        <div className="chat-message user-message">
                            <h3>👤 You</h3>
                            <p>{chat.question}</p>
                        </div>
                        <div className="chat-message ai-message">
                            <h3>🤖 Academic Mentor AI</h3>
                            <div className="answer-box">
                                {
                                    chat.answer
                                        .split("##")
                                        .filter(section => section.trim() !== "")
                                        .map((section, i) => {
                                            const lines = section.trim().split("\n");
                                            const title = lines[0];
                                            const content = lines.slice(1);
                                            return (
                                                <div
                                                    key={i}
                                                    className="analysis-section"
                                                >
                                                    <h3>{title}</h3>
                                                    {
                                                        content.map((line, j) => (
                                                            <p key={j}>{line}</p>
                                                        ))
                                                    }
                                                </div>
                                            );
                                        })
                                }
                            </div>
                        </div>
                    </div>
                ))
            }
            <div ref={bottomRef}></div>
        </div>
    );
}

export default Tutor;