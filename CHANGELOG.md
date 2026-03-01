# Changelog

Toutes les modifications notables apportées à ce projet sont documentées ici.  
Suivant la convention [Keep a Changelog](https://keepachangelog.com/fr/).

---

## [Unreleased]
### À venir
- Ajout d’une couche Data Quality (contrôles métier et cohérence référentielle)
- Dockerisation complète du projet (PostgreSQL + exécution pipeline)
- Ajout d’indicateurs industriels avancés : MTBF, MTTR, OEE complet
- Monitoring d’exécution du pipeline (logs et métriques de run)

---

## [v1.2] - 2026-03-01
### Ajouté
- Configuration `pre-commit` pour assurer la qualité automatique du code
- Intégration de `ruff` pour linting et formatage Python
- Documentation pour régénération des dépendances via `pip-compile`
- Séparation structure / reset / run dans la CLI

### Modifié
- Refactorisation du pipeline pour séparation claire :
  - `init` (DDL)
  - `reset` (TRUNCATE)
  - `run` (DML uniquement)
- Suppression des `DROP CASCADE` au profit d’une approche idempotente
- Réorganisation README pour clarifier installation et exécution

### Maintenance
- Application du formatage automatique Ruff sur l’ensemble du code
- Ajout des hooks pre-commit pour garantir cohérence et qualité

---

## [v1.1] - 2026-02-28
### Ajouté
- Modélisation des arrêts par Markov Chain par ligne
- Attribution automatique des arrêts aux causes racines réelles
- Génération d’événements avec catégorisation mécanique, électrique et process

### Modifié
- README : ajout des KPI et réorganisation des infos de base
- Mock data : simulation réaliste des arrêts par type et durée

### Corrigé
- Correction de la génération des événements `micro_stop` pour refléter les causes réelles

---

## [v1.0] - 2026-02-25
### Ajouté
- Base du projet de suivi de performance industrielle
- Génération de mock data réaliste pour les ateliers, lignes et machines
- Modèle opérationnel et tables analytiques pour la BI
- Dashboards Power BI pour suivi OEE et downtime
- README initial détaillé avec contexte, périmètre et pipeline.