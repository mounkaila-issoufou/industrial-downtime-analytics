-- ==========================================================
-- Chargement du CSV dans la zone STAGING : hourly_production
-- ==========================================================
COPY stg.hourly_production (
    hourly_prod_id,
    date,
    session,
    shift_supervision_id,
    operator_id,
    team_lead_id,
    workshop_id,
    line_id,
    hour_index,
    theoretical_production,
    actual_production,
    non_production_minutes,
    explained_minutes,
    unexplained_minutes,
    reliability_rate,
    explained_ratio,
    unexplained_ratio
)
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ','
);
