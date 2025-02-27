package com.example.demo.controller;

import com.example.demo.dto.ChatGPTRequest;
import com.example.demo.dto.ChatGPTResponse;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/bot")
public class CustomBotController {
//키값 입력해야지 작동댐!!!!!!
    //private final String apiKey = //key값은 sua에게 물어봐주세요;
    private final String apiURL = "https://api.openai.com/v1/chat/completions";

    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/chat")
    public Map<String, String> chat(@RequestBody Map<String, String> request) {
        String userMessage = request.get("message");
        System.out.println("📩 사용자 입력: " + userMessage);

        ChatGPTRequest chatRequest = new ChatGPTRequest(userMessage);

        // ✅ HTTP 요청 헤더 설정
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + apiKey);
        headers.set("Content-Type", "application/json");

        HttpEntity<ChatGPTRequest> entity = new HttpEntity<>(chatRequest, headers);

        try {
            ResponseEntity<ChatGPTResponse> response = restTemplate.exchange(
                    apiURL,
                    HttpMethod.POST,
                    entity,
                    ChatGPTResponse.class
            );

            // 🔥 응답이 비어있는지 확인
            if (response.getBody() == null || response.getBody().getChoices() == null || response.getBody().getChoices().isEmpty()) {
                System.out.println("⚠️ OpenAI 응답이 비어 있음");
                return Map.of("response", "죄송합니다. 응답을 생성할 수 없습니다.");
            }

            // ✅ OpenAI 응답 메시지 추출
            String responseText = response.getBody().getChoices().get(0).getMessage().getContent();
            System.out.println("🤖 ChatGPT 응답: " + responseText);

            return Map.of("response", responseText);

        } catch (Exception e) {
            System.out.println("❌ OpenAI API 호출 중 오류 발생");
            e.printStackTrace();  // ✅ 여기서 전체 오류 로그를 출력
            return Map.of("response", "죄송합니다. 응답을 받을 수 없습니다.");
        }
    }
}
