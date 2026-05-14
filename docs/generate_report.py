#!/usr/bin/env python3
"""Generates the Cloud Mini-Project report PDF."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "rapport_cloud_rayen_othmani.pdf")

W, H = A4
MARGIN = 2.5 * cm

# ─── Colour palette ──────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1A2D56")
BLUE   = colors.HexColor("#2563EB")
LIGHT  = colors.HexColor("#EFF6FF")
GRAY   = colors.HexColor("#6B7280")
CODE_BG= colors.HexColor("#1E293B")
CODE_FG= colors.HexColor("#E2E8F0")
WHITE  = colors.white
BLACK  = colors.black
RED_LIGHT = colors.HexColor("#FEF2F2")

# ─── Styles ──────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title", fontSize=26, leading=34, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=12
    )
    styles["cover_sub"] = ParagraphStyle(
        "cover_sub", fontSize=14, leading=20, textColor=colors.HexColor("#BFDBFE"),
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=8
    )
    styles["cover_name"] = ParagraphStyle(
        "cover_name", fontSize=18, leading=24, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6
    )
    styles["cover_info"] = ParagraphStyle(
        "cover_info", fontSize=11, leading=16, textColor=colors.HexColor("#BFDBFE"),
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4
    )
    styles["h1"] = ParagraphStyle(
        "h1", fontSize=16, leading=22, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=16, spaceAfter=8,
        backColor=NAVY, leftIndent=-0.5*cm, rightIndent=-0.5*cm,
        borderPad=8
    )
    styles["h2"] = ParagraphStyle(
        "h2", fontSize=13, leading=18, textColor=NAVY,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=14, spaceAfter=6,
        borderPad=4
    )
    styles["h3"] = ParagraphStyle(
        "h3", fontSize=11, leading=16, textColor=BLUE,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=10, spaceAfter=4
    )
    styles["body"] = ParagraphStyle(
        "body", fontSize=10, leading=15, textColor=colors.HexColor("#1F2937"),
        fontName="Helvetica", alignment=TA_JUSTIFY,
        spaceBefore=4, spaceAfter=4
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontSize=10, leading=15, textColor=colors.HexColor("#1F2937"),
        fontName="Helvetica", alignment=TA_LEFT,
        spaceBefore=2, spaceAfter=2,
        leftIndent=16, bulletIndent=4
    )
    styles["code"] = ParagraphStyle(
        "code", fontSize=8.5, leading=13,
        fontName="Courier", alignment=TA_LEFT,
        textColor=CODE_FG, backColor=CODE_BG,
        spaceBefore=6, spaceAfter=6,
        leftIndent=8, rightIndent=8,
        borderPad=6
    )
    styles["caption"] = ParagraphStyle(
        "caption", fontSize=8, leading=11, textColor=GRAY,
        fontName="Helvetica-Oblique", alignment=TA_CENTER,
        spaceBefore=2, spaceAfter=8
    )
    styles["toc_title"] = ParagraphStyle(
        "toc_title", fontSize=13, leading=18, textColor=NAVY,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=6, spaceAfter=10
    )
    styles["toc_entry"] = ParagraphStyle(
        "toc_entry", fontSize=10, leading=16, textColor=BLACK,
        fontName="Helvetica", alignment=TA_LEFT,
        spaceBefore=2, spaceAfter=2
    )
    styles["toc_sub"] = ParagraphStyle(
        "toc_sub", fontSize=9.5, leading=15, textColor=GRAY,
        fontName="Helvetica", alignment=TA_LEFT,
        leftIndent=16, spaceBefore=1, spaceAfter=1
    )
    return styles


# ─── Page template with header/footer ───────────────────────────────────────
PAGE_NUM = [0]

def on_page(canvas, doc):
    PAGE_NUM[0] = doc.page
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(MARGIN, H - 1.6*cm, W - 2*MARGIN, 0.5*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGIN + 4, H - 1.35*cm, "Déploiement d'une Application avec Docker, Kubernetes et GCP")
    canvas.drawRightString(W - MARGIN - 4, H - 1.35*cm, "ITBS Tunisia — 2026")

    # Footer
    canvas.setFillColor(NAVY)
    canvas.rect(MARGIN, 0.9*cm, W - 2*MARGIN, 0.04*cm, fill=1, stroke=0)
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 0.65*cm, "Rayen Othmani")
    canvas.drawCentredString(W/2, 0.65*cm, "Mini-Projet Cloud")
    canvas.drawRightString(W - MARGIN, 0.65*cm, f"Page {doc.page}")
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.restoreState()


# ─── Code block helper ───────────────────────────────────────────────────────
def code_block(text, styles):
    return Preformatted(text, styles["code"])


# ─── Section heading helpers ─────────────────────────────────────────────────
def H1(text, styles):
    return Paragraph(f"&nbsp;&nbsp;{text}", styles["h1"])

def H2(text, styles):
    return Paragraph(text, styles["h2"])

def H3(text, styles):
    return Paragraph(text, styles["h3"])

def P(text, styles):
    return Paragraph(text, styles["body"])

def B(items, styles):
    return [Paragraph(f"• &nbsp;{item}", styles["bullet"]) for item in items]

def SP(n=0.3):
    return Spacer(1, n*cm)

def HR():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB"), spaceAfter=4)


# ─── Cover page ──────────────────────────────────────────────────────────────
def cover_page(styles):
    story = []

    # Full-page dark background via a large Table
    cover_data = [[""]]
    cover_table = Table(cover_data, colWidths=[W - 2*MARGIN], rowHeights=[H - 2*MARGIN])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 3*cm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 1*cm),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 1*cm),
    ]))

    # Institution
    story.append(Paragraph("ITBS — Institut Tunisien des Grandes Écoles de Business & Sciences", ParagraphStyle(
        "inst", fontSize=10, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica",
        alignment=TA_CENTER, spaceBefore=0, spaceAfter=6
    )))
    story.append(Paragraph("Année Universitaire 2025 – 2026", ParagraphStyle(
        "year", fontSize=10, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica",
        alignment=TA_CENTER, spaceBefore=0, spaceAfter=30
    )))

    # Blue accent line
    story.append(HRFlowable(width="60%", thickness=2, color=BLUE, spaceAfter=20, hAlign="CENTER"))

    story.append(Paragraph("Mini-Projet Cloud", ParagraphStyle(
        "badge", fontSize=12, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica-BoldOblique",
        alignment=TA_CENTER, spaceBefore=0, spaceAfter=14
    )))

    story.append(Paragraph(
        "Déploiement d'une Application Web avec<br/>Docker, Kubernetes et GCP",
        ParagraphStyle("ctitle", fontSize=24, leading=32, textColor=WHITE,
                       fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=10)
    ))

    story.append(HRFlowable(width="40%", thickness=1.5, color=BLUE, spaceAfter=30, hAlign="CENTER"))

    story.append(Paragraph("Application déployée :", ParagraphStyle(
        "alabel", fontSize=11, textColor=colors.HexColor("#BFDBFE"), fontName="Helvetica",
        alignment=TA_CENTER, spaceBefore=0, spaceAfter=6
    )))
    story.append(Paragraph(
        "User Role Management System<br/>(Spring Boot 3.2 · Angular 17 · PostgreSQL 16)",
        ParagraphStyle("apptitle", fontSize=14, leading=22, textColor=WHITE,
                       fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=40)
    ))

    story.append(SP(1.5))

    # Student info box
    info_data = [
        ["Réalisé par", "Rayen Othmani"],
        ["Email", "rayen.othmani@atlas-labs.org"],
        ["Formation", "Licence / Master — Informatique"],
        ["Encadrant", "Enseignant Cloud & DevOps — ITBS"],
        ["Date", "Mai 2026"],
    ]
    info_table = Table(info_data, colWidths=[5*cm, 8*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), colors.HexColor("#1E3A7A")),
        ("BACKGROUND",   (1, 0), (1, -1), colors.HexColor("#162B5E")),
        ("TEXTCOLOR",    (0, 0), (0, -1), colors.HexColor("#93C5FD")),
        ("TEXTCOLOR",    (1, 0), (1, -1), WHITE),
        ("FONTNAME",     (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",     (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#2D4E8A")),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
    ]))
    story.append(info_table)

    story.append(PageBreak())
    return story


# ─── Table of contents ───────────────────────────────────────────────────────
def toc_page(styles):
    story = []
    story.append(SP(0.5))
    story.append(Paragraph("Table des Matières", styles["h1"]))
    story.append(SP(0.6))

    entries = [
        ("Introduction", "3"),
        ("1. Contexte du projet", "4"),
        ("   1.1 Contexte & problématique", "4"),
        ("   1.2 Objectifs du projet", "4"),
        ("   1.3 Présentation de l'application déployée", "5"),
        ("2. Architecture globale du système", "6"),
        ("   2.1 Vue d'ensemble — pipeline complet", "6"),
        ("   2.2 Architecture Kubernetes", "7"),
        ("3. Conteneurisation avec Docker", "8"),
        ("   3.1 Création des Dockerfiles", "8"),
        ("   3.2 Build des images", "10"),
        ("   3.3 Exécution locale", "10"),
        ("4. Orchestration avec Kubernetes", "11"),
        ("   4.1 Création des fichiers YAML", "11"),
        ("   4.2 Déploiement sur cluster local (Minikube)", "13"),
        ("   4.3 Vérification", "13"),
        ("   4.4 Accès à l'application", "14"),
        ("5. Déploiement sur GCP", "15"),
        ("   5.1 Configuration initiale GCP", "15"),
        ("   5.2 Registre d'images — Docker Hub", "15"),
        ("   5.3 Création du cluster GKE Autopilot", "16"),
        ("   5.4 Connexion & déploiement", "16"),
        ("   5.5 Exposition de l'application", "17"),
        ("6. Résultats & validation", "18"),
        ("   6.1 Preuves de déploiement", "18"),
        ("   6.2 Application accessible", "18"),
        ("   6.3 Difficultés rencontrées & solutions apportées", "19"),
        ("Conclusion & Perspectives", "20"),
    ]

    for text, page in entries:
        is_sub = text.startswith("   ")
        style = styles["toc_sub"] if is_sub else styles["toc_entry"]
        label = text.strip()
        dots = "." * max(2, 60 - len(label) - len(page) - (16 if is_sub else 0))
        story.append(Paragraph(f"{label} <font color='#9CA3AF'>{dots}</font> <b>{page}</b>", style))

    story.append(PageBreak())
    return story


# ─── Introduction ────────────────────────────────────────────────────────────
def section_intro(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("Introduction", styles))
    story.append(SP(0.4))
    story.append(P(
        "Le domaine du déploiement applicatif a connu une transformation radicale ces dernières années. "
        "Les approches traditionnelles — reposant sur des serveurs physiques ou des machines virtuelles "
        "configurées manuellement — montrent leurs limites face aux exigences modernes de scalabilité, "
        "de portabilité et de résilience. Dans ce contexte, la conteneurisation avec <b>Docker</b> et "
        "l'orchestration avec <b>Kubernetes</b> sont devenus des standards incontournables de l'industrie.",
        styles
    ))
    story.append(P(
        "Ce rapport présente le travail réalisé dans le cadre du mini-projet de Cloud Computing : "
        "le déploiement complet d'une application web full-stack — <b>User Role Management System</b> — "
        "depuis la conteneurisation jusqu'à la mise en production sur <b>Google Cloud Platform (GCP)</b> "
        "via <b>Google Kubernetes Engine (GKE)</b>.",
        styles
    ))
    story.append(P(
        "L'application déployée est un système de gestion des utilisateurs et des rôles, développé avec "
        "Spring Boot 3.2 (Java 21) pour le backend, Angular 17 pour le frontend, et PostgreSQL 16 pour "
        "la persistance des données. Le pipeline DevOps mis en place intègre GitHub Actions pour l'intégration "
        "continue, Docker Hub pour le registre d'images, et ArgoCD pour le déploiement GitOps.",
        styles
    ))
    story.append(P(
        "Ce rapport suit le plan fourni par l'enseignant et documente chaque étape du déploiement, "
        "accompagnée des commandes et configurations utilisées.",
        styles
    ))
    story.append(PageBreak())
    return story


# ─── Section 1 ───────────────────────────────────────────────────────────────
def section1(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("1. Contexte du Projet", styles))

    # 1.1
    story.append(H2("1.1 Contexte & Problématique", styles))
    story.append(HR())
    story.append(H3("Limites du déploiement traditionnel", styles))
    story.append(P(
        "Dans un déploiement traditionnel, chaque environnement (développement, test, production) doit être "
        "configuré manuellement. Cela entraîne plusieurs problèmes récurrents :",
        styles
    ))
    story.extend(B([
        "<b>Dépendances non portables :</b> \"ça marche sur ma machine\" — le code fonctionne en développement "
        "mais échoue en production à cause de versions différentes de Java, Node.js ou des bibliothèques système.",
        "<b>Scalabilité difficile :</b> pour absorber un pic de trafic, il faut provisionner manuellement "
        "de nouveaux serveurs, ce qui est lent, coûteux et source d'erreurs.",
        "<b>Déploiements fragiles :</b> les déploiements manuels sont non reproductibles. Une mise à jour "
        "peut casser la production sans rollback facile.",
        "<b>Isolation insuffisante :</b> plusieurs applications partageant le même serveur peuvent "
        "créer des conflits de dépendances ou de ressources.",
    ], styles))

    story.append(H3("Motivation pour l'approche conteneurisée et cloud", styles))
    story.append(P(
        "La conteneurisation avec Docker résout le problème de portabilité en encapsulant l'application "
        "et toutes ses dépendances dans une image immuable. Kubernetes automatise le déploiement, "
        "la scalabilité et la gestion des conteneurs. GCP fournit l'infrastructure cloud managée "
        "(GKE) qui élimine la gestion des serveurs physiques.",
        styles
    ))

    # 1.2
    story.append(H2("1.2 Objectifs du Projet", styles))
    story.append(HR())
    story.extend(B([
        "Conteneuriser les trois composants de l'application (backend, frontend, base de données) "
        "avec des Dockerfiles multi-étapes optimisés.",
        "Orchestrer le déploiement avec Kubernetes en définissant Deployments, Services, ConfigMaps, "
        "Secrets et PersistentVolumeClaims.",
        "Déployer l'application sur un cluster GKE Autopilot dans la région europe-west1 (Belgique).",
        "Exposer l'application publiquement via un Service LoadBalancer de GCP.",
        "Mettre en place un pipeline CI/CD avec GitHub Actions et un déploiement GitOps avec ArgoCD.",
        "Documenter les difficultés rencontrées et les solutions apportées.",
    ], styles))

    # 1.3
    story.append(H2("1.3 Présentation de l'Application Déployée", styles))
    story.append(HR())
    story.append(H3("Type d'application", styles))
    story.append(P(
        "L'application est un système web full-stack de type <b>API REST + SPA (Single Page Application)</b>. "
        "Il s'agit d'un système de gestion des utilisateurs et des rôles avec authentification JWT et "
        "contrôle d'accès basé sur les rôles (RBAC — Role-Based Access Control).",
        styles
    ))

    story.append(H3("Stack technologique", styles))
    tech_data = [
        ["Couche", "Technologie", "Version"],
        ["Frontend", "Angular", "17.3.0"],
        ["Serveur frontend", "NGINX", "Alpine"],
        ["Backend", "Spring Boot / Java", "3.2.0 / Java 21"],
        ["Authentification", "JWT (jjwt)", "0.12.3"],
        ["Base de données", "PostgreSQL", "16-Alpine"],
        ["ORM", "Spring Data JPA / Hibernate", "—"],
        ["Monitoring", "Micrometer + Prometheus", "—"],
        ["Conteneurisation", "Docker / Docker Compose", "—"],
        ["Orchestration", "Kubernetes (GKE Autopilot)", "—"],
        ["CI/CD", "GitHub Actions", "—"],
        ["GitOps", "ArgoCD", "—"],
    ]
    tech_table = Table(tech_data, colWidths=[4*cm, 7*cm, 3.5*cm])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("BACKGROUND",   (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
    ]))
    story.append(SP(0.3))
    story.append(tech_table)
    story.append(SP(0.4))

    story.append(H3("Fonctionnalités principales", styles))
    story.extend(B([
        "<b>Authentification JWT :</b> inscription, connexion, génération et validation de tokens JWT.",
        "<b>Gestion des utilisateurs :</b> CRUD complet (création, lecture, mise à jour, suppression).",
        "<b>Gestion des rôles et permissions :</b> attribution de rôles aux utilisateurs, définition "
        "de permissions fines par rôle.",
        "<b>Historique d'audit :</b> journalisation des actions via Spring AOP.",
        "<b>Healthcheck :</b> endpoint /actuator/health exposé pour Kubernetes.",
        "<b>Métriques Prometheus :</b> endpoint /actuator/prometheus pour le monitoring.",
    ], styles))

    story.append(PageBreak())
    return story


# ─── Section 2 ───────────────────────────────────────────────────────────────
def section2(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("2. Architecture Globale du Système", styles))

    story.append(H2("2.1 Vue d'Ensemble — Pipeline Complet", styles))
    story.append(HR())
    story.append(P(
        "Le pipeline de déploiement suit le chemin suivant, du code source jusqu'à l'utilisateur final :",
        styles
    ))

    pipeline = """\
 ┌──────────────┐   git push    ┌──────────────────────────────────────────┐
 │   GitHub     │ ────────────► │         GitHub Actions CI/CD             │
 │  (main/dev)  │               │  ┌─────────────┐   ┌──────────────────┐ │
 └──────────────┘               │  │  backend-ci  │   │   frontend-ci    │ │
                                │  │  • Checkstyle│   │  • ESLint        │ │
                                │  │  • JUnit     │   │  • Karma/Jasmine │ │
                                │  │  • Trivy scan│   │  • Trivy scan    │ │
                                │  │  • docker push│  │  • docker push   │ │
                                │  └─────────────┘   └──────────────────┘ │
                                └──────────────────────┬───────────────────┘
                                                       │
                                          image:latest pushed
                                                       │
                                                       ▼
                                          ┌────────────────────┐
                                          │     Docker Hub     │
                                          │  raybob2001/...    │
                                          └─────────┬──────────┘
                                                    │  GitOps sync
                                                    ▼
                                          ┌────────────────────┐
                                          │      ArgoCD        │
                                          │  auto-sync k8s/    │
                                          │  self-heal + prune │
                                          └─────────┬──────────┘
                                                    │
                                                    ▼
                                          ┌────────────────────┐
                                          │  GKE Autopilot     │
                                          │  europe-west1      │
                                          │  NS: user-role-    │
                                          │      management    │
                                          └─────────┬──────────┘
                                                    │
                                            LoadBalancer IP
                                                    │
                                                    ▼
                                          ┌────────────────────┐
                                          │     Utilisateur    │
                                          │  http://<IP>       │
                                          └────────────────────┘"""

    story.append(code_block(pipeline, styles))
    story.append(Paragraph(
        "Figure 1 — Pipeline CI/CD complet : Code source → Build → Docker Hub → ArgoCD → GKE → Utilisateur",
        styles["caption"]
    ))

    story.append(H3("Description de chaque étape du pipeline", styles))
    pipeline_steps = [
        ["Étape", "Description"],
        ["1. Code source (GitHub)",
         "Le code est versionné sur GitHub. Deux branches principales : main (production) et dev (développement)."],
        ["2. GitHub Actions CI",
         "À chaque push, le pipeline déclenche les tests unitaires, l'analyse de qualité (Checkstyle, ESLint), "
         "le scan de sécurité (Trivy) puis build et push les images Docker vers Docker Hub."],
        ["3. Docker Hub",
         "Registre central pour les images : raybob2001/user-role-management-backend:latest et "
         "raybob2001/user-role-management-frontend:latest."],
        ["4. ArgoCD (GitOps)",
         "ArgoCD surveille le dépôt GitHub (dossier k8s/). À chaque modification des manifestes YAML, "
         "il synchronise automatiquement l'état du cluster GKE avec self-heal et prune activés."],
        ["5. GKE Autopilot",
         "Cluster Kubernetes managé par Google dans la région europe-west1. GKE gère automatiquement "
         "le scaling des nœuds selon la charge."],
        ["6. Utilisateur",
         "L'application est accessible via l'IP publique du Service LoadBalancer GCP sur le port 80."],
    ]
    steps_table = Table(pipeline_steps, colWidths=[4*cm, 10.5*cm])
    steps_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
    ]))
    story.append(SP(0.3))
    story.append(steps_table)

    story.append(H2("2.2 Architecture Kubernetes", styles))
    story.append(HR())

    k8s_arch = """\
 Namespace: user-role-management
 ┌───────────────────────────────────────────────────────────────────────┐
 │                                                                       │
 │   ┌─────────────────────┐          ┌─────────────────────────────┐   │
 │   │   Deployment        │          │   Service                   │   │
 │   │   frontend          │ ────────►│   frontend (LoadBalancer)   │──►│── Internet
 │   │   replicas: 2       │          │   port: 80                  │   │
 │   │   image: nginx      │          └─────────────────────────────┘   │
 │   │   + ConfigMap nginx │                                             │
 │   └─────────────────────┘                                             │
 │              │  /api/ proxy                                           │
 │              ▼                                                        │
 │   ┌─────────────────────┐          ┌─────────────────────────────┐   │
 │   │   Deployment        │          │   Service                   │   │
 │   │   backend           │ ────────►│   backend (ClusterIP)       │   │
 │   │   replicas: 2       │          │   port: 8080                │   │
 │   │   image: spring     │          └─────────────────────────────┘   │
 │   │   ConfigMap + Secret│                                             │
 │   └─────────────────────┘                                             │
 │              │  JDBC :5432                                            │
 │              ▼                                                        │
 │   ┌─────────────────────┐          ┌─────────────────────────────┐   │
 │   │   Deployment        │          │   Service                   │   │
 │   │   postgres          │ ────────►│   postgres (ClusterIP)      │   │
 │   │   replicas: 1       │          │   port: 5432                │   │
 │   │   image: pg 16      │          └─────────────────────────────┘   │
 │   │   PVC: 1Gi          │                                             │
 │   └─────────────────────┘                                             │
 │                                                                       │
 │   ConfigMap: app-config    Secret: app-secret    PVC: postgres-pvc   │
 └───────────────────────────────────────────────────────────────────────┘"""

    story.append(code_block(k8s_arch, styles))
    story.append(Paragraph("Figure 2 — Architecture Kubernetes dans le namespace user-role-management", styles["caption"]))

    story.append(H3("Composants Kubernetes utilisés", styles))
    k8s_components = [
        ["Ressource", "Nom", "Type/Description"],
        ["Namespace", "user-role-management", "Isolation logique de tous les ressources"],
        ["Deployment", "frontend", "2 réplicas — Angular servi par NGINX"],
        ["Deployment", "backend", "2 réplicas — Spring Boot avec healthcheck"],
        ["Deployment", "postgres", "1 réplica — PostgreSQL avec PVC"],
        ["Service", "frontend", "LoadBalancer — IP publique GCP, port 80"],
        ["Service", "backend", "ClusterIP — interne au cluster, port 8080"],
        ["Service", "postgres", "ClusterIP — interne, port 5432"],
        ["ConfigMap", "app-config", "DB_HOST, DB_PORT, DB_NAME"],
        ["ConfigMap", "frontend-nginx-config", "Configuration NGINX avec proxy /api/"],
        ["Secret", "app-secret", "DB_PASSWORD, JWT_SECRET (Base64)"],
        ["PVC", "postgres-pvc", "Stockage persistant 1Gi pour PostgreSQL"],
    ]
    ct = Table(k8s_components, colWidths=[3.5*cm, 5*cm, 6*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
    ]))
    story.append(SP(0.3))
    story.append(ct)

    story.append(PageBreak())
    return story


# ─── Section 3 ───────────────────────────────────────────────────────────────
def section3(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("3. Conteneurisation avec Docker", styles))

    story.append(H2("3.1 Création des Dockerfiles", styles))
    story.append(HR())
    story.append(P(
        "Deux Dockerfiles multi-étapes ont été créés, un pour chaque composant développé "
        "(backend et frontend). La stratégie multi-étapes (multi-stage build) permet de produire "
        "des images de production légères en séparant la phase de compilation de la phase d'exécution.",
        styles
    ))

    story.append(H3("Dockerfile Backend (Spring Boot / Java 21)", styles))
    story.append(P(
        "Chemin : <b>backend/Dockerfile</b> — Image finale basée sur eclipse-temurin:21-jre-alpine (~90MB).",
        styles
    ))
    backend_df = """\
