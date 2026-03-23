# 📘 Data Dictionary – Industrial Production & Downtime Analytics

---

## 🎯 Objectif du data dictionary

Ce document décrit **l’ensemble des tables et des champs** utilisés dans le projet afin de :

* garantir une compréhension commune (data / métier),
* faciliter l’analyse, la maintenance et l’évolution du modèle,
* servir de référence pour les équipes data, métier et recruteurs.

---

# 🏭 OPERATIONAL MODEL (OPS)

---

## 🏭 factory

| Champ        | Type   | Description                   |
| ------------ | ------ | ----------------------------- |
| factory_id   | string | Identifiant unique de l’usine |
| factory_name | string | Nom du site industriel        |
| city         | string | Ville                         |
| country      | string | Pays                          |

---

## 🧰 workshop

| Champ         | Type   | Description           |
| ------------- | ------ | --------------------- |
| workshop_id   | string | Identifiant atelier   |
| workshop_name | string | Type d’atelier        |
| factory_id    | string | Usine de rattachement |

---

## 🛠 production_line

| Champ                         | Type    | Description             |
| ----------------------------- | ------- | ----------------------- |
| line_id                       | string  | Identifiant ligne       |
| machine_name                  | string  | Nom machine             |
| workshop_id                   | string  | Atelier                 |
| theoretical_capacity_per_hour | integer | Capacité max            |
| reliability_target            | float   | Objectif de performance |
| line_status                   | string  | Statut opérationnel     |

---

## 👤 operator

| Champ            | Type    | Description                 |
| ---------------- | ------- | --------------------------- |
| operator_id      | string  | Identifiant opérateur       |
| experience_years | integer | Ancienneté                  |
| status           | string  | Actif / Intérim / Formation |

---

## 🧑‍💼 team_lead

| Champ        | Type   | Description                 |
| ------------ | ------ | --------------------------- |
| team_lead_id | string | Chef d’équipe               |
| scope        | string | Périmètre de responsabilité |

---

## ⏱ shift_supervision

| Champ                | Type   | Description         |
| -------------------- | ------ | ------------------- |
| shift_supervision_id | string | Identifiant shift   |
| date                 | date   | Date                |
| session              | string | MATIN / SOIR / NUIT |
| factory_id           | string | Usine               |
| workshop_id          | string | Atelier             |
| line_id              | string | Ligne               |
| team_lead_id         | string | Chef d’équipe       |

---

## 👷 shift_operator_assignment

| Champ                        | Type   | Description |
| ---------------------------- | ------ | ----------- |
| shift_operator_assignment_id | string | Affectation |
| shift_supervision_id         | string | Shift       |
| operator_id                  | string | Opérateur   |
| role                         | string | Rôle        |

---

## ⏳ hourly_production (⚡ TABLE CENTRALE)

| Champ                  | Type    | Description             |
| ---------------------- | ------- | ----------------------- |
| hourly_prod_id         | string  | Identifiant unique      |
| date                   | date    | Date                    |
| session                | string  | Shift                   |
| shift_supervision_id   | string  | Contexte                |
| operator_id            | string  | Opérateur               |
| team_lead_id           | string  | Chef                    |
| workshop_id            | string  | Atelier                 |
| line_id                | string  | Ligne                   |
| hour_index             | integer | Heure (0–23)            |
| theoretical_production | integer | Production cible        |
| actual_production      | integer | Production réelle       |
| reliability_target     | float   | Objectif                |
| non_production_minutes | integer | Minutes perdues         |
| explained_minutes      | integer | Minutes expliquées      |
| unexplained_minutes    | integer | Minutes non expliquées  |
| reliability_rate       | float   | Performance réelle      |
| reliability_gap        | float   | Écart objectif          |
| explained_ratio        | float   | % pertes expliquées     |
| unexplained_ratio      | float   | % pertes non expliquées |

---

## 🚨 production_events

| Champ            | Type    | Description      |
| ---------------- | ------- | ---------------- |
| event_id         | string  | Identifiant      |
| hourly_prod_id   | string  | Heure liée       |
| event_type       | string  | Type d’arrêt     |
| cause_family     | string  | Catégorie        |
| organ            | string  | Organe machine   |
| element          | string  | Élément précis   |
| operator_action  | string  | Action opérateur |
| duration_minutes | integer | Durée            |
| comment          | text    | Description      |

---

## 🔍 quality_inspection

| Champ           | Type    | Description        |
| --------------- | ------- | ------------------ |
| inspection_id   | string  | Identifiant        |
| hourly_prod_id  | string  | Heure liée         |
| inspection_date | date    | Date               |
| session         | string  | Shift              |
| inspector_id    | string  | Inspecteur         |
| workshop_id     | string  | Atelier            |
| line_id         | string  | Ligne              |
| inspection_type | string  | Type contrôle      |
| inspected_units | integer | Quantité inspectée |

---

## ❌ quality_event

