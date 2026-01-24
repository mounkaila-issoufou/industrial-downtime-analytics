# 📊 KPI Definitions – Industrial Production & Downtime Analytics

## 🎯 Objectif du document
Ce document définit les **indicateurs clés de performance (KPI)** utilisés pour analyser la performance des lignes de conditionnement fromager.

Les KPI permettent :
- de mesurer la fiabilité et la performance réelle,
- d’identifier les causes de non-production,
- de comparer les performances entre lignes, ateliers, shifts et équipes,
- d’aider à la prise de décision opérationnelle.

---

## ⏱️ 1. Production théorique horaire

### Nom
**Production théorique horaire**

### Définition
Quantité maximale de fromages pouvant être emballés en une heure en conditions optimales.

### Formule
Production théorique = 4800 fromages / heure


### Source
- Référentiel industriel
- Table : `production_line.theoretical_capacity_per_hour`

---

## 📦 2. Production réelle horaire

### Nom
**Production réelle horaire**

### Définition
Nombre réel de fromages emballés sur une heure donnée.

### Source
- Compteur de l’emballeuse
- Table : `hourly_production.actual_production`

---

## ⏳ 3. Temps de non-production

### Nom
**Temps de non-production (minutes)**

### Définition
Temps pendant lequel la ligne n’a pas produit sur une heure donnée.

### Formule
Non-production (min) =
(Production théorique - Production réelle) / 80


*(80 fromages/minute)*

### Source
- Calcul analytique
- Table : `hourly_production.non_production_minutes`

---

## 📉 4. Taux de fiabilité horaire

### Nom
**Fiabilité horaire (%)**

### Définition
Rapport entre la production réelle et la production théorique sur une heure donnée.

### Formule
Fiabilité (%) =
(Production réelle / Production théorique) × 100


### Source
- Table : `hourly_production`

---

## 🕒 5. Fiabilité par shift

### Nom
**Fiabilité par service**

### Définition
Fiabilité moyenne calculée sur l’ensemble des heures d’un shift.

### Formule
Fiabilité shift = Σ Production réelle / Σ Production théorique


### Dimensions d’analyse
- Ligne
- Atelier
- Opérateur
- Chef d’équipe
- Session (MATIN / SOIR / NUIT / SD)

---

## 🎯 6. Objectif de fiabilité

### Nom
**Objectif de fiabilité**

### Définition
Seuil de performance attendu pour une ligne donnée.

### Valeurs de référence
| Atelier | Objectif |
|---|---|
| Ovale (ms) | 65 % |
| Ovale (es50, x, y, z) | 60 % |
| Camembert | 50 % |
| Entier | 67 % |
| Portion | 89 % |

### Source
- Table : `production_line.reliability_target`

---

## ⚠️ 7. Écart à l’objectif

### Nom
**Écart à l’objectif de fiabilité**

### Définition
Différence entre la fiabilité réelle et l’objectif défini.

### Formule
Écart = Fiabilité réelle - Objectif de fiabilité



### Interprétation
- Écart positif → performance conforme ou supérieure
- Écart négatif → sous-performance

---

## 🚨 8. Nombre d’arrêts par heure

### Nom
**Nombre d’événements d’arrêt**

### Définition
Nombre d’événements enregistrés sur une heure de production.

### Source
- Table : `production_events`

---

## 🧩 9. Temps cumulé d’arrêt par cause

### Nom
**Temps d’arrêt par cause**

### Définition
Durée totale des arrêts regroupés par type, organe ou élément.

### Dimensions d’analyse
- event_type
- organ
- element
- session
- ligne

---

## 👥 10. Performance opérateur (contextualisée)

### Nom
**Fiabilité opérateur**

### Définition
Fiabilité moyenne calculée sur les heures réellement travaillées par un opérateur, en tenant compte :
- de la ligne,
- du shift,
- du chef d’équipe.

### Note importante
Ce KPI **n’est jamais interprété isolément**.

---

## 🧑‍💼 11. Performance chef d’équipe

### Nom
**Fiabilité par chef d’équipe**

### Définition
Fiabilité moyenne observée sur les shifts supervisés par un chef d’équipe donné.

### Source
- `shift_supervision`
- `hourly_production`

---

## 🧠 Bonnes pratiques d’interprétation

- Comparer à périmètre équivalent (ligne, atelier)
- Prendre en compte pauses, nettoyages et maintenances
- Analyser les tendances avant les valeurs brutes
- Croiser systématiquement avec les événements

---

## ⚠️ Limites connues

- Données issues de saisies manuelles (approximations possibles)
- Les causes multiples peuvent se superposer sur une même heure
- Le contexte humain influence fortement la performance

---

## 📌 Conclusion
Ces KPI fournissent une vision **factuelle, contextualisée et actionnable** de la performance industrielle, en reliant le terrain, les machines et les équipes.

Ils constituent une base solide pour :
- le pilotage opérationnel,
- l’amélioration continue,
- la valorisation data des feuilles de marche.
