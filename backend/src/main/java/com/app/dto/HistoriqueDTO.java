package com.app.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class HistoriqueDTO {
    private Long id;
    private Long utilisateurId;
    private String utilisateurNom;
    private String utilisateurEmail;
    private String action;
    private LocalDateTime date;
}
