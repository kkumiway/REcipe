import React from "react";

const RecipeCard = ({ recipe }) => {
    let recipeInfo = [];
    let ingredients = [];

    try {
        // 🥄 `recipeInfo` JSON 파싱
        const parsedInfo = JSON.parse(recipe.recipeInfo);
        recipeInfo = Array.isArray(parsedInfo) ? parsedInfo : [];
    } catch (error) {
        console.error("JSON 파싱 오류 (recipeInfo):", error);
    }

    try {
        console.log("ingredients 데이터:", recipe.ingredients); // 데이터 확인

        // 🍳 `ingredients` JSON 파싱 or 문자열 처리
        if (typeof recipe.ingredients === "string") {
            if (recipe.ingredients.startsWith("[") && recipe.ingredients.endsWith("]")) {
                // JSON 문자열이면 파싱
                const parsedIngredients = JSON.parse(recipe.ingredients);
                ingredients = Array.isArray(parsedIngredients) ? parsedIngredients : [];
            } else {
                // 쉼표(,)로 구분된 문자열이면 배열로 변환
                ingredients = recipe.ingredients.split(",").map(item => item.trim());
            }
        } else if (Array.isArray(recipe.ingredients)) {
            ingredients = recipe.ingredients; // 이미 배열이면 그대로 사용
        }
    } catch (error) {
        console.error("JSON 파싱 오류 (ingredients):", error);
    }

    return (
        <div className="recipe-card">
            <h2>{recipe.menuName}</h2>
            <img src={recipe.menuImage} alt={recipe.menuName}/>
            {/* 🥄 재료 리스트 */}
            <h3>재료</h3>
            <p className="ingredients">
                {ingredients.length > 0 ? `🥄 ${ingredients.join(" ")}` : "❌ 재료 정보 없음"}
            </p>

            {/* 🍳 조리 과정 */}
            <h3>조리 과정</h3>
            <p className= "menu-tip" >
                {recipe.menuTip}
            </p>
            <ul>
                {recipeInfo.map((step, index) => <li key={index}>{step}</li>)}
            </ul>

            {/* 📺 유튜브 영상 */}
            <p>
                📺 <a href={recipe.youtubeUrl} target="_blank" rel="noopener noreferrer">
                {recipe.youtubeTitle}
            </a>
            </p>
        </div>
    );
};

export default RecipeCard;
