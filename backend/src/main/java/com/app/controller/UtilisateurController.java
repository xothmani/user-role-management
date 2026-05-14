package com.app.controller;

import com.app.dto.UtilisateurDTO;
import com.app.service.UtilisateurService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Tag(name = "Utilisateurs", description = "CRUD des comptes utilisateurs et assignation de rôles")
@SecurityRequirement(name = "bearerAuth")
@RestController
@RequestMapping("/api/utilisateurs")
@RequiredArgsConstructor
public class UtilisateurController {

    private final UtilisateurService utilisateurService;

    @Operation(summary = "Lister tous les utilisateurs")
    @ApiResponse(responseCode = "200", description = "Liste retournée avec succès")
    @GetMapping
    public ResponseEntity<List<UtilisateurDTO>> getAll() {
        return ResponseEntity.ok(utilisateurService.getAll());
    }

    @Operation(summary = "Obtenir un utilisateur par ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Utilisateur trouvé"),
        @ApiResponse(responseCode = "404", description = "Utilisateur introuvable")
    })
    @GetMapping("/{id}")
    public ResponseEntity<UtilisateurDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(utilisateurService.getById(id));
    }

    @Operation(summary = "Créer un utilisateur (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Utilisateur créé"),
        @ApiResponse(responseCode = "400", description = "Données invalides"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<UtilisateurDTO> create(@Valid @RequestBody UtilisateurDTO dto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(utilisateurService.createUtilisateur(dto));
    }

    @Operation(summary = "Modifier un utilisateur (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Utilisateur mis à jour"),
        @ApiResponse(responseCode = "404", description = "Utilisateur introuvable"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<UtilisateurDTO> update(@PathVariable Long id, @Valid @RequestBody UtilisateurDTO dto) {
        return ResponseEntity.ok(utilisateurService.updateUtilisateur(id, dto));
    }

    @Operation(summary = "Assigner un rôle à un utilisateur (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Rôle assigné"),
        @ApiResponse(responseCode = "404", description = "Utilisateur ou rôle introuvable"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PostMapping("/{id}/role/{roleId}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<UtilisateurDTO> assignRole(@PathVariable Long id, @PathVariable Long roleId) {
        return ResponseEntity.ok(utilisateurService.assignRole(id, roleId));
    }

    @Operation(summary = "Supprimer un utilisateur (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "204", description = "Utilisateur supprimé"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        utilisateurService.deleteUtilisateur(id);
        return ResponseEntity.noContent().build();
    }
}
