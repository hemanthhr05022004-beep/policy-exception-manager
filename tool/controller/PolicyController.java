package com.internship.tool.controller;

import com.internship.tool.entity.PolicyException;
import com.internship.tool.service.PolicyExceptionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/exceptions")
@CrossOrigin(origins = "*")
public class PolicyExceptionController {

    private final PolicyExceptionService service;

    public PolicyExceptionController(PolicyExceptionService service) {
        this.service = service;
    }

    // ── POST /api/exceptions/create
    @PostMapping("/create")
    public ResponseEntity<PolicyException> create(
        @RequestBody PolicyException policyException
    ) {
        PolicyException saved = service.create(policyException);
        return ResponseEntity.ok(saved);
    }

    // ── GET /api/exceptions/all
    @GetMapping("/all")
    public ResponseEntity<List<PolicyException>> getAll() {
        return ResponseEntity.ok(service.getAll());
    }

    // ── GET /api/exceptions/{id}
    @GetMapping("/{id}")
    public ResponseEntity<PolicyException> getById(@PathVariable Long id) {
        Optional<PolicyException> result = service.getById(id);

        if (result.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(result.get());
    }

    // ── PUT /api/exceptions/{id}
    @PutMapping("/{id}")
    public ResponseEntity<PolicyException> update(
        @PathVariable Long id,
        @RequestBody PolicyException updated
    ) {
        try {
            PolicyException result = service.update(id, updated);
            return ResponseEntity.ok(result);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // ── DELETE /api/exceptions/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<String> delete(@PathVariable Long id) {
        try {
            service.delete(id);
            return ResponseEntity.ok("Record deleted successfully");
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
}