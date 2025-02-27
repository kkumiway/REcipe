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

@Service
public class RecipeService {

    @Autowired
    private RecipeRepository recipeRepository;

    private final RestTemplate restTemplate = new RestTemplate();

    public List<Recipe> searchRecipeByIngredient(String ingredient) throws JsonProcessingException {
        // 1️⃣ 먼저 DB에서 해당 재료로 검색
        List<Recipe> existingRecipes = recipeRepository.findByIngredient(ingredient);

        // ✅ 기존 DB에 데이터가 있으면 그대로 반환
        if (!existingRecipes.isEmpty()) {
            System.out.println("✅ DB에서 찾은 레시피 반환: " + existingRecipes);
            return existingRecipes;
        }

        // 2️⃣ FastAPI에서 데이터 가져오기
        String url = "https://potential-fortnight-5grr6qqqr4r6h4j5x-8000.app.github.dev/recipe/" + ingredient;
        System.out.println("🔍 FastAPI 호출 URL: " + url);

        ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);

        // ✅ 응답이 정상적으로 왔을 때 처리
        if (response.getStatusCode() == HttpStatus.OK) {
            Map<String, Object> responseData = (Map<String, Object>) response.getBody();
            System.out.println("🔥 FastAPI 응답 데이터: " + responseData);

            // `recipe` 키 아래에서 데이터 추출
            Map<String, Object> recipeData = (Map<String, Object>) responseData.get("recipe");

            if (recipeData == null) {
                System.out.println("⚠️ recipe 데이터가 없음!");
                return List.of();
            }

            Recipe recipe = new Recipe();

            // `menuName`이 null이면 기본값 설정
            String menuName = (String) recipeData.get("menuName");
            if (menuName == null || menuName.trim().isEmpty()) {
                System.out.println("⚠️ menuName이 NULL이거나 비어 있음");
                menuName = "이름 없음"; // 기본값 설정
            }
            recipe.setMenuName(menuName);

            recipe.setMenuImage((String) recipeData.get("menuImage"));
            recipe.setMenuTip((String) recipeData.get("menuTip"));

            // JSON 데이터로 저장
            recipe.setIngredients(new ObjectMapper().writeValueAsString(recipeData.get("ingredients")));
            recipe.setRecipeInfo(new ObjectMapper().writeValueAsString(recipeData.get("recipeInfo")));

            // ✅ youtubeVideo가 있는지 체크 후 저장
            if (recipeData.containsKey("youtubeVideo") && recipeData.get("youtubeVideo") != null) {
                Map<String, String> youtube = (Map<String, String>) recipeData.get("youtubeVideo");
                recipe.setYoutubeTitle(youtube.getOrDefault("title", "제목 없음"));
                recipe.setYoutubeUrl(youtube.getOrDefault("url", "링크 없음"));
            } else {
                recipe.setYoutubeTitle("제목 없음");
                recipe.setYoutubeUrl("링크 없음");
            }

            // 🔥 레시피 DB에 저장
            recipeRepository.save(recipe);
            System.out.println("✅ 새로운 레시피 저장: " + recipe);
            return List.of(recipe);
        }

        System.out.println("⚠️ FastAPI에서 데이터를 가져오지 못함");
        return List.of();
    }
}