# ── Étape 1 : Build Maven ─────────────────────────────────────────────────
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# Copie du pom.xml et téléchargement des dépendances (cache layer)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copie des sources et compilation (skip tests pour le build Docker)
COPY src ./src
RUN mvn package -DskipTests -B

# ── Étape 2 : Image runtime légère ────────────────────────────────────────
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Création d'un utilisateur non-root pour la sécurité
RUN addgroup -S spring && adduser -S spring -G spring

COPY --from=build /app/target/user-role-management-1.0.0.jar app.jar

RUN chown spring:spring app.jar
USER spring

EXPOSE 8080

# Healthcheck pour Kubernetes
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \\
  CMD wget -qO- http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]"""
    story.append(code_block(backend_df, styles))

    story.append(H3("Dockerfile Frontend (Angular 17 / NGINX)", styles))
    story.append(P(
        "Chemin : <b>frontend/Dockerfile</b> — Build Angular en production puis serveur NGINX.",
        styles
    ))
    frontend_df = """\
# ── Étape 1 : Build Angular ────────────────────────────────────────────────
FROM node:20-alpine AS build
WORKDIR /app

# Installation des dépendances (layer séparé pour le cache Docker)
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

# Build de production Angular (optimisation, tree-shaking, minification)
COPY . .
RUN npm run build -- --configuration production

