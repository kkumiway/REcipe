package start.backend.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import start.backend.entity.Recipe;
import start.backend.service.RecipeService;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/recipes")
@CrossOrigin(origins = "http://localhost:3000")
public class RecipeController {
    @Autowired
    private RecipeService recipeService;

    @GetMapping("/search/{ingredient}")
    public ResponseEntity<List<Recipe>> searchRecipe(@PathVariable String ingredient) throws JsonProcessingException {

        return ResponseEntity.ok(recipeService.searchRecipeByIngredient(ingredient));
    }
}
