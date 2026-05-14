package com.app.controller;

import com.app.dto.RoleDTO;
import com.app.service.RoleService;
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

@Tag(name = "Rôles", description = "CRUD des rôles et gestion des permissions associées")
@SecurityRequirement(name = "bearerAuth")
@RestController
@RequestMapping("/api/roles")
@RequiredArgsConstructor
public class RoleController {

    private final RoleService roleService;

    @Operation(summary = "Lister tous les rôles")
    @ApiResponse(responseCode = "200", description = "Liste retournée avec succès")
    @GetMapping
    public ResponseEntity<List<RoleDTO>> getAll() {
        return ResponseEntity.ok(roleService.getAll());
    }

    @Operation(summary = "Obtenir un rôle par ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Rôle trouvé"),
        @ApiResponse(responseCode = "404", description = "Rôle introuvable")
    })
    @GetMapping("/{id}")
    public ResponseEntity<RoleDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(roleService.getById(id));
    }

    @Operation(summary = "Créer un rôle (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Rôle créé"),
        @ApiResponse(responseCode = "400", description = "Données invalides"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<RoleDTO> create(@Valid @RequestBody RoleDTO dto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(roleService.createRole(dto));
    }

    @Operation(summary = "Modifier un rôle (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Rôle mis à jour"),
        @ApiResponse(responseCode = "404", description = "Rôle introuvable"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<RoleDTO> update(@PathVariable Long id, @Valid @RequestBody RoleDTO dto) {
        return ResponseEntity.ok(roleService.updateRole(id, dto));
    }

    @Operation(summary = "Assigner des permissions à un rôle (ADMIN)",
               description = "Remplace l'ensemble des permissions du rôle par la liste fournie.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Permissions assignées"),
        @ApiResponse(responseCode = "404", description = "Rôle introuvable"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @PostMapping("/{id}/permissions")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<RoleDTO> assignPermissions(@PathVariable Long id, @RequestBody List<Long> permissionIds) {
        return ResponseEntity.ok(roleService.assignPermissions(id, permissionIds));
    }

    @Operation(summary = "Supprimer un rôle (ADMIN)")
    @ApiResponses({
        @ApiResponse(responseCode = "204", description = "Rôle supprimé"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis"),
        @ApiResponse(responseCode = "409", description = "Rôle encore assigné à des utilisateurs — impossible de supprimer"),
        @ApiResponse(responseCode = "500", description = "Erreur serveur lors de la suppression")
    })
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> delete(@PathVariable Long id) {
        try {
            roleService.deleteRole(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalStateException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(Map.of("message", e.getMessage()));
        } catch (RuntimeException e) {
            return ResponseEntity.internalServerError()
                    .body(Map.of("message", "Erreur lors de la suppression du rôle."));
        }
    }
}
