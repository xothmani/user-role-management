package com.app.repository;

import com.app.entity.HistoriqueAction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface HistoriqueActionRepository extends JpaRepository<HistoriqueAction, Long> {

    List<HistoriqueAction> findByUtilisateurIdOrderByDateDesc(Long utilisateurId);

    @Query("SELECT h FROM HistoriqueAction h WHERE " +
           "(:utilisateurId IS NULL OR h.utilisateur.id = :utilisateurId) AND " +
           "(:dateDebut IS NULL OR h.date >= :dateDebut) AND " +
           "(:dateFin IS NULL OR h.date <= :dateFin) " +
           "ORDER BY h.date DESC")
    List<HistoriqueAction> findWithFilters(
        @Param("utilisateurId") Long utilisateurId,
        @Param("dateDebut") LocalDateTime dateDebut,
        @Param("dateFin") LocalDateTime dateFin
    );
}
