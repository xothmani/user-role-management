package com.app.service;

import com.app.dto.PermissionDTO;
import com.app.dto.RoleDTO;
import com.app.entity.Permission;
import com.app.entity.Role;
import com.app.repository.PermissionRepository;
import com.app.repository.RoleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class RoleService {

    private final RoleRepository roleRepository;
    private final PermissionRepository permissionRepository;

    @Transactional(readOnly = true)
    public List<RoleDTO> getAll() {
        return roleRepository.findAll().stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public RoleDTO getById(Long id) {
        return roleRepository.findByIdWithPermissions(id)
            .map(this::toDTO)
            .orElseThrow(() -> new RuntimeException("Rôle non trouvé: " + id));
    }

    @Transactional
    public RoleDTO createRole(RoleDTO dto) {
        Role role = Role.builder()
            .nom(dto.getNom())
            .description(dto.getDescription())
            .build();
        if (dto.getPermissionIds() != null && !dto.getPermissionIds().isEmpty()) {
            Set<Permission> permissions = new HashSet<>(permissionRepository.findAllById(dto.getPermissionIds()));
            role.setPermissions(permissions);
        }
        return toDTO(roleRepository.save(role));
    }

    @Transactional
    public RoleDTO updateRole(Long id, RoleDTO dto) {
        Role role = roleRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Rôle non trouvé: " + id));
        role.setNom(dto.getNom());
        role.setDescription(dto.getDescription());
        if (dto.getPermissionIds() != null) {
            Set<Permission> permissions = new HashSet<>(permissionRepository.findAllById(dto.getPermissionIds()));
            role.setPermissions(permissions);
        }
        return toDTO(roleRepository.save(role));
    }

    @Transactional
    public RoleDTO assignPermissions(Long roleId, List<Long> permissionIds) {
        Role role = roleRepository.findById(roleId)
            .orElseThrow(() -> new RuntimeException("Rôle non trouvé: " + roleId));
        Set<Permission> permissions = new HashSet<>(permissionRepository.findAllById(permissionIds));
        role.setPermissions(permissions);
        return toDTO(roleRepository.save(role));
    }

    @Transactional
    public void deleteRole(Long id) {
        roleRepository.deleteById(id);
    }

    public RoleDTO toDTO(Role r) {
        RoleDTO dto = new RoleDTO();
        dto.setId(r.getId());
        dto.setNom(r.getNom());
        dto.setDescription(r.getDescription());
        if (r.getPermissions() != null) {
            dto.setPermissions(r.getPermissions().stream()
                .map(p -> {
                    PermissionDTO pdto = new PermissionDTO();
                    pdto.setId(p.getId());
                    pdto.setNom(p.getNom());
                    pdto.setDescription(p.getDescription());
                    return pdto;
                })
                .collect(Collectors.toSet()));
        }
        return dto;
    }
}
