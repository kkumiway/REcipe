import axios from "axios";

const BASE_URL = "http://localhost:8080/api/recipes";

// 🔥 재료 검색 API 호출
export const fetchRecipes = async (ingredient) => {
    if (!ingredient.trim()) return [];

    try {
        const response = await axios.get(`${BASE_URL}/search/${ingredient}`);
        return response.data;
    } catch (error) {
        console.error("API 요청 실패:", error);
        return [];
    }
};
