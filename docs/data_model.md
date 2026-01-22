# Data Model

Ce document décrit le **modèle de données conceptuel et analytique** du projet *Industrial Downtime Analytics*.

L’objectif n’est pas de présenter un schéma technique exhaustif, mais d’expliquer **comment les données métiers sont structurées et exploitées** pour analyser la performance industrielle et les temps de non-production.

---
## 🎯 Objectifs du modèle de données

Le modèle de données doit permettre de :
- suivre la production **heure par heure**,
- analyser les **arrêts de ligne par cause technique ou organisationnelle**,
- comparer les performances entre **usines, ateliers, lignes et machines**,
- disposer d’une base robuste pour des analyses transverses (équipes, périodes, équipements).

Le modèle est volontairement :
- **événementiel** (event-based),
- **orienté performance industrielle**,
- **agnostique des outils BI**.

---
## 🧱 Principes de modélisation

### 1. Séparation structure / événement
Le modèle distingue clairement :
- les entités **structurelles et stables** (usines, ateliers, machines, personnes),
- les entités **dynamiques** liées à l’activité (production horaire, événements).

### 2. Granularité horaire
La **brique centrale** de l’analyse est l’heure de production.
Toutes les analyses de performance et de non-production sont ramenées à cette granularité.

### 3. Calcul de la non-production
Le temps de non-production n’est pas saisi directement.
Il est **calculé** à partir de la production réelle mesurée par le compteur emballeuse et de la capacité théorique.

---
## 🏭 Entités structurelles

### Factories
Représente les sites industriels.

### Workshops
Représente les ateliers au sein d’une usine.

### Production Lines
Représente les lignes de conditionnement.

### Machines
Représente les équipements physiques d’une ligne.

### Machine Organs
Représente les sous-ensembles fonctionnels d’une machine.

### Machine Elements
Représente les éléments techniques précis pouvant provoquer un arrêt.

Ces entités forment la **hiérarchie industrielle** du modèle.

---
## 👥 Entités organisationnelles

### Operators
Opérateurs de production (anonymisés).

### Team Leads
Chefs d’équipe assurant l’encadrement opérationnel.

### Workshop Managers
Responsables d’atelier.

### Shifts
Plages horaires de travail (matin, soir, nuit).

Ces entités permettent des analyses par **organisation du travail**, sans logique d’évaluation individuelle.

---
## ⏱️ Entités événementielles

### Hourly Production
Table centrale de mesure de la production.

Elle contient pour chaque heure :
- le compteur réel de fromages emballés,
- la capacité théorique,
- le temps de non-production calculé.

Cette table sert de **base factuelle principale**.

### Production Events
Représente les événements consignés sur les feuilles de marche :
- arrêts techniques,
- arrêts maintenance,
- changements de série,
- nettoyage,
- pauses et échauffements.

Chaque événement est décrit par :
- une catégorie,
- un libellé,
- une durée estimée,
- un commentaire libre.

---
## 🕒 Dimension temps

### Calendars
La dimension temps permet d’analyser les données selon :
- jours,
- semaines,
- mois,
- années,
- dates de shift.

Elle facilite les comparaisons temporelles et les analyses de tendances.

---
## 🔗 Logique d’association (conceptuelle)

Sans entrer dans le détail technique des clés, le modèle suit la logique suivante :

- une **heure de production** est associée à :
  - une ligne,
  - un atelier,
  - une usine,
  - un shift,
- un **événement** est rattaché à :
  - une heure,
  - une machine,
  - un organe,
  - un élément,
- les acteurs (opérateurs, chefs d’équipe) sont associés au contexte horaire.

Cette approche permet de **croiser librement les axes d’analyse**.

---
## 📊 Cas d’usage analytiques couverts

Le modèle permet de répondre à des questions telles que :
- Quels sont les principaux contributeurs au temps de non-production ?
- Quels éléments techniques génèrent le plus d’arrêts ?
- Quelles différences de performance entre ateliers ou lignes ?
- Quels types d’événements impactent le plus la cadence ?
- Comment la performance évolue dans le temps ?

---
## ⚠️ Hypothèses et limites

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

