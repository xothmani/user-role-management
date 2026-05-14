package com.app.repository;

import com.app.entity.HistoriqueAction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HistoriqueActionRepository extends JpaRepository<HistoriqueAction, Long>,
        JpaSpecificationExecutor<HistoriqueAction> {

    List<HistoriqueAction> findByUtilisateurIdOrderByDateDesc(Long utilisateurId);
}
