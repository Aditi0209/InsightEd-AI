import BASE_URL, { getAuthHeaders } from "./api";

export async function getFeedback() {
    const response = await fetch(`${BASE_URL}/feedback`, {
        headers: getAuthHeaders()
    });

    if (!response.ok) {
        throw new Error("Unable to load feedback.");
    }

    return response.json();
}