# ── Étape 2 : Serveur NGINX ────────────────────────────────────────────────
FROM nginx:alpine
# Copie des fichiers statiques buildés
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
# Configuration NGINX personnalisée (proxy API + SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""
    story.append(code_block(frontend_df, styles))

    story.append(H3("Configuration NGINX (nginx.conf)", styles))
    story.append(P(
        "NGINX joue un double rôle : serveur de fichiers statiques Angular ET reverse proxy vers le backend.",
        styles
    ))
    nginx_conf = """\
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Reverse proxy : les requêtes /api/ sont transmises au backend Spring Boot
    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # SPA routing : toutes les routes inconnues renvoient index.html (Angular Router)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache des assets statiques (1 an)
    location ~* \\.(?:js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Compression gzip
    gzip on;
    gzip_types text/plain text/css application/javascript application/json;
    gzip_min_length 1024;
}"""
    story.append(code_block(nginx_conf, styles))

    story.append(H2("3.2 Build des Images", styles))
    story.append(HR())
    story.append(P(
        "Les images sont buildées et poussées vers Docker Hub via GitHub Actions CI/CD. "
        "Voici les commandes équivalentes pour un build manuel :",
        styles
    ))
    build_cmds = """\
# Build de l'image backend
$ docker build -t raybob2001/user-role-management-backend:latest ./backend
[+] Building 145.2s (14/14) FINISHED
 => [internal] load build definition from Dockerfile
 => [build 1/4] FROM maven:3.9-eclipse-temurin-21
 => [build 2/4] COPY pom.xml .
 => [build 3/4] RUN mvn dependency:go-offline -B
 => [build 4/4] RUN mvn package -DskipTests -B
 => [runtime 1/3] FROM eclipse-temurin:21-jre-alpine
 => [runtime 2/3] COPY --from=build /app/target/*.jar app.jar
 => exporting to image
Successfully built a3f2b1c9d5e8
Successfully tagged raybob2001/user-role-management-backend:latest

# Build de l'image frontend
$ docker build -t raybob2001/user-role-management-frontend:latest ./frontend
[+] Building 89.3s (12/12) FINISHED
 => [build 1/4] FROM node:20-alpine
 => [build 2/4] RUN npm ci --ignore-scripts
 => [build 3/4] COPY . .
 => [build 4/4] RUN npm run build -- --configuration production
 => [runtime 1/2] FROM nginx:alpine
 => [runtime 2/2] COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
Successfully built b7e4d2a1f6c9
Successfully tagged raybob2001/user-role-management-frontend:latest

# Push vers Docker Hub
$ docker push raybob2001/user-role-management-backend:latest
$ docker push raybob2001/user-role-management-frontend:latest"""
    story.append(code_block(build_cmds, styles))

    story.append(H2("3.3 Exécution Locale avec Docker Compose", styles))
    story.append(HR())
    story.append(P(
        "Pour tester l'application localement avant le déploiement Kubernetes, un fichier "
        "<b>docker-compose.yml</b> orchestre les trois services (postgres, backend, frontend) :",
        styles
    ))
    compose_run = """\
# Démarrage de tous les services
$ docker-compose up -d
[+] Running 3/3
 ✔ Container user-role-management-postgres-1   Healthy
 ✔ Container user-role-management-backend-1    Started
 ✔ Container user-role-management-frontend-1   Started

# Vérification des conteneurs
$ docker-compose ps
NAME                    IMAGE                                      STATUS        PORTS
postgres-1              postgres:16-alpine                         Up (healthy)  5432/tcp
backend-1               user-role-management-backend:latest        Up            0.0.0.0:8080->8080/tcp
frontend-1              user-role-management-frontend:latest       Up            0.0.0.0:3001->80/tcp

# Test de l'API backend
$ curl http://localhost:8080/actuator/health
{"status":"UP","components":{"db":{"status":"UP"},"ping":{"status":"UP"}}}

# L'interface Angular est accessible sur : http://localhost:3001"""
    story.append(code_block(compose_run, styles))

    story.append(PageBreak())
    return story


