package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/bot/chat") // ✅ 프론트엔드에서 백엔드 API 요청을 허용
                        .allowedOrigins("http://localhost:3000") // ✅ React 개발 서버 주소
                        .allowedMethods("POST") // ✅ POST 요청 허용
                        .allowedHeaders("*") // ✅ 모든 헤더 허용
                        .allowCredentials(true); // ✅ 쿠키 및 인증 정보 허용 (필요한 경우)
            }
        };
    }
}
