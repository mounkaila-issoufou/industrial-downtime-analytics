# 📐 Data Model – Industrial Production & Downtime Analytics

## 🎯 Objectif du modèle
Ce modèle de données vise à analyser la performance industrielle à partir :
- de la production horaire réelle,
- des arrêts machines détaillés,
- du contexte humain (opérateurs, chefs d’équipe),
- du contexte temporel (shifts).

Il permet d’expliquer **pourquoi** la production s’écarte du théorique, et pas seulement **combien**.

---

## 🧱 Vue d’ensemble conceptuelle

```text
Factory
└── Workshop
└── Production_Line
└── Shift_Supervision
├── Shift_Operator_Assignment
└── Hourly_Production
└── Production_Events
```

Le modèle est :
- relationnel
- orienté faits
- historisable
- compatible BI (Power BI / SQL / Python)

---

## 🏭 Dimensions de structure

### `factory`
Représente un site industriel.

| Champ | Description |
|---|---|
| factory_id (PK) | Identifiant usine |
| factory_name | Nom du site |
| city | Ville |
| country | Pays |

---

### `workshop`
Atelier de production au sein d’une usine.

| Champ | Description |
|---|---|
| workshop_id (PK) | Identifiant atelier |
| workshop_name | Ovale, Camembert, Portion, Entier |
| factory_id (FK) | Usine de rattachement |

---

### `production_line`
Ligne ou machine de conditionnement.

| Champ | Description |
|---|---|
| line_id (PK) | Identifiant ligne |
| machine_name | ms, es50, ENT1, ALPA1… |
| workshop_id (FK) | Atelier |
| theoretical_capacity_per_hour | Capacité théorique (ex: 4800) |
| reliability_target | Objectif de fiabilité (%) |

---

## 👥 Dimensions humaines

### `operator`
Opérateur de conduite machine.

| Champ | Description |
|---|---|
| operator_id (PK) | Identifiant opérateur |
| experience_years | Ancienneté |
| status | Actif / Intérim |

---

### `team_lead`
Chef d’équipe.

| Champ | Description |
|---|---|
| team_lead_id (PK) | Identifiant chef |
| scope | Ligne / Atelier |

---

## ⏱️ Tables de contexte (Shifts)

### `shift_supervision`
Décrit le **contexte managérial d’un service**.

| Champ | Description |
|---|---|
| shift_supervision_id (PK) | Identifiant du shift |
| date | Date |
| session | MATIN / SOIR / NUIT / SD |
| start_time | Heure de début |
| end_time | Heure de fin |
| factory_id (FK) | Usine |
| workshop_id (FK) | Atelier |
| line_id (FK) | Ligne |
| team_lead_id (FK) | Chef d’équipe |

---

### `shift_operator_assignment`
Décrit quel opérateur travaille pendant un shift.

| Champ | Description |
|---|---|
| shift_operator_assignment_id (PK) | Affectation |
| shift_supervision_id (FK) | Shift |
| operator_id (FK) | Opérateur |
| role | Conduite / Assistance |

---

## 📊 Tables de faits (Production)

### `hourly_production`
Table de faits principale – production agrégée à l’heure.

| Champ | Description |
|---|---|
| hourly_prod_id (PK) | Identifiant production horaire |
| shift_supervision_id (FK) | Contexte du shift |
| operator_id (FK) | Opérateur |
| team_lead_id (FK) | Chef d’équipe |
| line_id (FK) | Ligne |
| hour_timestamp | Heure de référence |
| theoretical_production | Production théorique |
| actual_production | Production réelle |
| non_production_minutes | Temps de non-production |

---

### `production_events`
Détail des événements expliquant la non-production.

| Champ | Description |
|---|---|
| event_id (PK) | Identifiant événement |
| hourly_prod_id (FK) | Heure concernée |
| event_type | Défaut / Pause / Nettoyage / Maintenance |
| organ | Empileur / Emballeuse / Encaisseuse |
| element | Trainard, Porte, Delta… |
| duration_minutes | Durée |
| operator_action | Action réalisée |
| escalation | Chef / Maintenance |
| comment | Commentaire libre |

---

## 🔗 Cardinalités principales

- 1 `factory` → N `workshop`
- 1 `workshop` → N `production_line`
- 1 `shift_supervision` → N `hourly_production`
- 1 `hourly_production` → N `production_events`
- 1 `shift_supervision` → N `shift_operator_assignment`

---

## 🧠 Principes de conception

- séparation **faits / dimensions**
- granularité **horaire réaliste**
- traçabilité terrain → analytique
- relations explicites mais non contraignantes (CSV-friendly)
- extensible (qualité, maintenance, TRS)

---

## 📌 Cas d’analyse rendus possibles

- Fiabilité par ligne, atelier, site
- Analyse des arrêts par organe / élément
- Comparaison des performances par shift
- Impact des chefs d’équipe
- Pareto des causes de non-production

---

## ⚠️ Hypothèses et limites
- Un opérateur est affecté à un seul shift à la fois
- Les événements expliquent la non-production d’une heure donnée
- Les objectifs de fiabilité sont définis par ligne
- Les durées d’intervention sont estimées manuellement.
- Les micro-arrêts peuvent ne pas être tracés.
- La qualité des analyses dépend de la rigueur de saisie terrain.

Ces limites sont documentées et prises en compte dans l’interprétation.

---
## ✅ Conclusion

Ce modèle de données fournit une base **robuste, scalable et compréhensible** pour l’analyse de la performance industrielle.

Il est adapté à :
- un contexte multi-usines,
- un usage analytique avancé,
- une démarche d’amélioration continue pilotée par la donnée.
