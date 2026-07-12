import BASE_URL, { getAuthHeaders } from "./api";

export async function getPerformance() {
    const response = await fetch(`${BASE_URL}/performance`, {
        headers: getAuthHeaders()
    });

    if (!response.ok) {
        throw new Error("Unable to load performance.");
    }

    return response.json();
}