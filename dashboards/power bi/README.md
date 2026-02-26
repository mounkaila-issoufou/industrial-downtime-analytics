# 📊 Analyse de la Production Industrielle & de la Maintenance

Tableau de bord Power BI conçu pour surveiller la performance de la production industrielle, la fiabilité opérationnelle et l’efficacité de la maintenance, en s’appuyant sur un **modèle en étoile structuré**.

---

# 1️⃣ Présentation du projet

Ce projet propose un **cadre analytique industriel de bout en bout**, construit autour de :

- La performance de production horaire  
- Les événements de production (arrêts / incidents)  
- Les indicateurs d’ingénierie de la fiabilité  
- L’intelligence maintenance  

Le modèle est conçu pour soutenir la **prise de décision opérationnelle**, l’**analyse des causes racines** et l’**optimisation de la performance industrielle**.

---

# 2️⃣ Objectifs métier

Le tableau de bord répond à trois questions stratégiques :

1. Produisons-nous au niveau de capacité attendu ?
2. Quand les dégradations de performance surviennent-elles ?
3. Pourquoi la production s’arrête-t-elle ou ralentit-elle ?

Il s’adresse principalement à :

- Responsables des opérations  
- Ingénieurs maintenance  
- Analystes fiabilité  
- Directeurs d’usine  

---

# 3️⃣ Architecture du modèle de données

Le modèle repose sur une **architecture en étoile (star schema)**.

## ⭐ Tables de faits

### `fact_hourly_performance`
Grain : **1 ligne par machine et par heure**

Contient :
- theoretical_production  
- actual_production  
- non_production_minutes  
- explained_minutes  
- unexplained_minutes  

Objectif :  
Mesurer la performance opérationnelle horaire et l’efficacité de production.

---

### `fact_production_events`
Grain : **1 ligne par événement de production**

Contient :
- event_id  
- machine_id  
- team_id  
- organe_element_id  
- duration_minutes  
- event_timestamp  
- event_type / cause  

Objectif :  
Suivre les événements d’arrêt et permettre l’analyse maintenance.

---

## 📘 Tables de dimensions

### `dim_machine`
- machine_id  
- machine_name  
- machine_type  
- production_line  
- installation_date  

Objectif :  
Analyser les performances et incidents par équipement.

---

### `dim_time`
- date  
- year  
- month  
- month_name  
- week  
- day  
- hour  
- shift  
- weekday_flag  
- weekend_flag  

Objectif :  
Permettre l’analyse temporelle (YTD, indicateurs glissants, analyse par poste).

---

### `dim_team`
- team_id  
- team_name  
- supervision  
- shift_category  

Objectif :  
Analyser la performance par équipe opérationnelle et structure de supervision.

---

### `dim_organe_element`
- organe_element_id  
- component_name  
- subsystem  
- criticality_level  

Objectif :  
Réaliser des analyses de causes racines et de défaillances au niveau composant.

---

# 4️⃣ Vue d’ensemble des relations

- `fact_hourly_performance` → liée à :
  - dim_machine  
  - dim_time  
  - dim_team  

- `fact_production_events` → liée à :
  - dim_machine  
  - dim_time  
  - dim_team  
  - dim_organe_element  

Le modèle permet :

- Le suivi de performance par machine  
- L’analyse temporelle avancée  
- La comparaison des performances par équipe  
- L’analyse de fiabilité au niveau des composants  

---

# 5️⃣ Organisation des mesures DAX

```text
powerbi/
│
├── dashboard.pbix
├── dax/
│ ├── 01_core_kpis.dax
│ ├── 02_time_analysis.dax
│ ├── 03_maintenance_analysis.dax
│ └── README.md
```

---

## 01_core_kpis.dax

Indicateurs clés de performance industrielle :

- Production totale (réelle / théorique)
- Taux de fiabilité (%)
- Minutes expliquées vs non expliquées
- Nombre total d’événements
- Temps d’arrêt total
- Durée moyenne des événements

**Objectif :**  
Fournir une mesure synthétique et de haut niveau de la performance globale.

---

## 02_time_analysis.dax

Mesures analytiques basées sur le temps :

