package com.example.demo.dto;

import java.util.List;
import java.util.ArrayList;

public class ChatGPTRequest {
    private String model = "gpt-3.5-turbo-0125";  // ✅ 올바른 모델명 사용
    private List<Message> messages;

    public ChatGPTRequest(String prompt) {
        this.messages = new ArrayList<>();
        this.messages.add(new Message("user", prompt));
    }

    public String getModel() {
        return model;
    }

    public List<Message> getMessages() {
        return messages;
    }
}
