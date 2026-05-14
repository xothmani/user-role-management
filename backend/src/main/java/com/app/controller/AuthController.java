package com.app.controller;

import com.app.dto.JwtResponse;
import com.app.dto.LoginRequest;
import com.app.dto.RegisterRequest;
import com.app.dto.UtilisateurDTO;
import com.app.service.AuthService;
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
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.Map;

@Tag(name = "Authentification", description = "Connexion, inscription et déconnexion")
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @Operation(summary = "Se connecter", description = "Authentifie l'utilisateur et retourne un token JWT Bearer.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Connexion réussie — token JWT retourné"),
        @ApiResponse(responseCode = "401", description = "Email ou mot de passe invalide")
    })
    @PostMapping("/login")
    public ResponseEntity<JwtResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @Operation(summary = "Créer un compte utilisateur (ADMIN)",
               description = "Crée un nouvel utilisateur. Le mot de passe est haché avec BCrypt. L'action est enregistrée dans l'historique.")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Utilisateur créé avec succès"),
        @ApiResponse(responseCode = "400", description = "Données de la requête invalides"),
        @ApiResponse(responseCode = "403", description = "Accès refusé — rôle ADMIN requis")
    })
    @SecurityRequirement(name = "bearerAuth")
    @PostMapping("/register")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<UtilisateurDTO> register(@Valid @RequestBody RegisterRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(authService.register(request));
    }

    @Operation(summary = "Se déconnecter",
               description = "Endpoint stateless : le serveur ne maintient pas de liste de tokens révoqués. "
                   + "Le SecurityContext du thread est vidé. Le client doit supprimer le token JWT localement.")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Déconnexion réussie")
    })
    @ExceptionHandler(AuthenticationException.class)
    public ResponseEntity<Map<String, String>> handleAuthenticationException(AuthenticationException ex) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(Map.of("message", "Identifiants invalides."));
    }

    @PostMapping("/logout")
    public ResponseEntity<Map<String, String>> logout() {
        SecurityContextHolder.clearContext();
        return ResponseEntity.ok(Map.of(
            "message", "Déconnexion réussie. Ce serveur est stateless — veuillez supprimer le token JWT côté client."
        ));
    }
}
