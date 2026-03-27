# Changelog

Toutes les modifications notables apportées à ce projet sont documentées ici.  
Suivant la convention [Keep a Changelog](https://keepachangelog.com/fr/).

---

## [Unreleased]

### Ajouté
- Introduction de la dimension analytique `dim_event`
  - Centralisation des types d’événements
  - Ajout des attributs :
    - `event_type`
    - `event_category`
    - `is_failure`
    - `is_micro_stop`
    - `is_quality_loss`

- Ajout du catalogue d’événements (`event_catalog.py`)
  - Source unique de vérité pour la classification métier
  - Standardisation des types d’événements dans tout le pipeline

---

### Modifié

#### Modèle Data Warehouse

- Refactorisation de `fact_production_events`
  - Passage à une clé primaire composite :
    ```
    (time_key, machine_key, team_key, organe_element_key, event_key)
    ```
  - Alignement avec le partitionnement (`PARTITION BY time_key`)
  - Intégration de `event_key` (liaison avec `dim_event`)
  - Suppression de la dépendance à `event_id` comme clé principale
  - Ajout de flags analytiques directement dans la fact :
    - `is_failure`
    - `is_micro_stop`
    - `is_quality_loss`

- Mise à jour de `dim_organe_element`
  - Alignement avec le nouveau grain événementiel
  - Amélioration de la cohérence avec les événements de production

---

#### Pipeline événements (STG → OPS → DW)

- Refactorisation de `stg_production_events`
  - Ajout de :
    - `event_type`
    - `cause_category`

- Refactorisation de `ops.production_events`
  - Enrichissement des événements avec :
    - `severity_score`
    - `is_recurrent`
  - Harmonisation de la structure avec le modèle analytique

- Mise à jour des scripts DML :
  - `stg → ops`
  - `ops → dw`
  - Intégration de `dim_event` dans le chargement de la fact

---

#### Simulation & Génération de données

- Mise à jour du moteur de génération d’événements
  - Intégration du catalogue d’événements
  - Amélioration de la cohérence des données générées

- Amélioration du `markov_engine`
  - Simulation plus réaliste des transitions d’état
  - Meilleure distribution des types d’événements

- Mise à jour du pipeline (`pipeline.py`)
  - Support du nouveau modèle événementiel

---

### Amélioré

- Qualité analytique des données
  - Distinction claire entre :
    - pannes (`failure`)
    - micro-arrêts (`micro_stop`)
    - pertes qualité (`quality_loss`)

- Analyse Pareto
  - Possibilité de filtrer par type d’événement
  - Meilleure pertinence métier des KPI downtime

- Compatibilité BI (Power BI)
  - Modèle en étoile plus robuste
  - Grain explicite : **1 ligne = 1 événement**
  - Simplification des mesures DAX

---

### Corrigé

- Erreur PostgreSQL sur table partitionnée :
  - Correction de la contrainte `PRIMARY KEY`
  - Inclusion de `time_key` dans la clé (obligatoire pour partitionnement)

- Correction des duplications potentielles
  - Alignement avec `ON CONFLICT` sur clé composite

---

### À venir

- Ajout de partitions automatiques par période (mois / jour)
- Unification potentielle des événements production + qualité
- Extension du modèle pour analyse avancée OEE :
  - Availability
  - Performance
  - Quality (complète)
- Optimisation des performances sur gros volumes
- Enrichissement des dashboards Power BI :
  - Pareto dynamique par type d’événement
  - Analyse multi-dimensionnelle (machine, équipe, ligne)

---

## [v1.0] - 2026-02-25

### Ajouté
- Base du projet de suivi de performance industrielle
- Génération de mock data réaliste pour les ateliers, lignes et machines
- Modèle opérationnel et tables analytiques pour la BI
- Dashboards Power BI pour suivi OEE et downtime
- README initial détaillé avec contexte, périmètre et pipeline

### Modifié
- N/A

### Corrigé
- N/A

---

## [v1.1] - 2026-02-28

### Ajouté
- Modélisation des arrêts par **Markov Chain** par ligne
- Attribution automatique des arrêts aux causes racines réelles
- Génération d’événements avec catégorisation :
  - mécanique
  - électrique
  - process

---

## [v1.2] - 2026-02-28

### Ajouté
- Release v1.2 - pipeline refactor, reset layer, pre-commit integration

---

## [v1.3] - 2026-03-15

### Ajouté
- Extension du modèle analytique pour intégrer la **dimension qualité dans le calcul de l’OEE**
- Création des tables opérationnelles qualité :
  - `quality_inspection`
  - `quality_event`
  - `quality_defect`
- Création des tables de staging :
  - `stg_quality_events`
  - `stg_quality_inspection`
- Création des tables analytiques :
  - `dim_quality_defect`
  - `fact_quality_events`
- Ajout des scripts ETL pour ingestion des données qualité
- Préparation du pipeline pour l’intégration des événements qualité

### Modifié
- Refactorisation complète de la structure SQL du projet
- Adoption d’une architecture **Data Warehouse en couches**
- README : ajout des KPI et réorganisation des informations
- Mock data : simulation réaliste des arrêts par type et durée

### Corrigé
- Correction de la génération des événements `micro_stop` pour refléter les causes réelles