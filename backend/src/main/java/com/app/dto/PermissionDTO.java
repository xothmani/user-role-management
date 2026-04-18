package com.app.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class PermissionDTO {
    private Long id;

    @NotBlank
    private String nom;

    private String description;
}
