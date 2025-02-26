// IngredientInput.js
import React, { useState } from "react";

function IngredientInput({ onSubmit }) {
  const [ingredients, setIngredients] = useState("");

  const handleChange = (event) => {
    setIngredients(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(ingredients);
    setIngredients("");
  };

  return (
    <div>
      <input
        type="text"
        value={ingredients}
        onChange={handleChange}
        placeholder="재료를 입력하세요"
      />
      <button onClick={handleSubmit}>레시피 추천</button>
    </div>
  );
}

export default IngredientInput;
