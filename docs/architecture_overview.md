# 🏗️ Architecture Overview – Industrial Production Analytics

## 🎯 Objectif
Ce document décrit l’**architecture globale du projet**, depuis la génération / collecte des données terrain jusqu’à leur exploitation analytique et décisionnelle.

L’architecture est pensée pour être :
- réaliste par rapport à un environnement industriel,
- modulaire et maintenable,
- facilement extensible vers un contexte réel (MES / ERP / BI).

---

## 🧠 Vue d’ensemble

```text
Feuilles de marche / Terrain
↓
Mock / Ingestion (Python)
↓
Data Raw (CSV)
↓
Cleaning & Structuration
↓
Data Processed / Curated
↓
Modèle analytique (Facts / Dimensions)
↓
SQL Analytics / KPI
↓
Dashboards & Insights
```

---

## 📥 Sources de données

### 1. Données opérationnelles terrain
Inspirées de la réalité industrielle :
- feuilles de marche opérateurs,
- compteurs machines (emballeuse),
- écrans de pilotage ligne.

Types de données :
- production horaire,
- événements d’arrêt détaillés,
- planning des shifts,
- supervision (chef d’équipe).

---

## ⚙️ Couche Ingestion (Python)

**Responsabilité :**
- générer ou charger les données brutes,
- garantir la cohérence des identifiants et des dates,
- produire des fichiers exploitables pour l’analyse.

**Scripts clés :**
- `generate_shift_context.py`
- `generate_mock_production_data.py`
- `run_generation.py`

**Principes :**
- seed aléatoire contrôlé,
- IDs uniques et stables,
- paramètres centralisés (dates, opérateurs, lignes).

---

## 🗂️ Data Layers

### 1. Raw
Données brutes, non modifiées :
- `hourly_production.csv`
- `production_events.csv`
- `shift_operator_assignment.csv`
- `shift_supervision.csv`

➡️ Fidèles à la saisie terrain.

---

### 2. Processed
Données nettoyées et enrichies :
- typage des colonnes,
- contrôles de cohérence,
- normalisation des libellés.

---

### 3. Curated
Données prêtes pour l’analyse :
- tables de faits,
- dimensions analytiques,
- calculs intermédiaires.

---

## 🧱 Modélisation des données

### 🔹 Dimensions
- Factory / Site
- Workshop (atelier)
- Production Line / Machine
- Operator
- Team Lead
- Shift
- Time (date, heure)

### 🔹 Faits
- `fact_hourly_production`
- `fact_production_events`

Le modèle est **event-based**, centré sur :
- la performance réelle,
- les causes de non-production.

---

## 📊 Couche Analytics

### SQL / Python Analytics
- calcul de la fiabilité,
- temps de non-production,
- analyse des causes dominantes,
- comparaison objectifs vs réel.

### KPIs principaux
- Taux de fiabilité
- Temps d’arrêt par organe / élément
- Production réelle vs théorique
- Contribution des arrêts planifiés / non planifiés

---

## 📈 Restitution & BI

### Dashboards (Power BI / Looker – conceptuels)
- performance par ligne / atelier,
- top causes d’arrêts,
- suivi opérateur / équipe,
- tendance hebdomadaire / mensuelle.

➡️ Pensés pour :
- chefs d’équipe,
- responsables atelier,
- direction industrielle.

---

## 🔐 Gouvernance & Qualité des données

- contrôles de complétude (heures manquantes),
- cohérence production ↔ événements,
- règles métiers documentées,
- hypothèses et limites explicitées.

---

## 🚀 Scalabilité & Extensions possibles

- Connexion à un MES réel
- Ajout de la qualité produit
- Intégration maintenance préventive
- Historisation des objectifs
- Temps réel / near real-time

---

## ✅ Conclusion
Cette architecture fournit une **base robuste, réaliste et évolutive** pour l’analyse de la performance industrielle.

Elle démontre une capacité à :
- comprendre le terrain,
- structurer la donnée,
- produire de la valeur métier.

➡️ Positionnement clair : **Data Analyst / Analytics Engineer orienté industrie**.
