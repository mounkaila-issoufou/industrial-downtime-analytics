# 📘 Data Dictionary – Industrial Production & Downtime Analytics

## 🎯 Objectif du data dictionary
Ce document décrit **l’ensemble des tables et des champs** utilisés dans le projet afin de :
- garantir une compréhension commune (data / métier),
- faciliter l’analyse, la maintenance et l’évolution du modèle,
- servir de référence lors des échanges avec des recruteurs, managers ou équipes industrielles.

---

## 🏭 factory

| Champ | Type | Description |
|---|---|---|
| factory_id | string | Identifiant unique de l’usine |
| factory_name | string | Nom du site industriel |
| city | string | Ville |
| country | string | Pays |

---

## 🧰 workshop

| Champ | Type | Description |
|---|---|---|
| workshop_id | string | Identifiant atelier |
| workshop_name | string | Type d’atelier (Ovale, Camembert, Portion, Entier) |
| factory_id | string | Usine de rattachement |

---

## 🛠 production_line

| Champ | Type | Description |
|---|---|---|
| line_id | string | Identifiant ligne |
| machine_name | string | Nom réel de la machine (ms, es50, ENT1, ALPA1…) |
| workshop_id | string | Atelier |
| theoretical_capacity_per_hour | integer | Capacité théorique horaire (ex: 4800 fromages) |
| reliability_target | float | Objectif de fiabilité (%) |

---

## 👤 operator

| Champ | Type | Description |
|---|---|---|
| operator_id | string | Identifiant opérateur (anonymisé) |
| experience_years | integer | Ancienneté en années |
| status | string | Actif, Intérim, Formation |

---

## 🧑‍💼 team_lead

| Champ | Type | Description |
|---|---|---|
| team_lead_id | string | Identifiant chef d’équipe |
| scope | string | Périmètre (Ligne, Atelier, Multi-lignes) |

---

## ⏱️ shift_supervision

| Champ | Type | Description |
|---|---|---|
| shift_supervision_id | string | Identifiant unique du shift |
| date | date | Date du service |
| session | string | MATIN / SOIR / NUIT / SD |
| start_time | time | Heure de début |
| end_time | time | Heure de fin |
| factory_id | string | Usine |
| workshop_id | string | Atelier |
| line_id | string | Ligne |
| team_lead_id | string | Chef d’équipe en charge |
| comment | string | Commentaire contextuel |

---

## 👷 shift_operator_assignment

| Champ | Type | Description |
|---|---|---|
| shift_operator_assignment_id | string | Identifiant affectation |
| shift_supervision_id | string | Shift concerné |
| operator_id | string | Opérateur affecté |
| role | string | Conduite machine, Aide |
| comment | string | Information complémentaire |

---

## ⏳ hourly_production

| Champ | Type | Description |
|---|---|---|
| hourly_prod_id | string | Identifiant production horaire |
| shift_supervision_id | string | Contexte du shift |
| operator_id | string | Opérateur |
| team_lead_id | string | Chef d’équipe |
| line_id | string | Ligne |
| hour_timestamp | datetime | Heure de production |
| theoretical_production | integer | Production théorique |
| actual_production | integer | Production réelle |
| non_production_minutes | integer | Minutes de non-production |

---

## 🚨 production_events

| Champ | Type | Description |
|---|---|---|
| event_id | string | Identifiant événement |
| hourly_prod_id | string | Heure associée |
| event_type | string | Défaut, Pause, Nettoyage, Maintenance |
| organ | string | Organe (Empileur, Emballeuse, Encaisseuse) |
| element | string | Élément précis (trainard, porte, delta…) |
| duration_minutes | integer | Durée de l’événement |
| operator_action | string | Action opérateur |
| escalation | string | Intervention chef / maintenance |
| comment | string | Description libre |

---

## 🧠 Règles métier clés

- La capacité théorique maximale est de **4800 fromages/heure**
- La non-production est calculée à partir de l’écart entre théorique et réel
- Plusieurs événements peuvent expliquer une même heure de non-production
- Les opérateurs et chefs d’équipe sont **indépendants** et contextualisés via le shift

---

## 📌 Notes
- Les relations sont **logiques**, non imposées (CSV / analytics-friendly)
- Les identifiants sont générés côté ingestion
- Le modèle est extensible (qualité, maintenance, TRS)

