package com.app.service;

import com.app.dto.UtilisateurDTO;
import com.app.entity.Utilisateur;
import com.app.repository.RoleRepository;
import com.app.repository.UtilisateurRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UtilisateurService {

    private final UtilisateurRepository utilisateurRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional(readOnly = true)
    public List<UtilisateurDTO> getAll() {
        return utilisateurRepository.findAll().stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public UtilisateurDTO getById(Long id) {
        return utilisateurRepository.findById(id)
            .map(this::toDTO)
            .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé: " + id));
    }

    @Transactional
    public UtilisateurDTO createUtilisateur(UtilisateurDTO dto) {
        Utilisateur utilisateur = Utilisateur.builder()
            .nom(dto.getNom())
            .email(dto.getEmail())
            .motDePasse(passwordEncoder.encode(dto.getMotDePasse()))
            .actif(dto.isActif())
            .build();
        if (dto.getRoleId() != null) {
            roleRepository.findById(dto.getRoleId()).ifPresent(utilisateur::setRole);
        }
        return toDTO(utilisateurRepository.save(utilisateur));
    }

    @Transactional
    public UtilisateurDTO updateUtilisateur(Long id, UtilisateurDTO dto) {
        Utilisateur utilisateur = utilisateurRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé: " + id));
        utilisateur.setNom(dto.getNom());
        utilisateur.setEmail(dto.getEmail());
        utilisateur.setActif(dto.isActif());
        if (dto.getMotDePasse() != null && !dto.getMotDePasse().isBlank()) {
            utilisateur.setMotDePasse(passwordEncoder.encode(dto.getMotDePasse()));
        }
        if (dto.getRoleId() != null) {
            roleRepository.findById(dto.getRoleId()).ifPresent(utilisateur::setRole);
        } else {
            utilisateur.setRole(null);
        }
        return toDTO(utilisateurRepository.save(utilisateur));
    }

    @Transactional
    public UtilisateurDTO assignRole(Long utilisateurId, Long roleId) {
        Utilisateur utilisateur = utilisateurRepository.findById(utilisateurId)
            .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé: " + utilisateurId));
        roleRepository.findById(roleId).ifPresent(utilisateur::setRole);
        return toDTO(utilisateurRepository.save(utilisateur));
    }

    @Transactional
    public void deleteUtilisateur(Long id) {
        utilisateurRepository.deleteById(id);
    }

    public UtilisateurDTO toDTO(Utilisateur u) {
        UtilisateurDTO dto = new UtilisateurDTO();
        dto.setId(u.getId());
        dto.setNom(u.getNom());
        dto.setEmail(u.getEmail());
        dto.setActif(u.isActif());
        if (u.getRole() != null) {
            dto.setRoleId(u.getRole().getId());
            dto.setRoleNom(u.getRole().getNom());
        }
        return dto;
    }
}
