package com.app.config;

import com.app.entity.Permission;
import com.app.entity.Role;
import com.app.entity.Utilisateur;
import com.app.repository.PermissionRepository;
import com.app.repository.RoleRepository;
import com.app.repository.UtilisateurRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.Set;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataInitializer implements CommandLineRunner {

    private final PermissionRepository permissionRepository;
    private final RoleRepository roleRepository;
    private final UtilisateurRepository utilisateurRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        seedPermissions();
        seedRoles();
        seedAdminUser();
        log.info("Data initialization completed.");
    }

    private void seedPermissions() {
        createPermissionIfAbsent("USER_READ", "Lire les utilisateurs");
        createPermissionIfAbsent("USER_WRITE", "Créer et modifier les utilisateurs");
        createPermissionIfAbsent("ROLE_MANAGE", "Gérer les rôles et permissions");
    }

    private void seedRoles() {
        if (!roleRepository.existsByNom("ADMIN")) {
            Permission userRead = permissionRepository.findByNom("USER_READ").orElseThrow();
            Permission userWrite = permissionRepository.findByNom("USER_WRITE").orElseThrow();
            Permission roleManage = permissionRepository.findByNom("ROLE_MANAGE").orElseThrow();

            Role admin = Role.builder()
                .nom("ADMIN")
                .description("Administrateur avec accès complet")
                .permissions(Set.of(userRead, userWrite, roleManage))
                .build();
            roleRepository.save(admin);
            log.info("Role ADMIN created.");
        }

        if (!roleRepository.existsByNom("USER")) {
            Permission userRead = permissionRepository.findByNom("USER_READ").orElseThrow();

            Role user = Role.builder()
                .nom("USER")
                .description("Utilisateur standard avec accès en lecture")
                .permissions(Set.of(userRead))
                .build();
            roleRepository.save(user);
            log.info("Role USER created.");
        }
    }

    private void seedAdminUser() {
        if (!utilisateurRepository.existsByEmail("admin@app.com")) {
            Role adminRole = roleRepository.findByNom("ADMIN").orElseThrow();
            Utilisateur admin = Utilisateur.builder()
                .nom("Administrateur")
                .email("admin@app.com")
                .motDePasse(passwordEncoder.encode("Admin@123"))
                .role(adminRole)
                .actif(true)
                .build();
            utilisateurRepository.save(admin);
            log.info("Admin user created: admin@app.com / Admin@123");
        }
    }

    private void createPermissionIfAbsent(String nom, String description) {
        if (!permissionRepository.existsByNom(nom)) {
            permissionRepository.save(Permission.builder().nom(nom).description(description).build());
            log.info("Permission created: {}", nom);
        }
    }
}
