import axios from "axios";
import BASE_URL, { getAuthHeaders } from "./api";

export async function addTest(testData) {
    const response = await axios.post(`${BASE_URL}/test`, testData, {
        headers: getAuthHeaders()
    });
    return response.data;
}