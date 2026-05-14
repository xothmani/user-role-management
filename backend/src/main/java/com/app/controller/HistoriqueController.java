package com.app.controller;

import com.app.dto.HistoriqueDTO;
import com.app.service.HistoriqueService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Tag(name = "Historique", description = "Consultation du journal d'audit des actions utilisateurs")
@SecurityRequirement(name = "bearerAuth")
@RestController
@RequestMapping("/api/historique")
@RequiredArgsConstructor
public class HistoriqueController {

    private final HistoriqueService historiqueService;

    @Operation(summary = "Lister les actions auditées",
               description = "Retourne toutes les actions enregistrées, filtrables par utilisateur et/ou plage de dates.")
    @ApiResponse(responseCode = "200", description = "Journal retourné avec succès")
    @GetMapping
    public ResponseEntity<List<HistoriqueDTO>> getAll(
        @Parameter(description = "Filtrer par ID utilisateur") @RequestParam(required = false) Long userId,
        @Parameter(description = "Date de début (ISO 8601 : yyyy-MM-dd)") @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dateDebut,
        @Parameter(description = "Date de fin (ISO 8601 : yyyy-MM-dd)")   @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate dateFin
    ) {
        LocalDateTime debut = dateDebut != null ? dateDebut.atStartOfDay() : null;
        LocalDateTime fin = dateFin != null ? dateFin.atTime(23, 59, 59) : null;
        return ResponseEntity.ok(historiqueService.getAll(userId, debut, fin));
    }
}
