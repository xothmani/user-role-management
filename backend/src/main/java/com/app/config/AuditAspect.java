package com.app.config;

import com.app.entity.HistoriqueAction;
import com.app.entity.Utilisateur;
import com.app.repository.HistoriqueActionRepository;
import com.app.repository.UtilisateurRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class AuditAspect {

    private final HistoriqueActionRepository historiqueRepository;
    private final UtilisateurRepository utilisateurRepository;

    @Pointcut("execution(* com.app.service.UtilisateurService.*(..)) || " +
              "execution(* com.app.service.RoleService.*(..)) || " +
              "execution(* com.app.service.PermissionService.*(..))")
    public void serviceLayer() {}

    @Pointcut("execution(* create*(..)) || execution(* update*(..)) || " +
              "execution(* delete*(..)) || execution(* assign*(..))")
    public void auditableMethods() {}

    @Around("serviceLayer() && auditableMethods()")
    public Object auditAction(ProceedingJoinPoint pjp) throws Throwable {
        Object result = pjp.proceed();

        try {
            String methodName = pjp.getSignature().getName();
            String className = pjp.getTarget().getClass().getSimpleName();
            String actionDescription = className + "." + methodName;

            Authentication auth = SecurityContextHolder.getContext().getAuthentication();
            Utilisateur utilisateur = null;

            if (auth != null && auth.isAuthenticated() && !"anonymousUser".equals(auth.getPrincipal())) {
                String email = auth.getName();
                utilisateur = utilisateurRepository.findByEmail(email).orElse(null);
            }

            HistoriqueAction action = HistoriqueAction.builder()
                .utilisateur(utilisateur)
                .action(actionDescription)
                .details(buildDetails(methodName, className, pjp.getArgs()))
                .date(LocalDateTime.now())
                .build();

            historiqueRepository.save(action);
        } catch (Exception e) {
            log.warn("Failed to log audit action: {}", e.getMessage());
        }

        return result;
    }

    private String buildDetails(String methodName, String className, Object[] args) {
        String entity = className.replace("Service", "");

        Long entityId = null;
        if (args != null) {
            for (Object arg : args) {
                if (arg instanceof Long) {
                    entityId = (Long) arg;
                    break;
                }
            }
        }

        String operation;
        if (methodName.startsWith("create")) operation = "Création";
        else if (methodName.startsWith("update")) operation = "Mise à jour";
        else if (methodName.startsWith("delete")) operation = "Suppression";
        else if (methodName.startsWith("assign")) operation = "Assignation";
        else operation = methodName;

        return entityId != null
            ? operation + " de " + entity + " #" + entityId
            : operation + " de " + entity;
    }
}
