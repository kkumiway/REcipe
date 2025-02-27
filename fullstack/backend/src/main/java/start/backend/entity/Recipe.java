package start.backend.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Setter @Getter
@Table(name = "recipes")
public class Recipe {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "menu_name")
    private String menuName;

    @Column(name = "menu_image")
    private String menuImage;

    @Column(name = "ingredients", columnDefinition = "TEXT")
    private String ingredients;  // JSON 형태로 저장

    @Column(name = "recipe_info", columnDefinition = "TEXT")
    private String recipeInfo;  // JSON 형태로 저장

    @Column(name = "menu_tip")
    private String menuTip;

    @Column(name = "youtube_title")
    private String youtubeTitle;

    @Column(name = "youtube_url")  // 만약 DB에 없으면 추가 필요
    private String youtubeUrl;
}
