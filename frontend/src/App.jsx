import { Routes, Route } from "react-router-dom";

import "./styles/landing.css";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Diagnostic from "./pages/Diagnostic";
import Performance from "./pages/Performance";
import Planner from "./pages/Planner";
import Tutor from "./pages/Tutor";
import Feedback from "./pages/Feedback";
import "./styles/dashboard.css";
import AddTest from "./pages/AddTest";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {

    return (

        <Routes>

            <Route
                path="/"
                element={<Landing />}
            />

            <Route
                path="/login"
                element={<Login />}
            />
            <Route
                path="/register"
                element={<Register />}
            />

            <Route
    path="/dashboard"
    element={
        <ProtectedRoute>
            <Dashboard />
        </ProtectedRoute>
    }
/>

            <Route
    path="/add-test"
    element={
        <ProtectedRoute>
            <AddTest />
        </ProtectedRoute>
    }
/>

            <Route
    path="/diagnostic"
    element={
        <ProtectedRoute>
            <Diagnostic />
        </ProtectedRoute>
    }
/>

            <Route
    path="/performance"
    element={
        <ProtectedRoute>
            <Performance />
        </ProtectedRoute>
    }
/>

           <Route
    path="/planner"
    element={
        <ProtectedRoute>
            <Planner />
        </ProtectedRoute>
    }
/>
<Route
    path="/tutor"
    element={
        <ProtectedRoute>
            <Tutor />
        </ProtectedRoute>
    }
/>

            <Route
    path="/feedback"
    element={
        <ProtectedRoute>
            <Feedback />
        </ProtectedRoute>
    }
/>

        </Routes>

    );

}

export default App;