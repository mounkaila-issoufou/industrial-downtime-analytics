# Downtime Investigation — Documentation Produit

> **Moteur de diagnostic industriel.** Non un tableau de bord de reporting.

---

## Objectif

| Détecter | Comprendre | Diagnostiquer | Agir |
|---|---|---|---|
| Identifier les causes racines | Analyser le comportement système | Repérer les patterns temporels | Appuyer la décision opérationnelle |

---

## Architecture globale

### 1. En-tête

- **Titre** : Downtime Investigation
- **Sous-titre** : Drill into root causes, patterns and operational drivers

### 2. Panneau de filtres

```
Workshop  ·  Line  ·  Machine  ·  Date
```

**Rôle** : Réduire le périmètre d'analyse et isoler le contexte opérationnel.

### 3. Système KPI

Indicateurs de premier niveau servant de **déclencheurs d'anomalie** — signal d'alerte initial : *quelque chose ne va pas*.

---

## Grille analytique principale

### 4.1 — Structure des pertes `(50% gauche)`

#### Treemap — Drivers primaires de downtime

**Objectif** : Comprendre la distribution du downtime. Focalisation sur la **structure**, non le classement.

| Paramètre | Valeur |
|---|---|
| Visuel | Treemap |
| Groupe | `dim_event[cause_category]` |
| Détail | `dim_event[event_type]` |
| Mesure | `[Total Downtime]` |

**Logique couleur (style Pareto)**

```dax
Cumulative Downtime % =
DIVIDE(
    CALCULATE(
        [Total Downtime],
        FILTER(
            ALL(dim_event[event_type]),
            [Total Downtime] >= EARLIER([Total Downtime])
        )
    ),
    [Total Downtime]
)

Downtime Driver Color =
IF(
    [Cumulative Downtime %] <= 0.8,
    "#F77F00",   -- Drivers critiques
    "#B0BEC5"    -- Résiduel
)
```

**Lecture** : grands blocs → pertes dominantes · fragmentation → problème systémique.

---

#### Histogramme — Distribution des événements

**Objectif** : Caractériser la nature des arrêts.

| Axe X | Axe Y |
|---|---|
| `duration_minutes` (bins) | `COUNT(events)` |

| Pattern | Interprétation |
|---|---|
| Nombreuses petites barres | Micro-arrêts |
| Queue longue | Défaillances majeures |
| Distribution équilibrée | Système mixte |

---

### 4.2 — Analyse des patterns `(50% droite)`

#### Heatmap — Machine × Heure

**Objectif** : détecter les anomalies temporelles, identifier l'instabilité machine, révéler les patterns cachés.

| Paramètre | Valeur |
|---|---|
| Visuel | Matrix |
| Lignes | `dim_machine[machine_name]` |
| Colonnes | `dim_time[Hour Label]` ⚠️ colonne, pas mesure |
| Mesure | `[Total Downtime]` |

**Colonne `Hour Label` (obligatoire)**

```dax
Hour Label =
FORMAT(
    TIME('dw dim_time'[hour_of_day], 0, 0),
    "HH:mm"
)
```

**Échelle de couleur** : faible → clair · élevé → rouge foncé.

| Pattern visuel | Diagnostic |
|---|---|
| Colonne marquée | Problème machine |
| Ligne marquée | Problème temporel |
| Point chaud isolé | Zone critique |

---

#### Heatmap — Jour × Shift *(optionnel — niveau avancé)*

| Lignes | Colonnes | Mesure |
|---|---|---|
| Date | Shift | Downtime |

**Cas d'usage** : détecter des problèmes d'équipe ou d'inefficacités organisationnelles.

---

## 5. Évolution temporelle `(pleine largeur)`

**Objectif** : analyser les tendances, évaluer la stabilité, détecter les dérives.

| Axe | Mesure | Légende |
|---|---|---|
| Date | Downtime | `cause_category` (optionnel) |

**Version avancée** : small multiples par machine · une ligne par cause.

---

## 6. Journal des événements `(table — critique)`

> Si ce n'est pas dans la table → ça n'existe pas.

**Colonnes requises**

| Date | Machine | Event Type | Cause Category | Duration | Severity | Operator Action |
|---|---|---|---|---|---|---|

---

## 7. Panneau d'insight dynamique *(avancé)*

**Objectif** : expliquer automatiquement la sélection courante.

**Exemple de sortie**

```
Top Cause       : Mechanical Failure
Contribution    : 42%
Avg Duration    : 18 min
Main Machine    : Line 2
Peak Hour       : 14:00
Dominant Shift  : Night
```

**Mesures DAX associées**

```dax
Selected Cause =
SELECTEDVALUE(dim_event[event_type], "Multiple")

Selected Contribution =
[Top Cause Contribution (%)]
```

---

## Design system

### Palette

| Usage | Hex |
|---|---|
| Critical | `#C62828` |
| Warning | `#F9A825` |
| Neutral | `#B0BEC5` |
| Highlight | `#F77F00` |

### Typographie

| Niveau | Style |
|---|---|
| Valeurs KPI | Bold |
| Labels | Medium |
| Insights | Light |

### Espacement

Grilles à **12–16 px** · alignement strict sur colonne.

---

## Erreurs courantes

| ❌ Anti-pattern | Impact |
|---|---|
| Ranking au lieu de structure | Perd la vue systémique |
| Heatmap sans contexte | Lecture impossible |
| Absence de tooltips | Friction utilisateur |
| Pas de données événement | Pas de diagnostic terrain |
| Visuels surchargés | Perte de signal |

---

## Flux utilisateur

```
1 · DÉTECTER    →  KPI row          "Quelque chose ne va pas"
2 · COMPRENDRE  →  Treemap + Histo  "Quel type de problème ?"
3 · LOCALISER   →  Heatmap          "Où / Quand ?"
4 · CONFIRMER   →  Event table      "Que s'est-il passé exactement ?"
5 · AGIR        →  Insight panel    "Que dois-je corriger ?"
```

---

## Statut

| Critère | État |
|---|---|
| Reproductible | ✅ |
| Couverture analytique complète | ✅ |
| Design production-grade | ✅ |
| Niveau Senior / Lead | ✅ |

---

> **Ce n'est pas un dashboard.**
> **C'est un système de diagnostic industriel.**