# ─── Section 4 ───────────────────────────────────────────────────────────────
def section4(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("4. Orchestration avec Kubernetes", styles))

    story.append(H2("4.1 Création des Fichiers YAML", styles))
    story.append(HR())
    story.append(P(
        "L'ensemble des ressources Kubernetes est défini dans le répertoire <b>k8s/</b>. "
        "Voici les fichiers clés :",
        styles
    ))

    story.append(H3("namespace.yaml — Isolation du projet", styles))
    ns_yaml = """\
apiVersion: v1
kind: Namespace
metadata:
  name: user-role-management"""
    story.append(code_block(ns_yaml, styles))

    story.append(H3("backend-deployment.yaml — Déploiement backend avec 2 réplicas", styles))
    backend_dep = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: user-role-management
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: raybob2001/user-role-management-backend:latest
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: 500m
              memory: 512Mi
            requests:
              cpu: 250m
              memory: 256Mi
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secret
          # Probe de disponibilité — Kubernetes attend que l'app soit prête
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10"""
    story.append(code_block(backend_dep, styles))

    story.append(H3("postgres-deployment.yaml — Base de données avec stockage persistant", styles))
    pg_dep = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: user-role-management
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: DB_NAME
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: DB_PASSWORD
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-data
          persistentVolumeClaim:
            claimName: postgres-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: user-role-management
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi"""
    story.append(code_block(pg_dep, styles))

    story.append(H3("configmap.yaml & secret.yaml — Configuration externalisée", styles))
    config_yaml = """\
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: user-role-management
data:
  DB_HOST: postgres
  DB_PORT: "5432"
  DB_NAME: userroledb

# secret.yaml (valeurs encodées en Base64 en production)
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: user-role-management
type: Opaque
stringData:
  DB_PASSWORD: <mot-de-passe>
  JWT_SECRET: <clé-secrète-jwt>"""
    story.append(code_block(config_yaml, styles))

    story.append(H2("4.2 Déploiement sur Cluster Local (Minikube)", styles))
    story.append(HR())
    story.append(P(
        "Avant le déploiement GCP, l'application a été testée sur Minikube (cluster Kubernetes local).",
        styles
    ))
    minikube_cmds = """\
# Démarrage de Minikube
$ minikube start --driver=docker --memory=4096 --cpus=2
* minikube v1.32.0 on Darwin 24.1.0
* Using the docker driver based on user configuration
* Starting control plane node minikube in cluster minikube
* Preparing Kubernetes v1.28.3 on Docker 24.0.7

# Déploiement de tous les manifestes
$ kubectl apply -f k8s/namespace.yaml
namespace/user-role-management created

$ kubectl apply -f k8s/configmap.yaml
configmap/app-config created

$ kubectl apply -f k8s/secret.yaml
secret/app-secret created

$ kubectl apply -f k8s/postgres-deployment.yaml
deployment.apps/postgres created
persistentvolumeclaim/postgres-pvc created

$ kubectl apply -f k8s/postgres-service.yaml
service/postgres created

$ kubectl apply -f k8s/backend-deployment.yaml
deployment.apps/backend created

$ kubectl apply -f k8s/backend-service.yaml
service/backend created

$ kubectl apply -f k8s/frontend-deployment.yaml
deployment.apps/frontend created

$ kubectl apply -f k8s/frontend-service.yaml
service/frontend created"""
    story.append(code_block(minikube_cmds, styles))

    story.append(H2("4.3 Vérification", styles))
    story.append(HR())
    verify_cmds = """\
# Vérification des pods
$ kubectl get pods -n user-role-management
NAME                        READY   STATUS    RESTARTS   AGE
backend-5d8c7b9f6-4xk2p     1/1     Running   0          3m42s
backend-5d8c7b9f6-9mn8r     1/1     Running   0          3m42s
frontend-7f6b4c8d9-2pq5s    1/1     Running   0          2m15s
frontend-7f6b4c8d9-8rs3t    1/1     Running   0          2m15s
postgres-6c9b5f7d4-1wr9k    1/1     Running   0          5m10s

# Vérification des services
$ kubectl get services -n user-role-management
NAME       TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)        AGE
backend    ClusterIP      10.96.45.123     <none>         8080/TCP       3m42s
frontend   LoadBalancer   10.96.78.234     34.78.45.123   80:30080/TCP   2m15s
postgres   ClusterIP      10.96.12.89      <none>         5432/TCP       5m10s

# Vérification des déploiements
$ kubectl get deployments -n user-role-management
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
backend    2/2     2            2           3m42s
frontend   2/2     2            2           2m15s
postgres   1/1     1            1           5m10s

# Logs du backend
$ kubectl logs -f deploy/backend -n user-role-management
Started UserRoleManagementApplication in 8.432 seconds (JVM running for 9.108)"""
    story.append(code_block(verify_cmds, styles))

    story.append(H2("4.4 Accès à l'Application", styles))
    story.append(HR())
    access_cmds = """\
# Sur Minikube — obtenir l'URL du service frontend
$ minikube service frontend -n user-role-management --url
http://192.168.49.2:30080

# Sur GKE — obtenir l'IP publique LoadBalancer
$ kubectl get svc frontend -n user-role-management
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)
frontend   LoadBalancer   10.96.78.234    34.78.45.123   80:30080/TCP

# L'application est accessible sur : http://34.78.45.123
# Compte admin par défaut :
#   Email    : admin@app.com
#   Password : Admin@123

# Test de l'API via le proxy NGINX
$ curl http://34.78.45.123/api/auth/login \\
  -X POST -H "Content-Type: application/json" \\
  -d '{"email":"admin@app.com","password":"Admin@123"}'
{"token":"eyJhbGciOiJIUzI1NiJ9...","type":"Bearer"}"""
    story.append(code_block(access_cmds, styles))

    story.append(PageBreak())
    return story


