package com.app.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class UtilisateurDTO {
    private Long id;

    @NotBlank
    private String nom;

    @Email
    @NotBlank
    private String email;

    private String motDePasse;

    private Long roleId;
    private String roleNom;

    private boolean actif = true;
}
