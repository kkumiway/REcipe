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

import java.util.List;
import java.util.Map;
import java.util.Objects;

@Service
public class RecipeService {
    @Autowired
    private RecipeRepository recipeRepository;

    private final RestTemplate restTemplate = new RestTemplate();

    public List<Recipe> searchRecipeByIngredient(String ingredient) throws JsonProcessingException {
        List<Recipe> existingRecipes = recipeRepository.findByIngredient(ingredient);

        // 기존 DB에 데이터가 있으면 그대로 반환
        if (!existingRecipes.isEmpty()) {
            return existingRecipes;
        }

        // 없으면 FastAPI에서 데이터 가져오기
        String url = "https://potential-fortnight-5grr6qqqr4r6h4j5x-8000.app.github.dev/recipe/" + ingredient;
        ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);

        if (response.getStatusCode() == HttpStatus.OK) {
            Map<String, Object> recipeData = (Map<String, Object>) response.getBody();

            Recipe recipe = new Recipe();
            recipe.setMenuName((String) recipeData.get("menuName"));
            recipe.setMenuImage((String) recipeData.get("menuImage"));
            recipe.setMenuTip((String) recipeData.get("menuTip"));

            // JSON 데이터
            recipe.setIngredients(new ObjectMapper().writeValueAsString(recipeData.get("ingredients")));
            recipe.setRecipeInfo(new ObjectMapper().writeValueAsString(recipeData.get("recipeInfo")));

            // ✅ youtubeVideo가 null인지 체크 후 처리
            if (recipeData.containsKey("youtubeVideo") && recipeData.get("youtubeVideo") != null) {
                Map<String, String> youtube = (Map<String, String>) recipeData.get("youtubeVideo");
                recipe.setYoutubeTitle(youtube.getOrDefault("title", "제목 없음"));
                recipe.setYoutubeUrl(youtube.getOrDefault("url", "링크 없음"));
            } else {
                recipe.setYoutubeTitle("제목 없음");
                recipe.setYoutubeUrl("링크 없음");
            }

            recipeRepository.save(recipe); // 저장
            return List.of(recipe);
        }
        return List.of();
    }
}