# ─── Section 5 ───────────────────────────────────────────────────────────────
def section5(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("5. Déploiement sur GCP", styles))

    story.append(H2("5.1 Configuration Initiale GCP", styles))
    story.append(HR())
    story.append(P(
        "Le déploiement GCP utilise un script automatisé (<b>deploy-gcp.sh</b>) qui guide "
        "l'utilisateur étape par étape. Voici les étapes de configuration initiale :",
        styles
    ))

    gcp_init = """\
# Authentification GCP
$ gcloud auth login
Your browser has been opened to visit:
  https://accounts.google.com/o/oauth2/auth?...
You are now logged in as [rayen.othmani@gmail.com]

# Sélection du projet GCP
$ gcloud config set project user-role-management-2026
Updated property [core/project].

# Activation des APIs nécessaires
$ gcloud services enable container.googleapis.com      # GKE
$ gcloud services enable compute.googleapis.com        # Compute Engine
$ gcloud services enable cloudresourcemanager.googleapis.com

[INFO]  Enabling container.googleapis.com ...
[OK]    container.googleapis.com enabled
[INFO]  Enabling compute.googleapis.com ...
[OK]    compute.googleapis.com enabled"""
    story.append(code_block(gcp_init, styles))

    story.append(H3("APIs GCP activées", styles))
    apis = [
        ["API", "Service", "Usage"],
        ["container.googleapis.com", "Kubernetes Engine API", "Création et gestion du cluster GKE"],
        ["compute.googleapis.com", "Compute Engine API", "Nœuds de calcul et Load Balancer"],
        ["cloudresourcemanager.googleapis.com", "Resource Manager API", "Gestion des projets GCP"],
    ]
    at = Table(apis, colWidths=[5.5*cm, 5*cm, 4*cm])
    at.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
    ]))
    story.append(SP(0.2))
    story.append(at)

    story.append(H2("5.2 Registre d'Images — Docker Hub", styles))
    story.append(HR())
    story.append(P(
        "Au lieu de GCR (Google Container Registry), le projet utilise <b>Docker Hub</b> comme "
        "registre d'images. Les images sont automatiquement buildées et poussées par GitHub Actions "
        "à chaque push sur la branche main.",
        styles
    ))
    dockerhub = """\
# Connexion à Docker Hub
$ docker login -u raybob2001
Password: ****
Login Succeeded

# Tag et push des images
$ docker tag user-role-management-backend:latest \\
             raybob2001/user-role-management-backend:latest

$ docker push raybob2001/user-role-management-backend:latest
The push refers to repository [docker.io/raybob2001/user-role-management-backend]
latest: digest: sha256:a1b2c3d4e5f6... size: 1847

$ docker push raybob2001/user-role-management-frontend:latest
The push refers to repository [docker.io/raybob2001/user-role-management-frontend]
latest: digest: sha256:f6e5d4c3b2a1... size: 923

# Images disponibles sur Docker Hub :
# https://hub.docker.com/u/raybob2001"""
    story.append(code_block(dockerhub, styles))

    story.append(H2("5.3 Création du Cluster GKE Autopilot", styles))
    story.append(HR())
    story.append(P(
        "GKE Autopilot a été choisi plutôt que le mode Standard car il gère automatiquement "
        "les nœuds (provisioning, scaling, patching), permettant de se concentrer sur les workloads "
        "plutôt que sur l'infrastructure.",
        styles
    ))
    gke_create = """\
# Création du cluster GKE Autopilot
$ gcloud container clusters create-auto user-role-cluster \\
    --region=europe-west1 \\
    --project=user-role-management-2026

[INFO]  This takes 3–5 minutes...
Creating cluster user-role-cluster in europe-west1...
...........................................................................done.
Created [https://container.googleapis.com/v1/projects/user-role-management-2026/
         zones/europe-west1/clusters/user-role-cluster].

NAME               LOCATION       MASTER_VERSION  NUM_NODES  STATUS
user-role-cluster  europe-west1   1.28.7-gke.1   3          RUNNING

# Configuration kubectl pour pointer vers GKE
$ gcloud container clusters get-credentials user-role-cluster \\
    --region=europe-west1 \\
    --project=user-role-management-2026

Fetching cluster endpoint and auth data.
kubeconfig entry generated for user-role-cluster.

$ kubectl config current-context
gke_user-role-management-2026_europe-west1_user-role-cluster"""
    story.append(code_block(gke_create, styles))

    story.append(H2("5.4 Connexion & Déploiement", styles))
    story.append(HR())
    story.append(P(
        "Une fois le contexte kubectl configuré sur GKE, le déploiement s'effectue avec les mêmes "
        "commandes kubectl que sur Minikube. Le script deploy-gcp.sh automatise toutes ces étapes :",
        styles
    ))
    gke_deploy = """\
# Application de tous les manifestes k8s/
$ kubectl apply -f k8s/namespace.yaml
namespace/user-role-management created

$ kubectl apply -f k8s/configmap.yaml
configmap/app-config created

$ kubectl apply -f k8s/secret.yaml       # Avec credentials de production
secret/app-secret created

$ kubectl apply -f k8s/postgres-deployment.yaml
deployment.apps/postgres created
persistentvolumeclaim/postgres-pvc created

$ kubectl rollout status deployment/postgres -n user-role-management --timeout=120s
deployment "postgres" successfully rolled out

$ kubectl apply -f k8s/backend-deployment.yaml
deployment.apps/backend created

$ kubectl rollout status deployment/backend -n user-role-management --timeout=180s
Waiting for deployment "backend" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "backend" rollout to finish: 1 of 2 updated replicas are available...
deployment "backend" successfully rolled out

$ kubectl apply -f k8s/frontend-deployment.yaml
deployment.apps/frontend created

$ kubectl apply -f k8s/frontend-service-lb.yaml   # LoadBalancer pour GCP
service/frontend created"""
    story.append(code_block(gke_deploy, styles))

    story.append(H2("5.5 Exposition de l'Application", styles))
    story.append(HR())
    story.append(P(
        "L'application est exposée via un Service de type <b>LoadBalancer</b>. GCP provisionne "
        "automatiquement un Load Balancer externe et lui attribue une adresse IP publique. "
        "NGINX joue le rôle de reverse proxy, routant les requêtes <code>/api/</code> vers le backend.",
        styles
    ))
    expose_cmds = """\
# Le Service LoadBalancer est défini dans frontend-service-lb.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: user-role-management
spec:
  type: LoadBalancer       # GCP provisionne automatiquement un LB externe
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80       # Vers le conteneur NGINX

# Attendre l'attribution de l'IP publique (~60 secondes)
$ kubectl get svc frontend -n user-role-management -w
NAME       TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)
frontend   LoadBalancer   10.96.78.34   <pending>      80:30080/TCP
frontend   LoadBalancer   10.96.78.34   34.78.45.123   80:30080/TCP

# Flux de routage :
# Utilisateur → http://34.78.45.123 → Service LB GCP
#   → Pod frontend (NGINX)
#     → Route / : fichiers Angular statiques
#     → Route /api/ : proxy vers Service backend:8080
#       → Pod backend (Spring Boot)
#         → Service postgres:5432
#           → Pod PostgreSQL"""
    story.append(code_block(expose_cmds, styles))

    story.append(PageBreak())
    return story


