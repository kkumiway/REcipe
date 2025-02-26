// App.js
import React, { useState } from "react";
import IngredientInput from "./components/IngredientInput";
import RecipeDisplay from "./components/RecipeDisplay";
import axios from "axios";

function App() {
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchRecipe = async (ingredients) => {
    setLoading(true);
    try {
      // 서버에 요청하여 레시피를 받아옵니다.
      const response = await axios.post("/api/getRecipe", { ingredients });
      setRecipe(response.data);
    } catch (error) {
      console.error("레시피 요청 중 오류 발생:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>맞춤형 레시피 추천</h1>
      <IngredientInput onSubmit={fetchRecipe} />
      {loading ? <p>로딩 중...</p> : <RecipeDisplay recipe={recipe} />}
    </div>
  );
}

export default App;
