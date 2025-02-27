import React from "react";
import RecipeCard from "./RecipeCard";

const RecipeList = ({ recipes }) => {
    return (
        <div>
            {recipes.length === 0 ? <p>검색 결과 없음</p> : (
                recipes.map((recipe) => <RecipeCard key={recipe.id} recipe={recipe} />)
            )}
        </div>
    );
};

export default RecipeList;