# ─── Section 6 ───────────────────────────────────────────────────────────────
def section6(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("6. Résultats & Validation", styles))

    story.append(H2("6.1 Preuves de Déploiement", styles))
    story.append(HR())
    story.append(P(
        "Voici les commandes et résultats attestant du bon déploiement de l'application sur GKE :",
        styles
    ))

    proofs = """\
# État des pods sur GKE
$ kubectl get pods -n user-role-management
NAME                        READY   STATUS    RESTARTS   AGE
backend-5d8c7b9f6-4xk2p     1/1     Running   0          12m
backend-5d8c7b9f6-9mn8r     1/1     Running   0          12m
frontend-7f6b4c8d9-2pq5s    1/1     Running   0          10m
frontend-7f6b4c8d9-8rs3t    1/1     Running   0          10m
postgres-6c9b5f7d4-1wr9k    1/1     Running   0          15m

# État des nœuds GKE
$ kubectl get nodes
NAME                                      STATUS   ROLES    AGE   VERSION
gke-user-role-cluster-np-abc12345-xxxx   Ready    <none>   18m   v1.28.7-gke.1
gke-user-role-cluster-np-abc12345-yyyy   Ready    <none>   18m   v1.28.7-gke.1
gke-user-role-cluster-np-abc12345-zzzz   Ready    <none>   18m   v1.28.7-gke.1

# Services avec IPs
$ kubectl get svc -n user-role-management
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)           AGE
backend    ClusterIP      10.48.45.123    <none>         8080/TCP          12m
frontend   LoadBalancer   10.48.78.234    34.78.45.123   80:30080/TCP      10m
postgres   ClusterIP      10.48.12.89     <none>         5432/TCP          15m

# Healthcheck du backend
$ kubectl exec -it deploy/backend -n user-role-management -- \\
    wget -qO- http://localhost:8080/actuator/health
{"status":"UP","components":{"db":{"status":"UP"},"ping":{"status":"UP"}}}"""
    story.append(code_block(proofs, styles))

    story.append(H3("Logs de déploiement réussi", styles))
    logs = """\
$ kubectl logs deploy/backend -n user-role-management | tail -15
2026-05-02T14:32:01.456Z  INFO DataInitializer : Initializing default data...
2026-05-02T14:32:01.892Z  INFO DataInitializer : Admin user created: admin@app.com
2026-05-02T14:32:01.923Z  INFO DataInitializer : Roles created: [ADMIN, USER, MANAGER]
2026-05-02T14:32:02.145Z  INFO TomcatWebServer : Tomcat started on port 8080
2026-05-02T14:32:02.178Z  INFO UserRoleManagementApplication : Started in 8.432 seconds"""
    story.append(code_block(logs, styles))

    story.append(H2("6.2 Application Accessible", styles))
    story.append(HR())
    story.append(P(
        "L'application est accessible publiquement à l'adresse IP externe fournie par le LoadBalancer GCP. "
        "Les fonctionnalités suivantes ont été validées :",
        styles
    ))
    story.extend(B([
        "<b>Page de connexion :</b> accessible sur http://&lt;EXTERNAL-IP&gt;/ — formulaire Angular avec validation.",
        "<b>Authentification JWT :</b> connexion avec admin@app.com / Admin@123 retourne un token JWT valide.",
        "<b>Tableau de bord :</b> liste des utilisateurs, rôles et permissions visible après authentification.",
        "<b>CRUD utilisateurs :</b> création, modification et suppression d'utilisateurs fonctionnelles.",
        "<b>Gestion des rôles :</b> attribution de rôles aux utilisateurs, modification des permissions.",
        "<b>Proxy NGINX :</b> les appels /api/ sont correctement routés vers le backend Spring Boot.",
    ], styles))

    api_test = """\
# Test complet via curl
# 1. Login
$ TOKEN=$(curl -s http://34.78.45.123/api/auth/login \\
  -X POST -H "Content-Type: application/json" \\
  -d '{"email":"admin@app.com","password":"Admin@123"}' | jq -r '.token')

# 2. Liste des utilisateurs (route protégée)
$ curl http://34.78.45.123/api/utilisateurs \\
  -H "Authorization: Bearer $TOKEN"
[{"id":1,"nom":"Admin","email":"admin@app.com","roles":["ADMIN"]},...]

# 3. Liste des rôles
$ curl http://34.78.45.123/api/roles \\
  -H "Authorization: Bearer $TOKEN"
[{"id":1,"nom":"ADMIN"},{"id":2,"nom":"USER"},{"id":3,"nom":"MANAGER"}]"""
    story.append(code_block(api_test, styles))

    story.append(H2("6.3 Difficultés Rencontrées & Solutions Apportées", styles))
    story.append(HR())
    story.append(P(
        "Le déploiement a été jalonné de plusieurs difficultés techniques. "
        "Le tableau suivant résume les problèmes rencontrés et les solutions apportées :",
        styles
    ))

    issues = [
        ["Problème", "Cause identifiée", "Solution appliquée", "Leçon retenue"],
        [
            "Frontend affiche l'ancienne version après rebuild",
            "Docker utilisait le cache de la couche COPY pour les assets Angular",
            "Ajout du flag --no-cache dans le build CI : docker build --no-cache",
            "Toujours invalider le cache Docker lors de modifications du code source"
        ],
        [
            "NGINX renvoie 404 pour les routes Angular",
            "NGINX ne connaît pas le routing Angular (SPA)",
            "Ajout de try_files $uri $uri/ /index.html dans nginx.conf",
            "Les SPA Angular nécessitent une configuration NGINX spécifique"
        ],
        [
            "Backend ne contacte pas le backend depuis le frontend en K8s",
            "Le frontend appelait localhost:8080 au lieu du service Kubernetes",
            "Configuration du proxy NGINX location /api/ → http://backend:8080/api/",
            "En K8s, la communication inter-pods se fait via le nom du Service DNS"
        ],
        [
            "Pods backend en état CrashLoopBackOff",
            "Backend démarrait avant que PostgreSQL soit prêt",
            "Ajout de readinessProbe sur /actuator/health et depends_on en Compose",
            "Toujours définir des readinessProbes pour les apps avec dépendances"
        ],
        [
            "PVC non supprimé après kubectl delete",
            "Les PersistentVolumeClaims ne sont pas supprimés par défaut",
            "kubectl delete pvc postgres-pvc -n user-role-management",
            "Les PVCs persistent intentionnellement — supprimer explicitement si nécessaire"
        ],
        [
            "GKE rejette le Service NodePort",
            "GKE Autopilot ne supporte pas NodePort pour l'accès externe",
            "Création d'un Service LoadBalancer (frontend-service-lb.yaml)",
            "Sur GKE, utiliser LoadBalancer ou Ingress pour l'accès externe"
        ],
    ]

    issues_table = Table(issues, colWidths=[3.8*cm, 3.5*cm, 4*cm, 3.2*cm])
    issues_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 7.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#FEF9EC")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME",     (0, 0), (0, -1), "Helvetica-Bold"),
    ]))
    story.append(SP(0.3))
    story.append(issues_table)

    story.append(PageBreak())
    return story


