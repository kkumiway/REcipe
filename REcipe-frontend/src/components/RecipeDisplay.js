// RecipeDisplay.js
import React from "react";

function RecipeDisplay({ recipe }) {
  if (!recipe) return null;

  return (
    <div>
      <h2>{recipe.title}</h2>
      <h3>재료</h3>
      <ul>
        {recipe.ingredients.map((ingredient, index) => (
          <li key={index}>{ingredient}</li>
        ))}
      </ul>
      <h3>레시피</h3>
      <p>{recipe.instructions}</p>
    </div>
  );
}

export default RecipeDisplay;
