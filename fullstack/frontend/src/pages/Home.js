import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import RecipeList from "../components/RecipeList";
import LoadingSpinner from "../components/LoadingSpinner";
import { fetchRecipes } from "../api/recipeApi";

const Home = () => {
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(false); // 로딩 상태 추가

    const handleSearch = async (ingredient) => {
        if (!ingredient.trim()) return;

        setLoading(true); // 검색 시작 시 로딩 상태 활성화
        const results = await fetchRecipes(ingredient);
        setRecipes(results);
        setLoading(false); // 검색 완료 후 로딩 상태 비활성화
    };

    return (
        <div>
            <h1>🍳 재료 검색</h1>
            <SearchBar onSearch={handleSearch} />

            {loading ? <LoadingSpinner /> : <RecipeList recipes={recipes} />}
        </div>
    );
};

export default Home;
