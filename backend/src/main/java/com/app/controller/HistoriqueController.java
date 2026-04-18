package com.app.controller;

import com.app.dto.HistoriqueDTO;
import com.app.service.HistoriqueService;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/historique")
@RequiredArgsConstructor
public class HistoriqueController {

    private final HistoriqueService historiqueService;

    @GetMapping
    public ResponseEntity<List<HistoriqueDTO>> getAll(
        @RequestParam(required = false) Long userId,
        @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dateDebut,
        @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dateFin
    ) {
        LocalDateTime debut = dateDebut != null ? dateDebut.atStartOfDay() : null;
        LocalDateTime fin = dateFin != null ? dateFin.atTime(23, 59, 59) : null;
        return ResponseEntity.ok(historiqueService.getAll(userId, debut, fin));
    }
}
