# Changelog

Toutes les modifications notables apportées à ce projet sont documentées ici.  
Suivant la convention [Keep a Changelog](https://keepachangelog.com/fr/).

---

## [Unreleased]
- Changements en cours de développement ou fonctionnalités à venir

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
- Modélisation des arrêts par Markov Chain par ligne
- Attribution automatique des arrêts aux causes racines réelles
- Génération d’événements avec catégorisation mécanique, électrique et process

### Modifié
- README : ajout des KPI et réorganisation des infos de base
- Mock data : simulation réaliste des arrêts par type et durée

### Corrigé
- Correction de la génération des événements `micro_stop` pour refléter les causes réelles 
