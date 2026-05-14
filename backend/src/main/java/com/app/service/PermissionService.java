package com.app.service;

import com.app.dto.PermissionDTO;
import com.app.entity.Permission;
import com.app.repository.PermissionRepository;
import com.app.repository.RoleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class PermissionService {

    private final PermissionRepository permissionRepository;
    private final RoleRepository roleRepository;

    @Transactional(readOnly = true)
    public List<PermissionDTO> getAll() {
        return permissionRepository.findAll().stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public PermissionDTO getById(Long id) {
        return permissionRepository.findById(id)
            .map(this::toDTO)
            .orElseThrow(() -> new RuntimeException("Permission non trouvée: " + id));
    }

    @Transactional
    public PermissionDTO createPermission(PermissionDTO dto) {
        Permission permission = Permission.builder()
            .nom(dto.getNom())
            .description(dto.getDescription())
            .build();
        return toDTO(permissionRepository.save(permission));
    }

    @Transactional
    public PermissionDTO updatePermission(Long id, PermissionDTO dto) {
        Permission permission = permissionRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Permission non trouvée: " + id));
        permission.setNom(dto.getNom());
        permission.setDescription(dto.getDescription());
        return toDTO(permissionRepository.save(permission));
    }

    @Transactional
    public void deletePermission(Long id) {
        // Remove from every role's permission set to clear role_permissions rows first,
        // otherwise PostgreSQL raises a FK constraint violation.
        roleRepository.findByPermissionsId(id)
            .forEach(role -> role.getPermissions().removeIf(p -> p.getId().equals(id)));
        permissionRepository.deleteById(id);
    }

    public PermissionDTO toDTO(Permission p) {
        PermissionDTO dto = new PermissionDTO();
        dto.setId(p.getId());
        dto.setNom(p.getNom());
        dto.setDescription(p.getDescription());
        return dto;
    }
}