- Indicateurs glissants 7 jours / 30 jours
- Indicateurs YTD (Year-To-Date)
- Comparaisons MoM / YoY
- Analyse par session (Matin / Soir / Nuit / Week-end)

**Objectif :**  
Identifier les tendances temporelles et les schémas de performance.

---

## 03_maintenance_analysis.dax

Indicateurs de maintenance et de fiabilité :

- MTTR (Mean Time To Repair)
- MTBF (Mean Time Between Failures)
- Disponibilité (%)
- Fréquence des incidents
- Sévérité (médiane, durée maximale)
- Analyse de Pareto par cause
- Taux d’incidents critiques
- Tendances glissantes de maintenance

**Objectif :**  
Soutenir l’analyse des causes racines et les stratégies de réduction des arrêts.

---

# 5️⃣ Pages du tableau de bord

---

## 📊 Page 1 — Vue exécutive

### Objectif
Fournir une synthèse exécutive de la performance de l’usine en 30 secondes.

### KPIs clés
- Taux de fiabilité (%)
- Disponibilité (%)
- Production totale
- Écart de production
- MTTR
- MTBF

### Analyses fournies
- État de santé opérationnel global
- Écart par rapport à la capacité théorique
- Arbitrage fiabilité vs maintenabilité

**Public cible :** Direction / Directeur d’usine

---

## 📊 Page 2 — Analyse temporelle & opérationnelle

### Objectif
Identifier quand les problèmes de performance surviennent.

### Analyses clés
- Tendance de production (rolling 30 jours)
- Carte thermique horaire
- Comparaison semaine / week-end
- Comparaison des performances par session
- Tendance mensuelle (YTD)

### Analyses fournies
- Instabilités liées aux postes
- Déviations de performance le week-end
- Dégradations de performance émergentes

**Public cible :** Management des opérations

---

## 📊 Page 3 — Intelligence maintenance

### Objectif
Identifier pourquoi les arrêts surviennent et comment les réduire.

### KPIs clés
- Nombre total d’incidents
- Temps d’arrêt total
- MTTR
- MTBF
- Disponibilité (%)
- Taux d’incidents critiques (%)

### Visuels clés
- Pareto des causes d’arrêt
- Nuage de points fréquence vs sévérité
- Tendance glissante des arrêts
- Arrêts par ligne / supervision

### Analyses fournies
- Priorisation des causes racines
- Défaillances fréquentes vs critiques
- Évolution de l’efficacité de la maintenance
- Zones de risque de fiabilité

**Public cible :** Équipes maintenance & fiabilité

---

# 6️⃣ Logique analytique

La performance industrielle est décomposée en :

1. Efficacité de production
2. Stabilité opérationnelle
3. Efficacité de la maintenance
4. Intelligence des causes racines

Le tableau de bord suit une logique analytique structurée :

- Que se passe-t-il ?
- Quand cela se produit-il ?
- Pourquoi cela se produit-il ?

---

# 7️⃣ Indicateurs industriels clés

- Taux de fiabilité
- Disponibilité
- MTTR
- MTBF
- Contribution aux arrêts (%)
- Pareto cumulatif (%)
- Taux d’incidents critiques

Ces indicateurs soutiennent la prise de décision stratégique et les démarches
d’amélioration continue.

---

# 8️⃣ Extensions potentielles

Les évolutions futures peuvent inclure :

- Modélisation de maintenance prédictive
- Scoring de probabilité de défaillance
- Seuils d’alerte automatisés
- Benchmark inter-usines
- Intégration avec des systèmes ERP / CMMS

---

# 9️⃣ Stack technique

- Power BI
- DAX
- Modélisation de données en étoile
- Git pour le versionnement

---

# 🔟 Note de l’auteur

Ce projet démontre :

- Les bonnes pratiques de modélisation de données
- Une implémentation avancée de DAX
- Une structuration rigoureuse des KPIs industriels
- Une conception de tableau de bord orientée exécutif
- Une narration analytique claire

L’objectif n’est pas uniquement le reporting, mais bien de **permettre des décisions
opérationnelles pilotées par la donnée**.
