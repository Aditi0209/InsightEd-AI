import BASE_URL, { getAuthHeaders } from "./api";

export async function submitDiagnostic(data) {
    const { student_id, ...rest } = data;
    const params = new URLSearchParams(rest);
    const response = await fetch(
        `${BASE_URL}/diagnostic?${params.toString()}`,
        {
            method: "POST",
            headers: getAuthHeaders()
        }
    );

    if (!response.ok) {
        throw new Error("Unable to submit diagnostic.");
    }

    return response.json();
}