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

```mermaid

erDiagram

    FACTORY {
        string factory_id PK
        string factory_name
        string city
        string country
    }

    WORKSHOP {
        string workshop_id PK
        string workshop_name
        string factory_id FK
    }

    PRODUCTION_LINE {
        string line_id PK
        string machine_name
        string workshop_id FK
        int theoretical_capacity_per_hour
        float reliability_target
    }

    OPERATOR {
        string operator_id PK
        int experience_years
        string status
    }

    TEAM_LEAD {
        string team_lead_id PK
        string scope
    }

    SHIFT_SUPERVISION {
        string shift_supervision_id PK
        date date
        string session
        time start_time
        time end_time
        string factory_id FK
        string workshop_id FK
        string line_id FK
        string team_lead_id FK
    }

    SHIFT_OPERATOR_ASSIGNMENT {
        string shift_operator_assignment_id PK
        string shift_supervision_id FK
        string operator_id FK
        string role
    }

    HOURLY_PRODUCTION {
        string hourly_prod_id PK
        string shift_supervision_id FK
        string operator_id FK
        string team_lead_id FK
        string workshop_id FK
        string line_id FK
        date production_date
        string session
        int hour_index
        int theoretical_production
        int actual_production
        float reliability_target
        float reliability_rate
        float reliability_gap
        int non_production_minutes
        int explained_minutes
        int unexplained_minutes
        float explained_ratio
        float unexplained_ratio
    }

    PRODUCTION_EVENTS {
        string event_id PK
        string hourly_prod_id FK
        string event_type
        string organ
        string element
        int duration_minutes
        string operator_action
        string escalation
        string comment
    }

    FACTORY ||--o{ WORKSHOP : has
    WORKSHOP ||--o{ PRODUCTION_LINE : has

    FACTORY ||--o{ SHIFT_SUPERVISION : context
    WORKSHOP ||--o{ SHIFT_SUPERVISION : context
    PRODUCTION_LINE ||--o{ SHIFT_SUPERVISION : context
    TEAM_LEAD ||--o{ SHIFT_SUPERVISION : supervises

    SHIFT_SUPERVISION ||--o{ SHIFT_OPERATOR_ASSIGNMENT : assigns
    OPERATOR ||--o{ SHIFT_OPERATOR_ASSIGNMENT : works_on

    SHIFT_SUPERVISION ||--o{ HOURLY_PRODUCTION : generates
    OPERATOR ||--o{ HOURLY_PRODUCTION : produces
    TEAM_LEAD ||--o{ HOURLY_PRODUCTION : manages
    PRODUCTION_LINE ||--o{ HOURLY_PRODUCTION : produces_on

    HOURLY_PRODUCTION ||--o{ PRODUCTION_EVENTS : explains
```

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
- fact_production_events

```mermaid
erDiagram

    DIM_TIME {
        int time_key PK
        date date
        int year
        int month
        string month_name
        int iso_week
        int day_of_week
        string day_name
        int hour_of_day
        string session
        boolean is_weekend
    }

    DIM_MACHINE {
        int machine_key PK
        string line_id UK
        string factory_id
        string workshop_id
        string factory_name
        string workshop_name
        string machine_name
        int theoretical_capacity_per_hour
        float reliability_target
        string line_status
        timestamp valid_from
        timestamp valid_to
        boolean is_current
    }

    DIM_TEAM {
        int team_key PK
        string team_lead_id
        string shift_supervision_id
        string session
        string scope_factory_id
        string scope_workshop_id
        string scope_line_id
        timestamp valid_from
        timestamp valid_to
        boolean is_current
    }

    DIM_ORGANE_ELEMENT {
        int organe_element_key PK
        string organe
        string element
        string cause_category
        string cause_family
        timestamp valid_from
        timestamp valid_to
        boolean is_current
    }

    FACT_HOURLY_PERFORMANCE {
        int time_key FK
        int machine_key FK
        int team_key FK
        int theoretical_production
        int actual_production
        int non_production_minutes
        int explained_minutes
        int unexplained_minutes
        float reliability_rate
        float explained_ratio
        float unexplained_ratio
        timestamp load_timestamp
    }

    FACT_PRODUCTION_EVENTS {
        int time_key FK
        int machine_key FK
        int team_key FK
        int organe_element_key FK
        int duration_minutes
        timestamp load_timestamp
    }

    DIM_TIME ||--o{ FACT_HOURLY_PERFORMANCE : "time_key"
    DIM_MACHINE ||--o{ FACT_HOURLY_PERFORMANCE : "machine_key"
    DIM_TEAM ||--o{ FACT_HOURLY_PERFORMANCE : "team_key"

    DIM_TIME ||--o{ FACT_PRODUCTION_EVENTS : "time_key"
    DIM_MACHINE ||--o{ FACT_PRODUCTION_EVENTS : "machine_key"
    DIM_TEAM ||--o{ FACT_PRODUCTION_EVENTS : "team_key"
    DIM_ORGANE_ELEMENT ||--o{ FACT_PRODUCTION_EVENTS : "organe_element_key"
```



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
