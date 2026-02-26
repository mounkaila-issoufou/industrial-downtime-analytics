
📊 PAGE 1 — Vue exécutive (Executive Overview)

🎯 Objectif : compréhension en ≤ 30 secondes

Structure globale
┌──────────────────────────────────────────────┐
│ Header (Titre + filtres globaux)              │ 1 ligne
├──────────────────────────────────────────────┤
│ KPI | KPI | KPI | KPI | KPI | KPI             │ 2 lignes
├───────────────────────────┬──────────────────┤
│ Trend Production          │ Reliability      │
│ (vs Théorique)            │ & Availability   │ 3 lignes
├───────────────────────────┴──────────────────┤
│ Key Insights / Commentary                     │ 2 lignes
└──────────────────────────────────────────────┘

Détail par zone
🔹 Header (Colonnes 1–12 | Ligne 1)

Titre : Industrial Performance Overview

Filtres (droite) :

Date

Ligne de production

Machine (optionnel)

🔹 Bande KPIs (Colonnes 1–12 | Lignes 2–3)
KPI	Col	Type
Reliability %	1–2	Card
Availability %	3–4	Card
Total Production	5–6	Card
Production Gap	7–8	Card
MTTR	9–10	Card
MTBF	11–12	Card

📌 Règles :

1 KPI = 1 carte

Valeur + delta (vs période précédente)

Couleur uniquement si seuil critique

🔹 Graphiques centraux (Lignes 4–6)

Gauche (Colonnes 1–7)
➡️ Line chart :

Production réelle vs théorique

Rolling 30J

Droite (Colonnes 8–12)
➡️ Combo chart :

Availability %

Reliability %

🔹 Insights (Lignes 7–8 | Colonnes 1–12)

➡️ Zone texte :

2–3 phrases dynamiques

Exemple :

Reliability decreased by 4% over the last 14 days, mainly driven by Line B downtime.