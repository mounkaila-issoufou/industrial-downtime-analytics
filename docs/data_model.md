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
## SCHÉMA 1 — MODÈLE OPÉRATIONNEL
```text
FACTORY
   │
   └── WORKSHOP
         │
         └── PRODUCTION_LINE
               │
               └── SHIFT_SUPERVISION  (DIMENSION DE CONTEXTE)
                       │
       ┌──────────────┼───────────────────────┐
       │                              │
SHIFT_OPERATOR_ASSIGNMENT      HOURLY_PRODUCTION  (FAIT)
                                      │
                                      └── PRODUCTION_EVENTS (FAIT)

```

## SCHÉMA 2 — MODÈLE ANALYTIQUE
```text
              DIM_TIME
                  │
DIM_MACHINE ─── FACT_HOURLY_PERFORMANCE   (pilotage global)
                  │
                  │
         FACT_PRODUCTION_EVENTS (diagnostic détaillé)
                  │
          DIM_ORGANE_ELEMENT


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

| Champ | Type | Description |
|-------|------|------------|
| `line_id` | PK / VARCHAR | Identifiant de la ligne |
| `machine_name` | VARCHAR | Nom de la machine (ex: MS, ES50, ENT1, ALPA1…) |
| `workshop_id` | FK / VARCHAR | Atelier auquel la ligne appartient |
| `theoretical_capacity_per_hour` | INT | Capacité théorique maximale par heure (ex: 4800) |
| `reliability_target` | NUMERIC(5,4) | Objectif de fiabilité (%) |


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

| Champ | Type | Description |
|-------|------|------------|
| `hourly_prod_id` | PK / VARCHAR | Identifiant unique de la production horaire |
| `shift_supervision_id` | FK / VARCHAR | Contexte du shift |
| `operator_id` | FK / VARCHAR | Opérateur responsable |
| `team_lead_id` | FK / VARCHAR | Chef d’équipe |
| `workshop_id` | FK / VARCHAR | Atelier |
| `line_id` | FK / VARCHAR | Ligne de production |
| `production_date` | DATE | Date du shift |
| `session` | VARCHAR | Session du shift (matin, après-midi, etc.) |
| `hour_index` | INT | Heure dans le shift (0 = première heure, …) |
| `theoretical_production` | INT | Production théorique maximale attendue |
| `actual_production` | INT | Production réellement réalisée |
| `reliability_target` | NUMERIC(5,4) | Objectif de fiabilité pour la ligne |
| `reliability_rate` | NUMERIC(6,4) | Taux de fiabilité réel (actual / theoretical) |
| `reliability_gap` | NUMERIC(6,4) | Écart entre fiabilité réelle et cible |
| `non_production_minutes` | INT | Minutes de non-production |
| `explained_minutes` | INT | Minutes de perte expliquées (pauses, maintenance planifiée, etc.) |
| `unexplained_minutes` | INT | Minutes de perte inexpliquées |
| `explained_ratio` | NUMERIC(6,4) | Ratio minutes expliquées / non-production |
| `unexplained_ratio` | NUMERIC(6,4) | Ratio minutes inexpliquées / non-production |


---

### `production_events`  
Détail des événements expliquant la non-production.

| Champ | Type | Description |
|-------|------|------------|
| `event_id` | PK / VARCHAR | Identifiant unique de l’événement |
| `hourly_prod_id` | FK / VARCHAR | Heure concernée (`hourly_production`) |
| `event_type` | VARCHAR | Type d’événement (ex: Défaut, Pause, Nettoyage, Maintenance) |
| `organ` | VARCHAR | Machine ou poste concerné (ex: Empileur, Emballeuse, Encaisseuse) |
| `element` | VARCHAR | Élément spécifique affecté (ex: Trainard, Porte, Delta…) |
| `duration_minutes` | INT | Durée de l’événement en minutes |
| `operator_action` | VARCHAR | Action réalisée par l’opérateur |
| `escalation` | VARCHAR | Escalade si nécessaire (ex: Chef, Maintenance) |
| `comment` | TEXT | Commentaire libre |


---

## 🔗 Cardinalités principales

- 1 `factory` → N `workshop`
- 1 `workshop` → N `production_line`
- 1 `shift_supervision` → N `hourly_production`
- 1 `hourly_production` → N `production_events`
- 1 `shift_supervision` → N `shift_operator_assignment`

---

## 🧠 Principes analytiques supplémentaires

- séparation claire entre modèle opérationnel et modèle analytique,
- agrégation horaire comme grain principal,
- traçabilité entre production et événements,
- compatibilité native avec Power BI / Tableau / SQL,
- évolutivité vers TRS (OEE), qualité et maintenance prédictive.


---
## 🧠 Couche analytique cible (BI-friendly)

Au-dessus du modèle opérationnel, une couche analytique en schéma en étoile est construite pour les usages BI.

### Dimensions
- dim_machine  
- dim_time  
- dim_team  
- dim_organe_element  

### Fait principal
- fact_hourly_performance  

Cette couche permet :
- analyses rapides en SQL,
- modèles Power BI performants,
- comparaisons transverses (atelier, ligne, équipe, période).



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
