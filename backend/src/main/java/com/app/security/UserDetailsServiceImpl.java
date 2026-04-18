package com.app.security;

import com.app.entity.Utilisateur;
import com.app.repository.UtilisateurRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserDetailsServiceImpl implements UserDetailsService {

    private final UtilisateurRepository utilisateurRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        Utilisateur utilisateur = utilisateurRepository.findByEmail(email)
            .orElseThrow(() -> new UsernameNotFoundException("Utilisateur non trouvé: " + email));

        List<GrantedAuthority> authorities = new ArrayList<>();
        if (utilisateur.getRole() != null) {
            authorities.add(new SimpleGrantedAuthority("ROLE_" + utilisateur.getRole().getNom()));
            utilisateur.getRole().getPermissions().forEach(perm ->
                authorities.add(new SimpleGrantedAuthority(perm.getNom()))
            );
        }

        return new User(
            utilisateur.getEmail(),
            utilisateur.getMotDePasse(),
            utilisateur.isActif(),
            true, true, true,
            authorities
        );
    }
}
