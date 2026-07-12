import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPerformance } from "../api/performance";
import { isAuthenticated } from "../api/api";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid
} from "recharts";

function Performance() {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate("/login");
            return;
        }

        getPerformance()
            .then(data => {
                setReport(data);
                setLoading(false);
            })
            .catch(() => {
                setLoading(false);
            });
    }, [navigate]);

    if (loading) {
        return <h2>Loading...</h2>;
    }

    if (!report) {
        return <h2>No performance report found.</h2>;
    }

    const summary = report.performance_summary;
    const chartData = Object.entries(
        summary.subject_averages
    ).map(([subject, score]) => ({ subject, score }));

    return (
        <div className="page">
            <h1>📊 Performance Analytics</h1>
            {/* Summary */}
            <div className="summary-cards">
                <div className="summary-card score-card">
                    <h4>Overall Score</h4>
                    <h2>{summary.average_score}%</h2>
                    <div className="progress-bar">
                        <div
                            className="progress-fill"
                            style={{ width: `${summary.average_score}%` }}
                        ></div>
                    </div>
                </div>
                <div className="summary-card strong-card">
                    <h4>Strongest Subject</h4>
                    <h2>{summary.strongest_subject}</h2>
                </div>
                <div className="summary-card weak-card">
                    <h4>Needs Attention</h4>
                    <h2>{summary.weakest_subject}</h2>
                </div>
            </div>
            {/* Chart */}
            <div className="result-card">
                <h2>Subject Performance</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="subject" />
                        <YAxis />
                        <Tooltip />
                        <Bar
                            dataKey="score"
                            fill="#2563eb"
                            radius={[8, 8, 0, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
            {/* AI Analysis */}
            <div className="result-card">
                <h2>🤖 AI Analysis</h2>
                <div className="analysis-box">
                    {
                        report.analysis
                            .split("##")
                            .filter(section => section.trim() !== "")
                            .map((section, index) => {
                                const lines = section.trim().split("\n");
                                const title = lines[0];
                                const content = lines.slice(1);
                                return (
                                    <div
                                        key={index}
                                        className="analysis-section"
                                    >
                                        <h3>{title}</h3>
                                        {
                                            content.map((line, i) => (
                                                <p key={i}>{line}</p>
                                            ))
                                        }
                                    </div>
                                );
                            })
                    }
                </div>
            </div>
        </div>
    );
}

export default Performance;