# Analyse globale des performances du service conditionnement d'une société fromagère industriel

## 🎯 Objectif du projet
Ce projet vise à mettre en place une **analyse globale, transverse et structurée** de la performance des ateliers de conditionnement industriel, en s’appuyant sur les **feuilles de marche opérateur** et les **compteurs de production**.

L’objectif est de suivre, comparer et analyser :
- l’ensemble des **ateliers**,
- toutes les **lignes et machines**,
- tous les **opérateurs, chefs d’équipe et responsables**,
- l’ensemble des **événements impactant la production**.

Le projet transforme une donnée terrain **manuelle, locale et opérationnelle** en une **vision analytique consolidée**, exploitable pour le **pilotage industriel** et l’**amélioration continue**.

---

## 🏭 Contexte industriel
- **Secteur** : industrie agroalimentaire (conditionnement fromager)
- **Ateliers** : ovales, camembert, portions
- **Équipements** : empileur / dépileur, emballeuse, encaisseuse
- **Organisation** : équipes matin / soir / nuit / SD (samedi, dimanche)

Chaque ligne fonctionne avec une **cadence théorique optimale** de :
- **80 fromages par minute**
- **4 800 fromages par heure** (condition sans arrêt)

Lorsqu’un arrêt survient, le système de pilotage indique l’**organe** et l’**élément** en cause.  
L’opérateur intervient directement sur la machine, puis consigne l’événement sur une **feuille de marche**.

---

## 📄 Source et nature des données

Les données analysées sont issues de **feuilles de marche opérateur**, renseignées **heure par heure**.

Chaque feuille contient :
- les **heures de production**,
- le **compteur emballeuse** (nombre réel de fromages emballés par heure),
- les **événements d’arrêt**, décrits par :
  - atelier,
  - ligne,
  - machine,
  - organe,
  - élément,
- la **durée approximative** des interventions,
- des **commentaires libres** en cas d’événements non répertoriés,
- les opérations normales : pause, break, échauffement, nettoyage, pilotage.

Les données présentes dans ce repository sont des **mock data réalistes**, reconstruites à partir de ce fonctionnement réel, sans exposition de données sensibles.

---

## 🧠 Principe de mesure de la non-production

Le temps de non-production n’est pas saisi directement.  
Il est **calculé** à partir de l’écart entre la production théorique et la production réelle.

Pour chaque heure :

**Temps de non-production (minutes) = (4 800 – compteur emballeuse) / 80**


Ce temps peut être expliqué par :
- des arrêts techniques (au niveau organe / élément),
- des arrêts organisationnels (approvisionnement, changements),
- des opérations normales (pause, nettoyage, échauffement),
- des arrêts maintenance.

Les événements enregistrés permettent de **qualifier et analyser** ces pertes de production.

---

## 🧩 Périmètre d’analyse

L’analyse couvre de manière globale :
- tous les **ateliers**,
- toutes les **lignes de conditionnement**,
- toutes les **machines**,
- l’ensemble des **organes et éléments techniques**,
- tous les **acteurs opérationnels** (opérateurs, chefs d’équipe, responsables).

L’objectif n’est pas l’évaluation individuelle, mais la **compréhension systémique** de la performance industrielle.

---

## 🧠 Démarche analytique

1. Compréhension du fonctionnement terrain
2. Structuration des données issues des feuilles de marche
3. Normalisation des événements et de la nomenclature
4. Modélisation analytique multi-ateliers et multi-lignes
5. Analyse du temps de non-production et des causes racines
6. Comparaisons transverses (ateliers, machines, équipes, périodes)
7. Restitution via indicateurs et dashboards décisionnels

---

## 📂 Organisation du repository

Le projet suit une architecture **modulaire, lisible et reproductible** :

- `data/` : données brutes, traitées et curatées  
- `notebooks/` : exploration, préparation, modélisation et analyse  
- `src/` : logique Python réutilisable (ingestion, nettoyage, modélisation)  
- `sql/` : schémas, tables analytiques et requêtes  
- `docs/` : documentation métier, data et hypothèses  
- `dashboards/` : description des tableaux de bord  

---

## 📊 Résultats attendus

- Vision consolidée de la performance industrielle
- Identification des principaux contributeurs au temps de non-production
- Analyse des écarts entre ateliers, lignes et machines
- Aide à la priorisation des actions d’amélioration continue

---

## ⚠️ Limites

- Données issues de saisies manuelles (durées estimées)
- Granularité horaire
- Micro-arrêts non systématiquement tracés

Ces limites sont **documentées et prises en compte** dans l’interprétation des résultats.

---

## 👤 Auteur
Projet de portfolio **Data Analyst senior** – Orientation **industrie**, **performance opérationnelle** et **pilotage data-driven**.  
Basé sur mon expérience en tant que **pilote de ligne de production**, appliquée à ma vision du métier de Data Analyst.

