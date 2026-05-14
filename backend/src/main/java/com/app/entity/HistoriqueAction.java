package com.app.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "historique_actions")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class HistoriqueAction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "utilisateur_id")
    private Utilisateur utilisateur;

    @Column(nullable = false)
    private String action;

    @Column(nullable = true)
    private String details;

    @Column(nullable = false)
    private LocalDateTime date;
}
