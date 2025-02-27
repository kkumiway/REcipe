package start.backend.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import start.backend.entity.Recipe;
import start.backend.repository.RecipeRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class RecipeService {
    @Autowired
    private RecipeRepository recipeRepository;

    private final RestTemplate restTemplate = new RestTemplate();

    public List<Recipe> searchRecipeByIngredient(String ingredient) throws JsonProcessingException {
        List<Recipe> existingRecipes = new ArrayList<>();
        Recipe recipe1 = new Recipe();
        recipe1.setId(123L);
        recipe1.setMenuName("제육볶음");
        recipe1.setMenuImage("http://localhost:8080/image/복습용프로필.jpg");
        recipe1.setIngredients("돼지고기, 고추장, 대파, 마늘");
        recipe1.setRecipeInfo("1. 돼지고기를 얇게 썬다. 2. 양념을 만든다. 3. 고기를 볶는다.");
        recipe1.setMenuTip("센 불에서 빠르게 볶아야 맛있음");
        recipe1.setYoutubeTitle("마늘치킨 만드는 법");
        recipe1.setYoutubeUrl("https://www.youtube.com/watch?v=abcdef1");

        existingRecipes.add(recipe1);
        // List<Recipe> existingRecipes = recipeRepository.findByIngredient(ingredient);
        if (!existingRecipes.isEmpty()) {
            return existingRecipes;
        }

        // FastAPI에서 데이터 가져오기
        String url = "https://potential-fortnight-5grr6qqqr4r6h4j5x-8000.app.github.dev/recipe/" + ingredient;
        ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);

        if (response.getStatusCode() == HttpStatus.OK) {
            Map<String, Object> recipeData = (Map<String, Object>) response.getBody().get("recipe");

            Recipe recipe = new Recipe();
            recipe.setMenuName((String) recipeData.get("menuName"));
            recipe.setMenuImage((String) recipeData.get("menuImage"));
            recipe.setMenuTip((String) recipeData.get("menuTip"));

            // JSON 데이터 저장
            recipe.setIngredients(new ObjectMapper().writeValueAsString(recipeData.get("ingredients")));
            recipe.setRecipeInfo(new ObjectMapper().writeValueAsString(recipeData.get("recipeInfo")));

            Map<String, String> youtube = (Map<String, String>) recipeData.get("youtubeVideo");
            recipe.setYoutubeTitle(youtube.get("title"));
            recipe.setYoutubeUrl(youtube.get("url"));

            recipeRepository.save(recipe);
            return List.of(recipe);
        }
        return List.of();
    }
}

