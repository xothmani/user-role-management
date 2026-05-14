package com.app.service;

import com.app.dto.HistoriqueDTO;
import com.app.entity.HistoriqueAction;
import com.app.entity.Utilisateur;
import com.app.repository.HistoriqueActionRepository;
import com.app.repository.UtilisateurRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class HistoriqueService {

    private final HistoriqueActionRepository historiqueRepository;
    private final UtilisateurRepository utilisateurRepository;

    @Transactional
    public void logAction(String email, String action) {
        Utilisateur utilisateur = utilisateurRepository.findByEmail(email).orElse(null);
        HistoriqueAction historique = HistoriqueAction.builder()
            .utilisateur(utilisateur)
            .action(action)
            .date(LocalDateTime.now())
            .build();
        historiqueRepository.save(historique);
    }

    @Transactional(readOnly = true)
    public List<HistoriqueDTO> getAll(Long utilisateurId, LocalDateTime dateDebut, LocalDateTime dateFin) {
        Specification<HistoriqueAction> spec = Specification.where(null);

        if (utilisateurId != null) {
            spec = spec.and((root, query, cb) ->
                cb.equal(root.get("utilisateur").get("id"), utilisateurId));
        }
        if (dateDebut != null) {
            spec = spec.and((root, query, cb) ->
                cb.greaterThanOrEqualTo(root.get("date"), dateDebut));
        }
        if (dateFin != null) {
            spec = spec.and((root, query, cb) ->
                cb.lessThanOrEqualTo(root.get("date"), dateFin));
        }

        return historiqueRepository.findAll(spec, Sort.by(Sort.Direction.DESC, "date"))
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    private HistoriqueDTO toDTO(HistoriqueAction h) {
        HistoriqueDTO dto = new HistoriqueDTO();
        dto.setId(h.getId());
        dto.setAction(h.getAction());
        dto.setDetails(h.getDetails());
        dto.setDate(h.getDate());
        if (h.getUtilisateur() != null) {
            dto.setUtilisateurId(h.getUtilisateur().getId());
            dto.setUtilisateurNom(h.getUtilisateur().getNom());
            dto.setUtilisateurEmail(h.getUtilisateur().getEmail());
        }
        return dto;
    }
}