| Champ            | Type    | Description        |
| ---------------- | ------- | ------------------ |
| quality_event_id | string  | Identifiant défaut |
| inspection_id    | string  | Inspection liée    |
| defect_category  | string  | Catégorie          |
| defect_family    | string  | Famille            |
| defect_type      | string  | Type précis        |
| defective_units  | integer | Quantité défaut    |
| scrap_units      | integer | Rebut              |
| reworked_units   | integer | Retouches          |

---

# 📊 DATA WAREHOUSE (DW)

---

## ⏱ dim_time

| Champ       | Type    | Description    |
| ----------- | ------- | -------------- |
| time_key    | integer | Clé YYYYMMDDHH |
| date        | date    | Date           |
| hour_of_day | integer | Heure          |
| month       | integer | Mois           |
| year        | integer | Année          |

---

## 🏭 dim_machine

| Champ       | Type    | Description   |
| ----------- | ------- | ------------- |
| machine_key | integer | Clé surrogate |
| line_id     | string  | Ligne         |
| workshop_id | string  | Atelier       |
| factory_id  | string  | Usine         |

---

## 👥 dim_team (⚠️ SENSIBLE)

| Champ         | Type      | Description    |
| ------------- | --------- | -------------- |
| team_key      | integer   | Clé            |
| team_lead_id  | string    | Chef           |
| session       | string    | Shift          |
| scope_line_id | string    | Ligne          |
| valid_from    | timestamp | Historisation  |
| is_current    | boolean   | Version active |

---

## 🧩 dim_quality_defect

| Champ           | Type    | Description |
| --------------- | ------- | ----------- |
| defect_key      | integer | Clé         |
| defect_category | string  | Catégorie   |
| defect_family   | string  | Famille     |
| defect_type     | string  | Type        |

---

# 📈 FACT TABLES

---

## ⚡ fact_hourly_performance

| Champ                  | Type    | Description       |
| ---------------------- | ------- | ----------------- |
| time_key               | integer | Temps             |
| machine_key            | integer | Machine           |
| team_key               | integer | Équipe            |
| theoretical_production | integer | Cible             |
| actual_production      | integer | Réel              |
| non_production_minutes | integer | Downtime          |
| explained_minutes      | integer | Pertes expliquées |
| unexplained_minutes    | integer | Pertes inconnues  |
| reliability_rate       | float   | Performance       |
| explained_ratio        | float   | Ratio             |
| unexplained_ratio      | float   | Ratio             |

👉 **Grain : 1 heure × 1 machine × 1 équipe**

---

## 🚨 fact_production_events

| Champ              | Type    | Description |
| ------------------ | ------- | ----------- |
| time_key           | integer | Temps       |
| machine_key        | integer | Machine     |
| team_key           | integer | Équipe      |
| organe_element_key | integer | Cause       |
| duration_minutes   | integer | Durée       |

---

## 🔍 fact_quality_events

| Champ           | Type    | Description |
| --------------- | ------- | ----------- |
| time_key        | integer | Temps       |
| machine_key     | integer | Machine     |
| team_key        | integer | Équipe      |
| defect_key      | integer | Défaut      |
| defective_units | integer | Défauts     |
| scrap_units     | integer | Rebut       |
| reworked_units  | integer | Retouche    |

👉 ⚠️ **Grain = événement qualité (pas agrégé)**

---

## 🏆 fact_oee_hourly

| Champ        | Type    | Description   |
| ------------ | ------- | ------------- |
| time_key     | integer | Temps         |
| machine_key  | integer | Machine       |
| team_key     | integer | Équipe        |
| availability | float   | Disponibilité |
| performance  | float   | Performance   |
| quality      | float   | Qualité       |
| oee          | float   | TRS           |

👉 **Grain identique à fact_hourly_performance**

---

# 🧠 RÈGLES MÉTIER CLÉS

* **OEE = Availability × Performance × Quality**
* Une heure = **60 minutes observées**
* Les pertes peuvent être :

  * expliquées (événements)
  * non expliquées (gap data)
* Une heure peut contenir **plusieurs événements**
* La qualité est calculée via :

  * production réelle
  * défauts

---

# ⚠️ PIÈGES IDENTIFIÉS (TRÈS IMPORTANT)

* ❌ Mauvais grain → duplication (dim_team)
* ❌ SUM sur données déjà horaires → incohérences
* ❌ Mauvais JOIN → explosion des lignes
* ❌ mismatch grain qualité vs production

---

# 💡 BONNES PRATIQUES IMPLÉMENTÉES

* Idempotence (`ON CONFLICT`)
* Partitionnement temporel
* Index BRIN pour tables volumineuses
* Validation des agrégats (OPS vs DW)
* Simulation réaliste (Markov)

---

# 📌 NOTES

* Modèle inspiré des systèmes MES industriels
* Structure compatible BI (Power BI)
* Architecture scalable (ajout maintenance, énergie, etc.)
