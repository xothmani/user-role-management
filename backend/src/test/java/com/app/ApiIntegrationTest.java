package com.app;

import com.app.dto.LoginRequest;
import com.app.dto.PermissionDTO;
import com.app.entity.HistoriqueAction;
import com.app.repository.HistoriqueActionRepository;
import com.app.repository.PermissionRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class ApiIntegrationTest {

    @Autowired MockMvc mockMvc;
    @Autowired ObjectMapper objectMapper;
    @Autowired HistoriqueActionRepository historiqueRepository;
    @Autowired PermissionRepository permissionRepository;

    // ── Helpers ───────────────────────────────────────────────────────────────

    private String obtainAdminToken() throws Exception {
        LoginRequest req = new LoginRequest();
        req.setEmail("admin@app.com");
        req.setMotDePasse("Admin@123");

        String body = mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        return objectMapper.readTree(body).get("token").asText();
    }

    private Long createPermission(String token, String nom, String description) throws Exception {
        PermissionDTO dto = new PermissionDTO();
        dto.setNom(nom);
        dto.setDescription(description);

        String body = mockMvc.perform(post("/api/permissions")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        return objectMapper.readTree(body).get("id").asLong();
    }

    // ── Auth tests ────────────────────────────────────────────────────────────

    @Nested
    class AuthTests {

        @Test
        void login_validCredentials_returns200WithToken() throws Exception {
            LoginRequest req = new LoginRequest();
            req.setEmail("admin@app.com");
            req.setMotDePasse("Admin@123");

            mockMvc.perform(post("/api/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.token").isNotEmpty())
                    .andExpect(jsonPath("$.type").value("Bearer"))
                    .andExpect(jsonPath("$.email").value("admin@app.com"))
                    .andExpect(jsonPath("$.role").value("ADMIN"));
        }

        @Test
        void login_wrongPassword_returns401() throws Exception {
            LoginRequest req = new LoginRequest();
            req.setEmail("admin@app.com");
            req.setMotDePasse("wrongpassword");

            mockMvc.perform(post("/api/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isUnauthorized())
                    .andExpect(jsonPath("$.message").value("Identifiants invalides."));
        }

        @Test
        void login_unknownEmail_returns401() throws Exception {
            LoginRequest req = new LoginRequest();
            req.setEmail("nobody@app.com");
            req.setMotDePasse("Admin@123");

            mockMvc.perform(post("/api/auth/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isUnauthorized());
        }
    }

    // ── GET /api/permissions/{id} tests ───────────────────────────────────────

    @Nested
    class GetPermissionByIdTests {

        private String token;

        @BeforeEach
        void setup() throws Exception {
            token = obtainAdminToken();
        }

        @Test
        void existingId_returns200WithPermission() throws Exception {
            Long id = permissionRepository.findByNom("USER_READ").orElseThrow().getId();

            mockMvc.perform(get("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id").value(id))
                    .andExpect(jsonPath("$.nom").value("USER_READ"));
        }

        @Test
        void nonExistingId_returns404() throws Exception {
            mockMvc.perform(get("/api/permissions/999999")
                            .header("Authorization", "Bearer " + token))
                    .andExpect(status().isNotFound());
        }
    }

    // ── Permission CRUD tests ─────────────────────────────────────────────────

    @Nested
    class PermissionCrudTests {

        private String token;

        @BeforeEach
        void setup() throws Exception {
            token = obtainAdminToken();
        }

        @Test
        void create_returns201WithBody() throws Exception {
            PermissionDTO dto = new PermissionDTO();
            dto.setNom("CRUD_CREATE");
            dto.setDescription("Created in test");

            mockMvc.perform(post("/api/permissions")
                            .header("Authorization", "Bearer " + token)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(dto)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.id").isNumber())
                    .andExpect(jsonPath("$.nom").value("CRUD_CREATE"))
                    .andExpect(jsonPath("$.description").value("Created in test"));
        }

        @Test
        void read_afterCreate_returns200() throws Exception {
            Long id = createPermission(token, "CRUD_READ", "Read test");

            mockMvc.perform(get("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.nom").value("CRUD_READ"));
        }

        @Test
        void update_returns200WithUpdatedFields() throws Exception {
            Long id = createPermission(token, "CRUD_UPDATE_BEFORE", "Original");

            PermissionDTO updated = new PermissionDTO();
            updated.setNom("CRUD_UPDATE_AFTER");
            updated.setDescription("Modified");

            mockMvc.perform(put("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updated)))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.nom").value("CRUD_UPDATE_AFTER"))
                    .andExpect(jsonPath("$.description").value("Modified"));
        }

        @Test
        void delete_returns204_thenGetReturns404() throws Exception {
            Long id = createPermission(token, "CRUD_DELETE", "To be deleted");

            mockMvc.perform(delete("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token))
                    .andExpect(status().isNoContent());

            mockMvc.perform(get("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token))
                    .andExpect(status().isNotFound());
        }

        @Test
        void create_withoutToken_returns401() throws Exception {
            PermissionDTO dto = new PermissionDTO();
            dto.setNom("CRUD_NOAUTH");
            dto.setDescription("No auth");

            mockMvc.perform(post("/api/permissions")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(dto)))
                    .andExpect(status().isUnauthorized());
        }

        @Test
        void create_withInvalidBody_returns400() throws Exception {
            // nom is @NotBlank — send empty string
            PermissionDTO dto = new PermissionDTO();
            dto.setNom("");
            dto.setDescription("Missing name");

            mockMvc.perform(post("/api/permissions")
                            .header("Authorization", "Bearer " + token)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(dto)))
                    .andExpect(status().isBadRequest());
        }
    }

    // ── HistoriqueAction details field tests ──────────────────────────────────

    @Nested
    class HistoriqueDetailsTests {

        private String token;

        @BeforeEach
        void setup() throws Exception {
            token = obtainAdminToken();
        }

        @Test
        void createPermission_auditsDetailsWithCreationAndEntityType() throws Exception {
            PermissionDTO dto = new PermissionDTO();
            dto.setNom("HIST_CREATE");
            dto.setDescription("Audit create test");

            mockMvc.perform(post("/api/permissions")
                            .header("Authorization", "Bearer " + token)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(dto)))
                    .andExpect(status().isCreated());

            HistoriqueAction log = historiqueRepository.findAll().stream()
                    .filter(h -> h.getAction() != null && h.getAction().contains("createPermission"))
                    .findFirst()
                    .orElseThrow(() -> new AssertionError("No audit record for createPermission"));

            assertThat(log.getDetails()).isNotNull();
            assertThat(log.getDetails()).contains("Création");
            assertThat(log.getDetails()).contains("Permission");
        }

        @Test
        void updatePermission_auditsDetailsWithMiseAJourAndEntityId() throws Exception {
            Long id = createPermission(token, "HIST_UPDATE", "Audit update test");

            PermissionDTO updated = new PermissionDTO();
            updated.setNom("HIST_UPDATE_AFTER");
            updated.setDescription("Updated");

            mockMvc.perform(put("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(updated)))
                    .andExpect(status().isOk());

            HistoriqueAction log = historiqueRepository.findAll().stream()
                    .filter(h -> h.getAction() != null && h.getAction().contains("updatePermission"))
                    .findFirst()
                    .orElseThrow(() -> new AssertionError("No audit record for updatePermission"));

            assertThat(log.getDetails()).isNotNull();
            assertThat(log.getDetails()).contains("Mise à jour");
            assertThat(log.getDetails()).contains("Permission");
            assertThat(log.getDetails()).contains("#" + id);
        }

        @Test
        void deletePermission_auditsDetailsWithSuppressionAndEntityId() throws Exception {
            Long id = createPermission(token, "HIST_DELETE", "Audit delete test");

            mockMvc.perform(delete("/api/permissions/" + id)
                            .header("Authorization", "Bearer " + token))
                    .andExpect(status().isNoContent());

            HistoriqueAction log = historiqueRepository.findAll().stream()
                    .filter(h -> h.getAction() != null && h.getAction().contains("deletePermission"))
                    .findFirst()
                    .orElseThrow(() -> new AssertionError("No audit record for deletePermission"));

            assertThat(log.getDetails()).isNotNull();
            assertThat(log.getDetails()).contains("Suppression");
            assertThat(log.getDetails()).contains("Permission");
            assertThat(log.getDetails()).contains("#" + id);
        }
    }
}
