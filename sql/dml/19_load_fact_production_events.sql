-- ==========================================================
-- Alimentation de la table de fait DW.fact_hourly_performance
-- Grain : 1 ligne = 1 heure de production
-- Source : ops.hourly_production + dimensions DW
-- ==========================================================

INSERT INTO dw.fact_hourly_performance (
    hourly_prod_id,
    date_key,
    machine_key,
    team_key,
    shift_supervision_id,
    operator_id,
    team_lead_id,
    hour_index,
    actual_production,
    non_production_minutes,
    load_ts
)

SELECT DISTINCT
    hp.hourly_prod_id,

    -- Clé temps
    dt.date_key,

    -- Clé machine (usine + atelier + ligne)
    dm.machine_key,

    -- Clé équipe (team lead + opérateur)
    dteam.team_key,

    hp.shift_supervision_id,
    hp.operator_id,
    hp.team_lead_id,
    hp.hour_index,
    hp.actual_production,
    hp.non_production_minutes,

    CURRENT_TIMESTAMP AS load_ts

FROM ops.hourly_production hp

-- Dimension temps
JOIN dw.dim_time dt
  ON dt.date = hp.date

-- Dimension machine
JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id

-- Dimension équipe
JOIN dw.dim_team dteam
  ON dteam.team_lead_id = hp.team_lead_id
 AND dteam.operator_id = hp.operator_id

WHERE NOT EXISTS (
    SELECT 1
    FROM dw.fact_hourly_performance f
    WHERE f.hourly_prod_id = hp.hourly_prod_id
);
