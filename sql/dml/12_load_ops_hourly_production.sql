-- ==========================================================
-- Alimentation de la table OPS.hourly_production
-- depuis STAGING
-- ==========================================================

INSERT INTO ops.hourly_production (
    hourly_prod_id,
    shift_supervision_id,
    operator_id,
    team_lead_id,
    line_id,
    date,
    session,
    hour_index,
    hour_timestamp,
    theoretical_production,
    actual_production,
    non_production_minutes
)
SELECT DISTINCT
    s.hourly_prod_id,
    s.shift_supervision_id,
    s.operator_id,
    s.team_lead_id,
    s.line_id,
    s.date,
    s.session,
    s.hour_index,

    -- reconstruire un vrai timestamp horaire
    (s.date + (s.hour_index || ' hours')::interval) AS hour_timestamp,

    -- règle métier cohérente avec ton mock (4800 pièces / heure)
    4800 AS theoretical_production,

    s.actual_production,
    s.non_production_minutes

FROM stg.hourly_production s
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.hourly_production o
    WHERE o.hourly_prod_id = s.hourly_prod_id
);
