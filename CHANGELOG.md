# Changelog

Toutes les modifications notables apportées à ce projet sont documentées ici.  
Suivant la convention [Keep a Changelog](https://keepachangelog.com/fr/).

---

## [Unreleased]

### Ajouté
- Extension du modèle analytique pour intégrer la **dimension qualité**
- Création des tables opérationnelles :
  - `quality_inspection`
  - `quality_event`
  - `quality_defect`
- Création de la dimension analytique :
  - `dim_quality_defect`
- Création de la table de faits :
  - `fact_quality_events`
- Ajout des tables de staging pour ingestion des événements qualité
- Scripts SQL pour le chargement du pipeline qualité

### Modifié
- Refactorisation complète de la structure SQL du projet
- Organisation des scripts selon une architecture **Data Warehouse en couches** :

  OPS → STG → DW

  
- Réorganisation des dossiers :

```bash
sql/
├── ddl
│ ├── ops
│ ├── stg
│ └── dw
├── dml
│ ├── ops
│ ├── stg
│ └── dw
```


- Renumérotation des scripts SQL pour refléter l’ordre d’exécution
- Mise à jour de l’orchestration du pipeline pour supporter la nouvelle structure

### Corrigé
- Nettoyage des anciens scripts ETL devenus obsolètes après la refactorisation

### À venir
- Génération de **mock data pour les événements qualité**
- Intégration complète du pipeline qualité dans le workflow ETL
- Calcul du composant **Quality de l’OEE**
- Ajout des métriques :
  - defect rate
  - good parts
  - scrap
- Extension des dashboards Power BI pour inclure la qualité

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

## [v1.2] - 2026-02-28

### Ajouté
- Release v1.2 - pipeline refactor, reset layer, pre-commit integration


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