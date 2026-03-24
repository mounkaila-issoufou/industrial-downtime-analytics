# 📊 KPI Definitions – Industrial Production & Downtime Analytics

## 🎯 Objectif du document

Ce document définit les **indicateurs clés de performance (KPI)** utilisés pour analyser la performance des lignes de conditionnement fromager.

Les KPI permettent :

* de mesurer la fiabilité et la performance réelle,
* d’identifier les causes de non-production,
* de comparer les performances entre lignes, ateliers, shifts et équipes,
* d’aider à la prise de décision opérationnelle.

---

# 🏭 KPI CORE (Production & Fiabilité)

---

## ⏱️ 1. Production théorique horaire

### Nom

**Production théorique horaire**

### Définition

Quantité maximale de fromages pouvant être emballés en une heure en conditions optimales.

### Formule

```text
Production théorique = capacité ligne (unités / heure)
```

### Source

Table : dw.dim_machine.theoretical_capacity_per_hour

---

## 📦 2. Production réelle horaire

### Nom

Production réelle horaire

### Définition

Nombre réel de fromages emballés sur une heure donnée.

### Source

Table : dw.fact_hourly_performance.actual_production

---

## 📉 3. Taux de fiabilité (Reliability)

### Nom

Fiabilité horaire (%)

### Définition

Rapport entre la production réelle et la production théorique sur une heure donnée.

### Formule

```text
Reliability (%) = (Production réelle / Production théorique)
```

### Interprétation

* 1.0 → performance parfaite
* < 1.0 → pertes de production

---

## 🎯 4. Écart à l’objectif (Reliability Gap)

### Nom

Écart à l’objectif de fiabilité

### Définition

Différence entre la fiabilité réelle et l’objectif défini.

### Formule

```text
Écart = Fiabilité réelle - Objectif de fiabilité
```

### Interprétation

* Écart positif → performance conforme ou supérieure
* Écart négatif → sous-performance

---

# ⏳ KPI TEMPS & PERTES

---

## ⏱️ 5. Temps observé

### Définition

Temps total théorique disponible.

### Formule

```text
Temps observé = nombre d’heures × 60 minutes
```

---

## 🛑 6. Temps de non-production

### Nom

Temps de non-production (minutes)

### Définition

Temps pendant lequel la ligne n’a pas produit sur une heure donnée.

### Source

Table : dw.fact_hourly_performance.non_production_minutes

---

## 🧩 7. Temps expliqué

### Définition

Part du downtime associée à des événements identifiés.

### Source

explained_minutes

---

## ❓ 8. Temps non expliqué

### Définition

Part du downtime sans cause identifiée.

### Source

unexplained_minutes

---

## 📊 9. Ratio d’explication

### Formule

```text
Explained Ratio = explained_minutes / non_production_minutes
```

### Objectif

Mesurer la qualité du tracking des causes.

---

# 🧠 KPI ÉVÉNEMENTS (Root Cause Analysis)

---

## 🚨 10. Nombre d’événements d’arrêt

### Définition

Nombre d’événements enregistrés sur une heure de production.

### Source

Table : dw.fact_production_events

---

## 🧩 11. Temps cumulé d’arrêt

### Définition

Durée totale des arrêts.

### Formule

```text
Total Downtime = SUM(duration_minutes)
```

---

## 🧱 12. Downtime par cause

### Dimensions d’analyse

* event_type
* organ
* element
* cause_category
* session
* ligne

---

## 📊 13. Pareto des causes

### Définition

Classement des causes par contribution décroissante au downtime.

### Objectif

Identifier les causes principales (règle des 80/20).

---

# 🧪 KPI QUALITÉ

---

## ❌ 14. Defective Units

### Définition

Nombre d’unités non conformes détectées.

### Source

dw.fact_quality_events.defective_units

---

## 🗑 15. Scrap Units

### Définition

Unités perdues définitivement.

---

## 🔁 16. Reworked Units

### Définition

Unités corrigées et réintégrées.

---

## 📉 17. Quality Rate

### Formule

```text
Quality = (actual_production - defective_units) / actual_production
```

### Interprétation

* 1.0 → zéro défaut
* < 1.0 → pertes qualité

---

## 🧨 18. Scrap Rate

### Formule

```text
Scrap Rate = scrap_units / actual_production
```

---

# 🏆 KPI GLOBAL – OEE (TRS)

---

## ⚙️ 19. Availability

### Formule

```text
Availability = (60 - non_production_minutes) / 60
```

---

## ⚡ 20. Performance

### Définition

Capacité à produire à la vitesse nominale.

### Formule

```text
Performance = actual_production / theoretical_production
```

---

## 🧪 21. Quality (OEE)

### Formule

```text
Quality = good_units / actual_production
```

---

## 🏆 22. OEE (Overall Equipment Effectiveness)

### Formule

```text
OEE = Availability × Performance × Quality
```

### Interprétation

| OEE    | Niveau              |
| ------ | ------------------- |
| > 85%  | Excellent           |
| 60–85% | Standard industriel |
| < 60%  | À améliorer         |

---

# 📊 KPI TEMPORELS (Dashboard)

---

## 📈 23. Trend KPI

### Définition

Évolution dans le temps (jour / semaine / mois)

### Exemples

* Reliability trend
* Downtime trend
* OEE trend

---

## 🔄 24. Delta KPI

### Formule

```text
Delta = KPI actuel - KPI période précédente
```

---

## 🎨 25. KPI Color Logic

| Situation    | Couleur  |
| ------------ | -------- |
| amélioration | 🟢 vert  |
| dégradation  | 🔴 rouge |
| stable       | ⚪ gris   |

---

## 🏷 26. KPI Label

### Exemple

* ↑ +2.3% vs last month
* ↓ -1.5% vs last month
* → 0.0% vs last month

---

# 🧠 Bonnes pratiques d’interprétation

* Comparer à périmètre équivalent (ligne, atelier)
* Prendre en compte pauses, nettoyages et maintenances
* Analyser les tendances avant les valeurs brutes
* Croiser systématiquement avec les événements

---

# ⚠️ Limites connues

* Données issues de mock data
* Qualité dépend du générateur
* Les causes multiples peuvent se superposer
* Certaines pertes peuvent être sous-estimées