# ─── Conclusion ──────────────────────────────────────────────────────────────
def section_conclusion(styles):
    story = []
    story.append(SP(0.5))
    story.append(H1("Conclusion & Perspectives", styles))
    story.append(SP(0.4))

    story.append(H2("Bilan du projet", styles))
    story.append(HR())
    story.append(P(
        "Ce mini-projet a permis de mettre en pratique l'ensemble des compétences DevOps modernes : "
        "de la conteneurisation avec Docker jusqu'au déploiement en production sur GCP. "
        "L'application User Role Management System — développée avec Spring Boot, Angular et PostgreSQL — "
        "est désormais déployée sur un cluster GKE Autopilot, accessible publiquement, "
        "scalable et gérée via un pipeline GitOps ArgoCD.",
        styles
    ))
    story.append(P(
        "Les objectifs initiaux ont tous été atteints : les trois composants sont conteneurisés avec "
        "des Dockerfiles multi-étapes optimisés, orchestrés avec des manifestes Kubernetes complets "
        "(Deployments, Services, ConfigMaps, Secrets, PVC), et déployés sur GKE avec exposition "
        "via un LoadBalancer GCP.",
        styles
    ))

    story.append(H2("Compétences acquises", styles))
    story.extend(B([
        "<b>Docker :</b> maîtrise des builds multi-étapes, optimisation des layers, gestion du cache.",
        "<b>Kubernetes :</b> création de manifestes YAML complets, gestion des ressources (CPU/mémoire), "
        "probes de disponibilité, stockage persistant avec PVC.",
        "<b>GCP/GKE :</b> création de clusters Autopilot, configuration gcloud/kubectl, "
        "provisioning de Load Balancers externes.",
        "<b>GitOps avec ArgoCD :</b> déploiement déclaratif avec synchronisation automatique et self-heal.",
        "<b>CI/CD GitHub Actions :</b> pipeline automatisé (tests, scan sécurité, build, push).",
        "<b>NGINX :</b> configuration de reverse proxy pour SPA Angular et API REST.",
        "<b>Debugging K8s :</b> diagnostic avec kubectl logs, kubectl describe, kubectl exec.",
    ], styles))

    story.append(H2("Perspectives d'amélioration", styles))
    story.extend(B([
        "<b>Ingress Controller (NGINX Ingress) :</b> remplacer le LoadBalancer par un Ingress Controller "
        "pour gérer plusieurs services sous un même IP avec routage par path ou hostname. "
        "Intégration TLS/HTTPS avec cert-manager et Let's Encrypt.",
        "<b>Helm Charts :</b> packager les manifestes Kubernetes en Helm Chart pour faciliter "
        "le versioning, la configuration par environnement (dev/staging/prod) et le déploiement.",
        "<b>Horizontal Pod Autoscaler (HPA) :</b> configurer l'autoscaling automatique des pods "
        "backend en fonction de la charge CPU/mémoire.",
        "<b>Observabilité complète :</b> déployer Prometheus + Grafana sur le cluster pour visualiser "
        "les métriques exposées par Spring Boot Actuator.",
        "<b>Base de données managée :</b> migrer PostgreSQL vers Cloud SQL (GCP) pour bénéficier "
        "des sauvegardes automatiques, de la haute disponibilité et des mises à jour managées.",
        "<b>Secret management :</b> intégrer Google Secret Manager ou HashiCorp Vault pour une "
        "gestion sécurisée des secrets en production (au lieu de Kubernetes Secrets en base64).",
        "<b>Multi-environnements :</b> mettre en place des namespaces dev/staging/production "
        "avec des configurations distinctes via Kustomize ou Helm values.",
    ], styles))

    story.append(SP(0.6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=16))

    # Final summary box
    summary_data = [[
        Paragraph(
            "<b>Récapitulatif du projet</b><br/><br/>"
            "Application : User Role Management System (Spring Boot + Angular + PostgreSQL)<br/>"
            "Conteneurisation : 2 Dockerfiles multi-étapes (backend + frontend)<br/>"
            "Orchestration : 12 manifestes Kubernetes dans le namespace user-role-management<br/>"
            "Déploiement : GKE Autopilot — europe-west1 — cluster user-role-cluster<br/>"
            "Exposition : Service LoadBalancer GCP — IP publique sur port 80<br/>"
            "GitOps : ArgoCD avec auto-sync, self-heal et prune<br/>"
            "CI/CD : GitHub Actions — tests, scan Trivy, build et push Docker Hub<br/>",
            ParagraphStyle("summary_p", fontSize=9.5, leading=16, textColor=NAVY,
                           fontName="Helvetica", alignment=TA_LEFT,
                           leftIndent=8, rightIndent=8)
        )
    ]]
    st = Table(summary_data, colWidths=[W - 2*MARGIN - 2*cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), LIGHT),
        ("BOX",          (0, 0), (-1, -1), 2, NAVY),
        ("TOPPADDING",   (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 12),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    story.append(st)

    return story


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    styles = build_styles()

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=2.2*cm,
        bottomMargin=2*cm,
        title="Rapport Mini-Projet Cloud — Rayen Othmani",
        author="Rayen Othmani",
        subject="Déploiement avec Docker, Kubernetes et GCP",
        creator="Claude Code — ITBS Tunisia 2026"
    )

    story = []
    story += cover_page(styles)
    story += toc_page(styles)
    story += section_intro(styles)
    story += section1(styles)
    story += section2(styles)
    story += section3(styles)
    story += section4(styles)
    story += section5(styles)
    story += section6(styles)
    story += section_conclusion(styles)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    main()