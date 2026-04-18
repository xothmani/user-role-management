package com.app.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.util.List;
import java.util.Set;

@Data
public class RoleDTO {
    private Long id;

    @NotBlank
    private String nom;

    private String description;

    private Set<PermissionDTO> permissions;

    private List<Long> permissionIds;
}
