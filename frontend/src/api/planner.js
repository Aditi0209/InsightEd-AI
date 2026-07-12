import BASE_URL, { getAuthHeaders } from "./api";

export async function getPlanner() {
    const response = await fetch(`${BASE_URL}/planner`, {
        headers: getAuthHeaders()
    });

    if (!response.ok) {
        throw new Error("Unable to load study plan.");
    }

    return response.json();
}