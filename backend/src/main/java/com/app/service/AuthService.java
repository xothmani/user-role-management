package com.app.service;

import com.app.dto.JwtResponse;
import com.app.dto.LoginRequest;
import com.app.entity.Utilisateur;
import com.app.repository.UtilisateurRepository;
import com.app.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;
    private final UtilisateurRepository utilisateurRepository;

    public JwtResponse login(LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.getEmail(), request.getMotDePasse())
        );
        SecurityContextHolder.getContext().setAuthentication(authentication);

        String token = jwtUtil.generateToken(request.getEmail());

        String roleName = utilisateurRepository.findByEmail(request.getEmail())
            .map(u -> u.getRole() != null ? u.getRole().getNom() : "")
            .orElse("");

        return new JwtResponse(token, request.getEmail(), roleName);
    }
}
