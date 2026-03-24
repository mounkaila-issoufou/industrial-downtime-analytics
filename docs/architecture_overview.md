# 🏗️ Architecture Overview – Industrial Production Analytics

## 🎯 Objectif

Ce document décrit l’**architecture globale du projet**, depuis la génération des données terrain jusqu’à leur exploitation analytique et décisionnelle.

L’architecture est conçue pour être :

* réaliste (proche d’un environnement industriel réel),
* modulaire (séparation claire des couches),
* scalable (évolutive vers un contexte production),
* BI-ready (optimisée pour Power BI / SQL analytics).

---

# 🧠 Vue d’ensemble

```text
Mock Generator (Python)
↓
STAGING (Raw Data)
↓
OPS (Operational Model)
↓
DW (Star Schema)
↓
Analytics (SQL / DAX)
↓
Dashboard (Power BI)
```

---

# 📥 1. Sources de données

## 🏭 Données simulées (Mock Data)

Inspirées de la réalité industrielle :

* production horaire
* événements d’arrêt machines
* inspections qualité
* défauts produits
* organisation des équipes (shift)

### Types de données

* **Production** : volumes théoriques vs réels
* **Downtime** : causes détaillées (organe, élément)
* **Qualité** : défauts, rebuts, retouches
* **Contexte humain** : opérateurs, chefs d’équipe

---

# ⚙️ 2. Couche Ingestion (Python)

## 🎯 Rôle

* générer des données cohérentes
* simuler des comportements industriels réalistes
* injecter de la variabilité contrôlée

## 🧠 Mécaniques utilisées

* moteur Markov → simulation des états machine
* génération d’événements (micro-arrêts, pannes)
* calcul de KPI intermédiaires
* génération qualité (inspection + défauts)

## 📁 Modules clés

* `production/` → simulation production
* `events/` → génération downtime
* `quality/` → génération défauts
* `kpi_calculator.py` → calculs métiers

---

# 🗂️ 3. Data Layers (Architecture en 3 couches)

## 🥉 STAGING (stg)

### 🎯 Objectif

Zone raw data (brut, traçable)

### Caractéristiques

* aucune transformation métier
* ajout de métadonnées :

  * `source_file_name`
  * `load_timestamp`

### Tables

* `stg.hourly_production`
* `stg.production_events`
* `stg.quality_inspection`
* `stg.quality_events`

---

## 🥈 OPS (Operational Layer)

### 🎯 Objectif

Modèle relationnel propre et cohérent

### Caractéristiques

* normalisation des données
* intégrité référentielle (FK)
* structure proche du terrain

### Tables

* `ops.hourly_production`
* `ops.production_event`
* `ops.quality_inspection`
* `ops.quality_event`
* `ops.shift_supervision`
* `ops.operator_assignment`

---

## 🥇 DW (Data Warehouse)

### 🎯 Objectif

Modèle analytique optimisé BI (schéma en étoile)

### 📐 Dimensions

* `dim_time`
* `dim_machine`
* `dim_team`
* `dim_organe_element`
* `dim_quality_defect`

### 📊 Tables de faits

#### 🔹 Performance

* `fact_hourly_performance`

#### 🔹 Événements

* `fact_production_events`

#### 🔹 Qualité

* `fact_quality_events`

#### 🔹 KPI global

* `fact_oee_hourly`

### ⚡ Optimisations

* partitionnement par `time_key`
* index (B-Tree + BRIN)
* modèle dénormalisé pour Power BI

---

# 🧠 4. Couche Analytics

## 📊 SQL

* calcul des agrégats
* construction des faits
* jointures dimensions

## 📈 DAX (Power BI)

* KPI dynamiques :

  * OEE
  * Availability
  * Performance
  * Quality

* deltas temporels

* indicateurs visuels (couleurs, labels)

---

# 📊 5. Dashboard (Power BI)

## 🧱 Structure

### 🔝 KPIs

* OEE
* Availability
* Performance
* Quality
* Scrap Rate

### 📈 Trends

* OEE over time
* Downtime trend
* Reliability evolution

### 🧠 Root Cause Analysis

* Top causes downtime
* Pareto (80/20)
* Downtime by machine

### ⚙️ Operations

* statut machine
* alertes actives
* monitoring temps réel (simulé)

---

# 🔐 6. Data Quality & Gouvernance

## ✅ Contrôles mis en place

### Intégrité

* Foreign Keys (OPS)
* contraintes métiers (CHECK)

### Cohérence

* production vs downtime
* explained vs unexplained minutes

### Complétude

* heures manquantes
* défauts non rattachés

## 🧪 Tests & garde-fous

* détection des doublons
* vérification des ratios (0–1)
* validation du grain (1h = 1 ligne)

---

# 🚀 7. Scalabilité & Extensions

## 🔮 Extensions possibles

* connexion MES réel
* ingestion streaming (Kafka)
* orchestration (Airflow / Prefect / Dagster)
* monitoring (Grafana)
* machine learning (prédiction pannes)

---

# 🧠 8. Positionnement Data

Ce projet démontre :

## 🧩 Data Engineering

* pipeline complet (Python → SQL → DW)
* gestion des couches data
* idempotence

## 📊 Analytics Engineering

* modélisation en étoile
* KPI métier
* performance BI

## 🏭 Compréhension métier

* logique industrielle réelle
* OEE / downtime / qualité
* analyse root cause

---

# 📌 Conclusion

Cette architecture constitue une base :

* robuste
* scalable
* orientée métier
