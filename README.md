[![Version](https://img.shields.io/badge/Version-1.0-0066cc?style=flat-square)](#versioning)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37726?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![PowerBI](https://img.shields.io/badge/Power%20BI-Analytics-F2CC8F?style=flat-square&logo=powerbi&logoColor=black)](https://www.microsoft.com/fr-fr/power-platform/products/power-bi)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#licence)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=flat-square)](#)

# Analyse globale des performances du service conditionnement d'une société fromagère industriel

## Objectif du projet
Ce projet vise à mettre en place une **analyse globale, transverse et structurée** de la performance des ateliers de conditionnement industriel, en s’appuyant sur les **feuilles de marche opérateur** et les **compteurs de production**.

L’objectif est de suivre, comparer et analyser :
- l’ensemble des **ateliers**,
- toutes les **lignes et machines**,
- tous les **opérateurs, chefs d’équipe et responsables**,
- l’ensemble des **événements impactant la production**.

Le projet transforme une donnée terrain **manuelle, locale et opérationnelle** en une **vision analytique consolidée**, exploitable pour le **pilotage industriel** et l’**amélioration continue**.



## Table des matières

## 📚 Table des matières
- [Objectif du projet](#objectif-du-projet)
- [Contexte industriel](#contexte-industriel)
- [Source et nature des données](#source-et-nature-des-données)
- [Principe de mesure de la non-production](#principe-de-mesure-de-la-non-production)
- [Périmètre d’analyse](#périmètre-danalyse)
- [Démarche analytique](#démarche-analytique)
- [Approche données](#approche-données)
- [Couche analytique (Data Warehouse)](#couche-analytique-data-warehouse)
- [Architecture globale](#architecture-globale)
- [Stack technologique](#stack-technologique)
- [KPIs industriels clés](#kpis-industriels-clés)
- [Organisation du repository](#organisation-du-repository)
- [Dashboards Power BI](#dashboards-power-bi)
- [Pipeline](#le-pipeline)
- [Installation](#installation)
- [Organisation du projet](#structure-du-projet)
- [Documentation](#documentation-détaillée)
---

## Contexte industriel
- **Secteur** : industrie agroalimentaire (conditionnement fromager)
- **Ateliers** : ovales, camembert, portions
- **Équipements** : empileur / dépileur, emballeuse, encaisseuse
- **Organisation** : équipes matin / soir / nuit / SD (samedi, dimanche)

Chaque ligne fonctionne avec une **cadence théorique optimale** de :
- **80 fromages par minute**
- **4 800 fromages par heure** (condition sans arrêt)

Lorsqu’un arrêt survient, le système de pilotage indique l’**organe** et l’**élément** en cause.  
L’opérateur intervient directement sur la machine, puis consigne l’événement sur une **feuille de marche**.

---

## Source et nature des données

Les données analysées sont issues de **feuilles de marche opérateur**, renseignées **heure par heure**.

Chaque feuille contient :
- les **heures de production**,
- le **compteur emballeuse** (nombre réel de fromages emballés par heure),
- les **événements d’arrêt**, décrits par :
  - atelier,
  - ligne,
  - machine,
  - organe,
  - élément,
- la **durée approximative** des interventions,
- des **commentaires libres** en cas d’événements non répertoriés,
- les opérations normales : pause, break, échauffement, nettoyage, pilotage.

Les données présentes dans ce repository sont des **mock data réalistes**, reconstruites à partir de ce fonctionnement réel, sans exposition de données sensibles.

---

## Principe de mesure de la non-production

Le temps de non-production n’est pas saisi directement.  
Il est **calculé** à partir de l’écart entre la production théorique et la production réelle.

Pour chaque heure :

**Temps de non-production (minutes) = (4 800 – compteur emballeuse) / 80**


Ce temps peut être expliqué par :
- des arrêts techniques (au niveau organe / élément),
- des arrêts organisationnels (approvisionnement, changements),
- des opérations normales (pause, nettoyage, échauffement),
- des arrêts maintenance.

Les événements enregistrés permettent de **qualifier et analyser** ces pertes de production.

---

## Périmètre d’analyse

L’analyse couvre de manière globale :
- tous les **ateliers**,
- toutes les **lignes de conditionnement**,
- toutes les **machines**,
- l’ensemble des **organes et éléments techniques**,
- tous les **acteurs opérationnels** (opérateurs, chefs d’équipe, responsables).

L’objectif n’est pas l’évaluation individuelle, mais la **compréhension systémique** de la performance industrielle.

---

## Démarche analytique

1. Compréhension du fonctionnement terrain
2. Structuration des données issues des feuilles de marche
3. Normalisation des événements et de la nomenclature
4. Modélisation analytique multi-ateliers et multi-lignes
5. Analyse du temps de non-production et des causes racines
6. Comparaisons transverses (ateliers, machines, équipes, périodes)
7. Restitution via indicateurs et dashboards décisionnels

---
## Approche données

Le projet distingue deux niveaux d’usage des données :

1) **Modèle opérationnel structurant**  
   - décrit fidèlement le fonctionnement industriel  
   - relie usines, ateliers, lignes, shifts, production et événements  
   - garantit traçabilité et cohérence des analyses  

2) **Tables analytiques pour la BI**  
   - issues du modèle opérationnel  
   - agrégées et simplifiées pour les besoins métiers  
   - prêtes à être consommées par Power BI / Tableau  
   - sans complexité technique pour les équipes terrain et management  

## Couche analytique (Data Warehouse)

En complément du modèle opérationnel (ingestion / métier), une couche analytique dédiée est construite pour faciliter l’analyse et la BI.

### Dimensions analytiques
- **dim_machine**
  - machine_key  
  - line_id  
  - workshop_id  
  - factory_id  
  - machine_name  
  - theoretical_capacity_per_hour  
  - reliability_target  

- **dim_time**
  - date  
  - hour  
  - session (MATIN / SOIR / NUIT / SD)  
  - week  
  - month  

- **dim_team**
  - team_lead_id  
  - scope  

- **dim_organe_element**
  - organ  
  - element  

### Table de faits analytique
- **fact_hourly_performance**
  - time_key  
  - machine_key  
  - team_lead_id  
  - total_actual_production  
  - total_theoretical_production  
  - total_non_production_minutes  
  - explained_minutes  
  - unexplained_minutes  

## Architecture globale

```text
Raw data (CSV)
↓
Python (EDA, Cleaning, Modeling)
↓
Parquet (processed / curated)
↓
PostgreSQL (staging → dimensions → facts)
↓
SQL Analytics (BI-ready)
↓
Power BI / Looker

```

---


## Stack Technologique

| Couche | Technologies |
|:---:|:---|
| **Ingestion & ETL** | [![Python](https://img.shields.io/badge/Python-Data%20Processing-3776ab?style=flat&logo=python&logoColor=white)](https://www.python.org/) [![Pandas](https://img.shields.io/badge/Pandas-Data%20Transformation-150458?style=flat&logo=pandas)](https://pandas.pydata.org/) |
| **Storage & Processing** | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Data%20Warehouse-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/) [![Parquet](https://img.shields.io/badge/Parquet-Columnar%20Format-2C3E50?style=flat)](https://parquet.apache.org/) |
| **Analysis & Exploration** | [![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37726?style=flat&logo=jupyter&logoColor=white)](https://jupyter.org/) [![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?style=flat&logo=numpy)](https://numpy.org/) |
| **Visualization & BI** | [![PowerBI](https://img.shields.io/badge/Power%20BI-Business%20Intelligence-F2CC8F?style=flat&logo=powerbi&logoColor=black)](https://www.microsoft.com/power-platform/products/power-bi) [![SQL](https://img.shields.io/badge/SQL-Analytics%20Queries-CC2927?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/) |
| **DevOps & Versioning** | [![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?style=flat&logo=git&logoColor=white)](https://git-scm.com/) [![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/) |

## KPIs industriels clés

### 1️⃣ Fiabilité opérationnelle  
\`\`\`
Fiabilité (%) = Actual Production / Theoretical Production
\`\`\`

### 2️⃣ Taux d’explication des pertes  
\`\`\`
Taux expliqué (%) = Minutes expliquées / Minutes de non-production
\`\`\`

Ces indicateurs permettent :
- d’évaluer la performance réelle des lignes,
- de mesurer la qualité de la traçabilité des événements terrain.



## Organisation du repository

Le projet suit une architecture **modulaire, lisible et reproductible** :

- `data/` : données brutes, traitées et curatées  
- `notebooks/` : exploration, préparation, modélisation et analyse  
- `src/` : logique Python réutilisable (ingestion, nettoyage, modélisation)  
- `sql/` : schémas, tables analytiques et requêtes  
- `docs/` : documentation métier, data et hypothèses  
- `dashboards/` : description des tableaux de bord  

---
## Dashboards Power BI

Les dashboards Power BI sont conçus pour offrir une **lecture claire, synthétique et orientée décision** des performances commerciales.

### Emplacement des fichiers

```text
dashboards/
└── powerbi/
    ├── sales_performance.pbix
    └── screenshots/
```

## Le pipeline

initialise les tables SQL,

charge le staging,

alimente les dimensions,

peuple la table de faits.



## Installation

```text
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .

```
## Run pipeline

```text
python -m sales_orders.cli run 
```
or


```text
sales-orders run
```
## Résultats attendus

- Vision consolidée de la performance industrielle
- Identification des principaux contributeurs au temps de non-production
- Analyse des écarts entre ateliers, lignes et machines
- Aide à la priorisation des actions d’amélioration continue

---

## Documentation détaillée

La documentation fonctionnelle et technique du projet est centralisée dans le dossier `docs/` :

- **Architecture globale**  
  👉 [`docs/architecture_overview.md`](docs/architecture_overview.md)

- **Modèle de données (Star Schema)**  
  👉 [`docs/data_model.md`](docs/data_model.md)

- **Dictionnaire de données**  
  👉 [`docs/data_dictionary.md`](docs/data_dictionary.md)

- **Définition des KPI métier**  
  👉 [`docs/kpi_definitions.md`](docs/kpi_definitions.md)

- **Hypothèses, périmètre et limites du projet**  
  👉 [`docs/assumptions_and_limits.md`](docs/assumptions_and_limits.md)


## ⚠️ Limites

- Données issues de saisies manuelles (durées estimées)
- Granularité horaire
- Micro-arrêts non systématiquement tracés

Ces limites sont **documentées et prises en compte** dans l’interprétation des résultats.

---

## 👤 Auteur
Projet de portfolio **Data Analyst senior** – Orientation **industrie**, **performance opérationnelle** et **pilotage data-driven**.  
Basé sur mon expérience en tant que **pilote de ligne de production**, appliquée à ma vision du métier de Data Analyst.

## Contact & Liens

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mounkaila%20Issoufou-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/abdoul-m-3a76b5214/)
[![GitHub](https://img.shields.io/badge/GitHub-mounkaila--issoufou-181717?style=flat-square&logo=github)](https://github.com/mounkaila-issoufou)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-D14836?style=flat-square&logo=gmail)](mailto:mounkaila.issoufou025@gmail.com)


## Licence

Ce projet est sous licence **MIT** – libre d’utilisation à des fins éducatives et professionnelles.
