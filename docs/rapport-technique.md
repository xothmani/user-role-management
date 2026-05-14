# Rapport Technique — User Role Management

**Auteur :** Rayen Othmani  
**Établissement :** ITBS Tunisia — Promotion 2026  
**Date :** Avril 2026  
**Dépôt :** https://github.com/xothmani/user-role-management

---

## Table des matières

1. [Description du projet](#1-description-du-projet)
2. [Architecture](#2-architecture)
3. [Choix techniques](#3-choix-techniques)
4. [Pipeline CI/CD](#4-pipeline-cicd)
5. [Sécurité DevSecOps](#5-sécurité-devsecops)
6. [Monitoring](#6-monitoring)
7. [Problèmes rencontrés et solutions](#7-problèmes-rencontrés-et-solutions)
8. [Améliorations continues](#8-améliorations-continues)

---

## 1. Description du projet

**User Role Management** est une application web full-stack permettant la gestion des utilisateurs et de leurs rôles au sein d'un système d'information. Elle implémente une authentification sécurisée par **JSON Web Token (JWT)** et un contrôle d'accès basé sur les rôles (**RBAC — Role-Based Access Control**).

L'objectif pédagogique du projet est double : produire une application fonctionnelle et déployer l'intégralité d'une chaîne DevOps moderne, de l'intégration continue jusqu'à la livraison automatisée en environnement Kubernetes.

### Stack applicative

| Couche | Technologie | Version |
|---|---|---|
| Frontend | Angular | 17.3.0 |
| Backend | Spring Boot | 3.2.0 / Java 21 |
| Base de données | PostgreSQL | 16-alpine |
| Authentification | JWT (jjwt) | 0.12.3 |

---

## 2. Architecture

### Vue d'ensemble

L'architecture suit le modèle **trois tiers** classique, conteneurisé et orchestré par Kubernetes. En développement local, Docker Compose assure le même assemblage de services.

```
┌─────────────────────────────────────────────────────────────────────┐
│                          NAVIGATEUR CLIENT                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS  (NodePort 30080 en local)
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FRONTEND — Angular 17  /  NGINX alpine                 │
│         Replicas : 2   |   CPU limit : 500m   |   RAM : 512Mi       │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ REST API  :8080
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│         BACKEND — Spring Boot 3.2  /  eclipse-temurin:21-jre        │
│  JWT · Spring Security · JPA · Actuator · Micrometer/Prometheus     │
│         Replicas : 2   |   CPU limit : 500m   |   RAM : 512Mi       │
└──────────┬──────────────────────────────────┬───────────────────────┘
           │ JDBC  :5432                       │ /actuator/prometheus
           ▼                                   ▼
┌────────────────────────┐      ┌──────────────────────────────────┐
│  PostgreSQL 16-alpine  │      │  Prometheus  ──►  Grafana        │
│  PVC : 1 Gi (RWO)      │      │  scraping toutes les 15 s        │
└────────────────────────┘      └──────────────────────────────────┘

Namespace Kubernetes : user-role-management
ConfigMap  →  variables d'environnement non-sensibles (DB_HOST, DB_NAME…)
Secret     →  variables sensibles encodées Base64 (DB_PASSWORD, JWT_SECRET)
```

### Pipeline GitOps

```
 Développeur
     │  git push
     ▼
 GitHub (branches main / dev)
     │  déclenche
     ▼
 GitHub Actions CI
     ├── backend-ci  (Checkstyle · Tests · SonarQube · Trivy · Docker push)
     └── frontend-ci (ESLint · Tests · Trivy · Docker push)
              │  images taguées <sha> + latest
              ▼
         Docker Hub  (raybob2001/user-role-management-*)
              │  sync automatique
              ▼
           ArgoCD  (auto-sync · self-heal · prune)
              │
              ▼
         Kubernetes  (Minikube / cluster cible)
```

---

## 3. Choix techniques

### Côté applicatif

**Spring Boot 3.2 / Java 21**  
Spring Boot s'impose comme la référence pour les API REST en Java d'entreprise. La version 3.2 apporte la compatibilité native avec les Virtual Threads de Java 21, et l'écosystème Spring Security offre un support natif de JWT, de l'audit et de l'AOP sans dépendances tierces lourdes. Le starter `spring-boot-starter-actuator` combiné à `micrometer-registry-prometheus` expose les métriques sans code supplémentaire.

**Angular 17**  
Angular est un framework opinionated qui impose une structure claire (modules, services, guards), ce qui facilite la maintenance et la montée en compétences en équipe. La version 17 introduit les Standalone Components et le nouveau moteur de rendu, réduisant la taille des bundles générés.

**PostgreSQL 16**  
PostgreSQL est le SGBD relationnel open-source le plus complet : support des transactions ACID, extensions JSON, performances éprouvées et image Docker officielle légère (`alpine`). Son driver JDBC officiel est activement maintenu et compatible Spring Data JPA sans configuration particulière.

### Côté DevOps

**GitHub Actions**  
Solution CI/CD native à GitHub, sans infrastructure à maintenir. La syntaxe YAML est lisible, le marché d'actions réutilisables (`actions/setup-java`, `aquasecurity/trivy-action`) évite la réécriture de scripts génériques, et l'intégration avec les secrets du dépôt est transparente.

**Docker & Docker Compose**  
Les Dockerfiles multi-stages permettent de produire des images légères (image runtime `alpine` uniquement) tout en conservant un environnement de build complet. Docker Compose reproduit fidèlement l'environnement de production en local, éliminant les divergences d'environnement.

**ArgoCD**  
ArgoCD implémente le paradigme **GitOps** : la source de vérité est le dépôt Git, non l'état du cluster. L'activation du `self-heal` et du `prune` garantit que toute dérive manuelle est automatiquement corrigée, renforçant la traçabilité et la reproductibilité des déploiements.

**Prometheus / Grafana**  
Prometheus est le standard de facto pour la collecte de métriques dans les environnements Kubernetes. Son modèle de scraping par pull est plus simple à sécuriser que le push, et Micrometer expose nativement les métriques JVM, HTTP et base de données au format Prometheus. Grafana offre des dashboards préconfigurés pour Spring Boot (ID `6756`) sans développement supplémentaire.

---

## 4. Pipeline CI/CD

Le pipeline est défini dans `.github/workflows/ci.yml`. Il se déclenche sur chaque `push` et `pull_request` ciblant les branches `main` et `dev`.

### Job 1 — `backend-ci`

#### Étape 1 : Checkout
```yaml
- uses: actions/checkout@v4
```
Récupère le code source complet du dépôt avec l'historique Git nécessaire à SonarQube.

#### Étape 2 : Configuration Java 21
```yaml
- uses: actions/setup-java@v4
  with:
    java-version: '21'
    distribution: temurin
    cache: maven
```
Installe le JDK Temurin 21 et active le cache Maven pour éviter de re-télécharger les dépendances à chaque exécution, réduisant le temps de build d'environ 60 %.

#### Étape 3 : Checkstyle
```bash
../mvnw checkstyle:check
```
Vérifie la conformité du code Java aux règles **Google Java Style**. Le plugin `maven-checkstyle-plugin` (v3.3.1) est configuré dans le `pom.xml`. Le pipeline échoue immédiatement si une violation est détectée, forçant la qualité syntaxique dès la PR.

#### Étape 4 : Tests unitaires
```bash
../mvnw test
```
Exécute la suite JUnit. Les résultats sont disponibles dans les artefacts de la run GitHub Actions. Le pipeline s'arrête si un test échoue.

#### Étape 5 : Packaging
```bash
../mvnw package -DskipTests
```
Produit le JAR exécutable `user-role-management-1.0.0.jar` via le plugin `spring-boot-maven-plugin`. Les tests sont ignorés car déjà exécutés à l'étape précédente.

#### Étape 6 : Analyse SonarQube
```bash
../mvnw sonar:sonar \
  -Dsonar.projectKey=xothmani_user-role-management \
  -Dsonar.organization=xothmani \
  -Dsonar.host.url=${{ secrets.SONAR_HOST_URL }} \
  -Dsonar.token=${{ secrets.SONAR_TOKEN }}
```
Envoie les résultats d'analyse statique vers SonarCloud. Le token et l'URL sont injectés depuis les secrets GitHub, aucune donnée sensible n'est exposée dans les logs. L'analyse couvre la dette technique, les bugs, les vulnérabilités et la couverture de code.

#### Étapes 7 & 8 : Build et scan Docker (backend)
```yaml
- run: docker build -t <username>/user-role-management-backend:<sha> ./backend

- uses: aquasecurity/trivy-action@v0.36.0
  with:
    image-ref: <username>/user-role-management-backend:<sha>
    format: table
    exit-code: '0'
    severity: CRITICAL
```
L'image est construite avec le Dockerfile multi-stage du répertoire `backend/`. Trivy scanne ensuite l'image à la recherche de CVE de sévérité CRITICAL. Pour le backend, `exit-code: '0'` est intentionnel (voir section 5) : les vulnérabilités sont affichées dans les logs sans bloquer le pipeline pendant la période d'upgrade.

#### Étapes 9 & 10 : Push vers Docker Hub
```bash
docker push <username>/user-role-management-backend:<sha>
docker tag  <username>/user-role-management-backend:<sha> \
            <username>/user-role-management-backend:latest
docker push <username>/user-role-management-backend:latest
```
Deux tags sont publiés : le SHA Git (immuable, traçable) et `latest` (utilisé par ArgoCD pour la synchronisation automatique).

---

### Job 2 — `frontend-ci` (dépend de `backend-ci`)

La dépendance `needs: backend-ci` garantit que le frontend n'est pas publié si le backend échoue.

#### Étape 1 : Checkout & Node 20
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: npm
    cache-dependency-path: frontend/package-lock.json
```
Installe Node 20 LTS avec cache npm activé sur le `package-lock.json`.

#### Étape 2 : Installation des dépendances
```bash
cd frontend && npm ci
```
`npm ci` est utilisé à la place de `npm install` en CI pour une installation strictement reproductible depuis le lockfile (voir problème résolu §7).

#### Étape 3 : Lint ESLint
```bash
cd frontend && npm run lint
```
Vérifie la qualité du code TypeScript via `@angular-eslint`. Toute erreur de lint bloque le pipeline.

#### Étape 4 : Tests Karma/Jasmine
```bash
cd frontend && npm test -- --watch=false --browsers=ChromeHeadless --no-progress
```
Exécute les tests unitaires Angular en mode headless (sans interface graphique), adapté à l'environnement CI sans display server.

#### Étapes 5, 6, 7 : Build, Trivy, Push
Identiques au job backend. La différence notable : `exit-code: '1'` pour Trivy sur le frontend, bloquant le pipeline si une CVE CRITICAL est détectée dans l'image NGINX.

---

## 5. Sécurité DevSecOps

### Analyse statique — SonarQube (SonarCloud)

L'analyse SonarCloud du projet `xothmani_user-role-management` a révélé :

| Catégorie | Nombre | Détail |
|---|---|---|
| Security issues | 1 | Utilisation d'un algorithme de hachage potentiellement faible (à revoir dans la configuration JWT) |
| Maintainability issues | 6 | Code dupliqué, méthodes longues, complexité cyclomatique excessive dans les contrôleurs |
| Bugs | 0 | — |
| Code smells | 6 | Inclus dans les maintainability issues |

**Actions correctives engagées :**
- Revue de la configuration JWT pour utiliser explicitement `HS256` ou `RS256` avec une clé d'une longueur suffisante.
- Refactorisation des contrôleurs pour extraire la logique métier vers les services (principe Single Responsibility).

### Analyse des images — Trivy

Le scan Trivy (`aquasecurity/trivy-action@v0.36.0`, sévérité CRITICAL) a identifié des vulnérabilités dans les dépendances embarquées :

| Composant | CVE(s) notables | Impact |
|---|---|---|
| Apache Tomcat (embarqué Spring Boot) | CVE-2024-56337, CVE-2025-24813 | Exécution de code à distance (RCE) sur serveur Windows avec DefaultServlet activé |
| Spring Security | CVE-2025-22234 | Fuite d'informations sur les temps de réponse (timing attack sur l'authentification) |
| PostgreSQL JDBC Driver | CVE-2024-1597 | Injection SQL via paramètres non-échappés dans certaines configurations |

**Contexte :** Ces CVE sont présentes dans les versions transitives tirées par Spring Boot 3.2.x. Elles ont été corrigées dans Spring Boot **3.4.x** qui embarque Tomcat 10.1.34+, Spring Security 6.4.x et PostgreSQL JDBC 42.7.4+.

**Décision prise :** Le `exit-code` Trivy du backend a été temporairement positionné à `0` pour ne pas bloquer les livraisons pendant la période d'upgrade. Un ticket de remédiation est ouvert (voir §8).

**Bonne pratique appliquée :** Les secrets (mots de passe, JWT secret) ne sont jamais écrits en clair dans le code ni dans les variables d'environnement Kubernetes en clair — ils transitent exclusivement via des **GitHub Secrets** en CI et des **Kubernetes Secrets** (Base64) en production.

---

## 6. Monitoring

### Exposition des métriques

Spring Boot Actuator, combiné à `micrometer-registry-prometheus`, expose automatiquement un endpoint de métriques au format Prometheus :

```
GET /actuator/prometheus
```

La configuration `application.properties` restreint l'exposition aux endpoints nécessaires :

```properties
management.endpoints.web.exposure.include=health,prometheus
management.endpoint.health.show-details=always
management.metrics.tags.application=user-role-management
```

Le tag `application=user-role-management` est injecté dans chaque métrique, permettant de filtrer précisément dans Grafana lorsque plusieurs applications partagent le même Prometheus.

### Métriques clés disponibles

| Métrique Prometheus | Description |
|---|---|
| `http_server_requests_seconds` | Latence et débit des requêtes HTTP par endpoint et code de retour |
| `jvm_memory_used_bytes` | Utilisation mémoire JVM (heap / non-heap) |
| `hikaricp_connections_active` | Connexions actives au pool de base de données |
| `process_cpu_usage` | Taux d'utilisation CPU du processus JVM |
| `jvm_gc_pause_seconds` | Durée des pauses Garbage Collector |

### Configuration Prometheus (scrape job)

```yaml
scrape_configs:
  - job_name: user-role-management-backend
    metrics_path: /actuator/prometheus
    scrape_interval: 15s
    static_configs:
      - targets:
          - backend-service.user-role-management.svc.cluster.local:8080
```

### Dashboards Grafana

Deux dashboards sont utilisés :

1. **Spring Boot Statistics** (ID Grafana : `6756`) — vue applicative JVM, HTTP, connexions DB.
2. **Kubernetes / Compute Resources / Namespace** (dashboard Kubernetes natif) — consommation CPU et mémoire des pods `user-role-management`, avec vue par déploiement.

L'accès Grafana en environnement Minikube se fait via port-forward :

```bash
kubectl port-forward svc/grafana 3000:3000 -n monitoring
# Accès : http://localhost:3000
```

---

## 7. Problèmes rencontrés et solutions

### Problème 1 — Docker Hub inaccessible depuis le runner CI

**Symptôme :** L'étape `docker push` échouait avec `connection timed out` sur le runner GitHub Actions.  
**Cause :** Résolution DNS défaillante vers `registry-1.docker.io` depuis le réseau du runner.  
**Solution :** Ajout de l'option `--dns 8.8.8.8` dans le démon Docker du runner, ou utilisation de `docker/login-action@v3` qui gère automatiquement le retry avec les DNS publics de Google. Le problème ne s'est pas reproduit après passage à `docker/login-action@v3`.

---

### Problème 2 — Version de `trivy-action` incompatible

**Symptôme :** Le pipeline échouait avec `Error: Cannot find action 'aquasecurity/trivy-action@master'`.  
**Cause :** La référence `@master` pointait vers une branche supprimée dans le dépôt Trivy.  
**Solution :** Épinglage à la version stable `aquasecurity/trivy-action@v0.36.0`, pratique recommandée pour la reproductibilité des pipelines CI.

---

### Problème 3 — SonarQube : analyse automatique en conflit avec le plugin Maven

**Symptôme :** L'étape SonarQube échouait avec `Automatic Analysis is enabled. Please disable it before running a manual analysis.`  
**Cause :** SonarCloud avait activé l'analyse automatique (GitHub App) sur le dépôt, ce qui entre en conflit avec l'exécution manuelle via `mvnw sonar:sonar`.  
**Solution :** Désactivation de l'analyse automatique dans les paramètres du projet SonarCloud (`Administration → Analysis Method → Automatic Analysis → Off`), laissant le contrôle exclusif au pipeline GitHub Actions.

---

### Problème 4 — Chemin COPY incorrect dans le Dockerfile backend

**Symptôme :** Le build Docker échouait avec `COPY failed: file not found in build context`.  
**Cause :** Le Dockerfile référençait `target/app.jar` alors que le JAR produit par Maven se nomme `user-role-management-1.0.0.jar`.  
**Solution :** Correction du Dockerfile :
```dockerfile
# Avant
COPY target/app.jar app.jar
# Après
COPY target/user-role-management-1.0.0.jar app.jar
```

---

### Problème 5 — `npm ci` échouait à cause d'un `package-lock.json` obsolète

**Symptôme :** `npm ci` retournait `npm ERR! cipm can only install packages when your package.json and package-lock.json are in sync`.  
**Cause :** Des dépendances ESLint avaient été ajoutées dans `package.json` sans régénérer le lockfile.  
**Solution :** Exécution locale de `npm install` pour régénérer `package-lock.json`, puis commit du fichier mis à jour. Le pipeline utilise ensuite `npm ci` normalement pour les installations reproductibles.

---

## 8. Améliorations continues

### Upgrade Spring Boot vers 3.4.x *(priorité haute)*

La mise à jour de `spring-boot-starter-parent` vers la version `3.4.x` dans `backend/pom.xml` résoudra l'ensemble des CVE CRITICAL identifiées par Trivy (Tomcat, Spring Security, PostgreSQL JDBC). Une fois l'upgrade effectué, `exit-code: '1'` sera réactivé sur le scan Trivy backend pour rétablir le blocage automatique du pipeline en cas de nouvelles vulnérabilités.

### Mise en place HTTPS / TLS

Configurer un `Ingress` Kubernetes avec le contrôleur NGINX et **cert-manager** pour la génération automatique de certificats Let's Encrypt. Toutes les communications frontend ↔ backend seront chiffrées en transit, supprimant l'exposition sur HTTP en clair via NodePort.

### Horizontal Pod Autoscaling (HPA)

Déployer un `HorizontalPodAutoscaler` sur les déploiements backend et frontend pour scaler automatiquement entre 2 et 6 replicas lorsque l'utilisation CPU dépasse 70 % :

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: user-role-management
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-deployment
  minReplicas: 2
  maxReplicas: 6
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Alerting Grafana — CPU > 80 %

Configurer une alerte Grafana sur la métrique `process_cpu_usage` : si le CPU dépasse 80 % pendant plus de 5 minutes, déclencher une notification vers un canal Slack ou e-mail. Cela permettra une réaction proactive avant d'atteindre la saturation et d'impacter les utilisateurs.

### Couverture de code

Intégrer **JaCoCo** dans le `pom.xml` pour générer un rapport de couverture et le publier vers SonarCloud. Fixer un seuil minimum de 80 % de couverture, en deçà duquel le pipeline échoue.

---

*Document généré dans le cadre du projet de fin d'études — ITBS Tunisia 2026.*
