const BASE_URL = "http://127.0.0.1:8000";

export default BASE_URL;

export function getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

export function isAuthenticated() {
    return !!localStorage.getItem("access_token");
}