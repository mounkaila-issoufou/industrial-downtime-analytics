# Data Dictionary

Ce document décrit les tables et champs utilisés dans le projet **Industrial Downtime Analytics**.  
Les noms techniques des tables et colonnes sont en anglais, les descriptions métier en français.

---
## 1. factories
Représente les sites industriels.

| Champ | Type | Description |
|------|-----|-------------|
| factory_id | string | Identifiant unique de l’usine |
| factory_name | string | Nom de l’usine (FLERS, DOMFRONT, VIRE_NORMANDIE) |
| city | string | Ville de l’usine |
| country | string | Pays |
| status | string | Statut de l’usine (active / inactive) |

---
## 2. workshops
Représente les ateliers de production.

| Champ | Type | Description |
|------|-----|-------------|
| workshop_id | string | Identifiant unique de l’atelier |
| workshop_name | string | Nom de l’atelier (OVALES, CAMEMBERT, PORTION) |
| workshop_type | string | Type d’atelier |

---
## 3. shifts
Représente les équipes horaires.

| Champ | Type | Description |
|------|-----|-------------|
| shift_id | string | Identifiant du shift |
| shift_name | string | Nom du shift (MORNING, EVENING, NIGHT) |
| start_time | time | Heure de début |
| end_time | time | Heure de fin |

---
## 4. operators
Représente les opérateurs de production (anonymisés).

| Champ | Type | Description |
|------|-----|-------------|
| operator_id | string | Identifiant anonymisé de l’opérateur |
| seniority_years | integer | Ancienneté en années |
| contract_type | string | Type de contrat |
| active_flag | boolean | Opérateur actif ou non |

---
## 5. team_leads
Représente les chefs d’équipe.

| Champ | Type | Description |
|------|-----|-------------|
| team_lead_id | string | Identifiant du chef d’équipe |
| experience_years | integer | Années d’expérience |
| active_flag | boolean | Statut actif |

---
## 6. workshop_managers
Représente les responsables d’atelier.

| Champ | Type | Description |
|------|-----|-------------|
| manager_id | string | Identifiant du responsable |
| role_level | string | Niveau de responsabilité |
| active_flag | boolean | Statut actif |

---
## 7. production_lines
Représente les lignes de conditionnement.

| Champ | Type | Description |
|------|-----|-------------|
| line_id | string | Identifiant de la ligne |
| line_name | string | Nom de la ligne |
| line_type | string | Type de ligne |
| status | string | Statut de la ligne |

---
## 8. machines
Représente les machines composant une ligne.

| Champ | Type | Description |
|------|-----|-------------|
| machine_id | string | Identifiant de la machine |
| machine_name | string | Nom de la machine |
| machine_type | string | Type de machine (empileur, emballeuse, encaisseuse) |

---
## 9. machine_organs
Représente les organes d’une machine.

| Champ | Type | Description |
|------|-----|-------------|
| organ_id | string | Identifiant de l’organe |
| organ_name | string | Nom de l’organe |

---
## 10. machine_elements
Représente les éléments techniques causant des arrêts.

| Champ | Type | Description |
|------|-----|-------------|
| element_id | string | Identifiant de l’élément |
| element_name | string | Nom de l’élément (défaut porte, capteur, convoyeur, etc.) |

---
## 11. event_types
Catégorise les événements.

| Champ | Type | Description |
|------|-----|-------------|
| event_type_id | string | Identifiant du type d’événement |
| event_category | string | Catégorie (arrêt technique, maintenance, pause, nettoyage, changement) |

---
## 12. production_events
Événements déclarés sur les feuilles de marche.

| Champ | Type | Description |
|------|-----|-------------|
| event_id | string | Identifiant de l’événement |
| event_label | string | Libellé de l’événement |
| event_comment | string | Commentaire libre |
| estimated_duration_minutes | integer | Durée estimée de l’intervention |

---
## 13. hourly_production
Mesure horaire de la production.

| Champ | Type | Description |
|------|-----|-------------|
| production_id | string | Identifiant de la mesure |
| hour_timestamp | datetime | Heure de référence |
| wrapper_counter | integer | Nombre réel de fromages emballés |
| theoretical_capacity | integer | Capacité théorique (4800 / heure) |
| non_production_minutes | float | Temps de non-production calculé |

---
## 14. calendars
Dimension temps.

| Champ | Type | Description |
|------|-----|-------------|
| date | date | Date |
| day | integer | Jour du mois |
| week | integer | Numéro de semaine |
| month | integer | Mois |
| year | integer | Année |
| shift_date | date | Date associée au shift |

---
## Remarques
- Les durées sont estimées par les opérateurs
- Les données sont à granularité horaire
- Les micro-arrêts peuvent ne pas être tracés

Ce dictionnaire sert de référence fonctionnelle et analytique pour l’ensemble du projet.

