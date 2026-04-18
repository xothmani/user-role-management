package com.app.repository;

import com.app.entity.Utilisateur;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UtilisateurRepository extends JpaRepository<Utilisateur, Long> {
    Optional<Utilisateur> findByEmail(String email);
    boolean existsByEmail(String email);

    @Query("SELECT u FROM Utilisateur u LEFT JOIN FETCH u.role WHERE u.actif = true")
    List<Utilisateur> findAllActifs();
}
