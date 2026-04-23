package com.internship.tool.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.*;

import java.time.Duration;
import java.util.List;
import java.util.Map;

@Component
public class AiServiceClient {

    private final RestTemplate restTemplate;

    // This reads from application.yml
    @Value("${ai.service.url}")
    private String aiServiceUrl;

    // Constructor — set 10 second timeout
    public AiServiceClient(RestTemplateBuilder builder) {
        this.restTemplate = builder
            .setConnectTimeout(Duration.ofSeconds(10))
            .setReadTimeout(Duration.ofSeconds(10))
            .build();
    }

    // ── Call /describe endpoint
    public Map<String, Object> describe(Map<String, Object> payload) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> request = 
                new HttpEntity<>(payload, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(
                aiServiceUrl + "/describe",
                request,
                Map.class
            );

            System.out.println("✅ AI /describe called successfully");
            return response.getBody();

        } catch (Exception e) {
            // Never crash — just log and return null
            System.out.println("❌ AI /describe failed: " + e.getMessage());
            return null;
        }
    }

    // ── Call /recommend endpoint
    public List<Map<String, Object>> recommend(Map<String, Object> payload) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> request = 
                new HttpEntity<>(payload, headers);

            ResponseEntity<List> response = restTemplate.postForEntity(
                aiServiceUrl + "/recommend",
                request,
                List.class
            );

            System.out.println("✅ AI /recommend called successfully");
            return response.getBody();

        } catch (Exception e) {
            // Never crash — just log and return null
            System.out.println("❌ AI /recommend failed: " + e.getMessage());
            return null;
        }
    }

    // ── Call /health endpoint
    public Map<String, Object> health() {
        try {
            ResponseEntity<Map> response = restTemplate.getForEntity(
                aiServiceUrl + "/health",
                Map.class
            );
            return response.getBody();
        } catch (Exception e) {
            System.out.println("❌ AI /health failed: " + e.getMessage());
            return null;
        }
    }
}