# ⚠️ Assumptions and Limits – Industrial Production & Downtime Analytics

## 🎯 Objectif du document
Ce document explicite les **hypothèses**, **règles de gestion** et **limites connues** du projet afin de :
- garantir une interprétation correcte des analyses,
- éviter les conclusions erronées,
- cadrer le périmètre du modèle de données.

Il reflète une posture **data analyst senior** : transparente, rigoureuse et pragmatique.

---

## ✅ Hypothèses de travail

### 1. Capacité théorique constante
La capacité théorique est fixée à **4800 fromages/heure**, soit :
- 80 fromages par minute,
- dans des conditions optimales sans arrêt.

Cette valeur est considérée comme **stable** pour une ligne donnée sur la période analysée.

---

### 2. Production horaire agrégée
La production est agrégée **à l’heure** :
- les micro-arrêts (< 1 minute) sont intégrés dans la production réelle,
- les événements détaillent les causes principales de non-production.

---

### 3. Un opérateur principal par heure
Chaque heure de production est associée à :
- **un opérateur principal**
- **un chef d’équipe référent**

Même si, en réalité, plusieurs personnes peuvent intervenir ponctuellement.

---

### 4. Les événements expliquent la non-production
Les événements enregistrés dans `production_events` sont supposés :
- expliquer **la totalité ou la majorité** du temps de non-production observé sur l’heure correspondante,
- pouvoir être multiples sur une même heure.

---

### 5. Objectifs de fiabilité définis par ligne
Les objectifs de fiabilité sont :
- définis **par type de ligne / atelier**,
- constants sur la période analysée,
- stockés dans `production_line.reliability_target`.

---

### 6. Indépendance opérateur / chef d’équipe
Les opérateurs ne sont **pas hiérarchiquement liés** de manière permanente à un chef d’équipe :
- le lien est **contextuel**, via le shift,
- un opérateur peut travailler sous différents chefs d’équipe.

---

### 7. Planning standardisé des shifts
Les shifts suivent un schéma standard :
- MATIN / SOIR / NUIT en semaine,
- SD (week-end),
- sans gestion des heures supplémentaires ou des chevauchements.

---

## ⚠️ Limites connues du modèle

### 1. Saisie manuelle et approximations
Les données d’événements reposent sur :
- l’analyse de l’opérateur,
- une saisie manuelle sur feuille de marche.

👉 Les durées sont **approximatives**.

---

### 2. Granularité limitée
Le modèle ne permet pas :
- l’analyse à la minute ou à la seconde,
- la détection fine des micro-arrêts.

---

### 3. Absences et remplacements simplifiés
Les cas suivants ne sont pas modélisés :
- absences imprévues,
- remplacements en cours de shift,
- doublons opérateur sur une même heure.

---

### 4. Maintenance préventive non détaillée
La maintenance est modélisée comme un événement :
- sans distinction corrective / préventive,
- sans planification long terme.

---

### 5. Qualité produit non intégrée
Le modèle ne couvre pas :
- rebuts,
- non-conformités qualité,
- pertes matière.

---

### 6. Données multi-sites limitées
Bien que le modèle supporte plusieurs sites :
- l’analyse se concentre sur **un site (Domfront)**,
- les comparaisons inter-sites ne sont pas approfondies.

---

## 🔄 Évolutions possibles (hors périmètre actuel)

- Intégration des données qualité
- Détail des micro-arrêts
- Prise en compte des heures supplémentaires
- Historisation des objectifs de fiabilité
- Connexion à un MES / ERP
- Modélisation des équipes complètes

---

## 📌 Conclusion
Ce projet fournit une base **robuste et réaliste** pour l’analyse de la performance industrielle, tout en reconnaissant les limites inhérentes à la collecte terrain et au niveau de granularité disponible.

Ces hypothèses et limites doivent être **prises en compte dans toute interprétation des résultats**.
