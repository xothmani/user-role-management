package com.app.controller;

import com.app.dto.PermissionDTO;
import com.app.service.PermissionService;
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
import java.util.Map;

@Tag(name = "Permissions", description = "CRUD des permissions atomiques assignables aux rôles")
@SecurityRequirement(name = "bearerAuth")
@RestController
@RequestMapping("/api/permissions")
@RequiredArgsConstructor
public class PermissionController {

    private final PermissionService permissionService;

    @Operation(summary = "Lister toutes les permissions")
    @ApiResponse(responseCode = "200", description = "Liste retournée avec succès")
    @GetMapping
    public ResponseEntity<List<PermissionDTO>> getAll() {
        return ResponseEntity.ok(permissionService.getAll());
    }

    @Operation(summary = "Obtenir une permission par ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Permission trouvée"),
        @ApiResponse(responseCode = "404", description = "Permission introuvable")
    })
    @GetMapping("/{id}")
    public ResponseEntity<PermissionDTO> getById(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(permissionService.getById(id));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @Operation(summary = "Créer une permission (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Permission créée"),
        @ApiResponse(responseCode = "400", description = "Données invalides"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<PermissionDTO> create(@Valid @RequestBody PermissionDTO dto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(permissionService.createPermission(dto));
    }

    @Operation(summary = "Modifier une permission (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Permission mise à jour"),
        @ApiResponse(responseCode = "404", description = "Permission introuvable"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<PermissionDTO> update(@PathVariable Long id, @Valid @RequestBody PermissionDTO dto) {
        return ResponseEntity.ok(permissionService.updatePermission(id, dto));
    }

    @Operation(summary = "Supprimer une permission (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "204", description = "Permission supprimée"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis"),
        @ApiResponse(responseCode = "409", description = "Permission encore utilisée — impossible de supprimer"),
        @ApiResponse(responseCode = "500", description = "Erreur serveur lors de la suppression")
    })
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> delete(@PathVariable Long id) {
        try {
            permissionService.deletePermission(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalStateException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(Map.of("message", e.getMessage()));
        } catch (RuntimeException e) {
            return ResponseEntity.internalServerError()
                    .body(Map.of("message", "Erreur lors de la suppression de la permission."));
        }
    }
}
