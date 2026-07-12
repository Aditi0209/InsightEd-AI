import BASE_URL, { getAuthHeaders } from "./api";

export async function askTutor(question) {
    const response = await fetch(
        `${BASE_URL}/chat?query=${encodeURIComponent(question)}`,
        {
            method: "POST",
            headers: getAuthHeaders()
        }
    );

    if (!response.ok) {
        throw new Error("Unable to contact AI Tutor.");
    }

    return response.json();
}