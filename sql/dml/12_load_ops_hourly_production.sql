-- ==========================================================
-- Alimentation de la table OPS.hourly_production
-- depuis STAGING
-- ==========================================================

INSERT INTO dw.fact_hourly_performance (
    time_key,
    machine_key,
    team_key,
    theoretical_production,
    actual_production,
    non_production_minutes,
    explained_minutes,
    unexplained_minutes,
    reliability_rate,
    explained_ratio,
    unexplained_ratio,
    load_timestamp
)

SELECT
    dt.time_key,
    dm.machine_key,
    dteam.team_key,
    hp.theoretical_production,
    hp.actual_production,
    hp.non_production_minutes,
    hp.explained_minutes,
    hp.unexplained_minutes,
    hp.reliability_rate,
    hp.explained_ratio,
    hp.unexplained_ratio,
    CURRENT_TIMESTAMP

FROM ops.hourly_production hp
JOIN dw.dim_time dt
  ON dt.date = hp.date
JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id
JOIN dw.dim_team dteam
  ON dteam.team_lead_id = hp.team_lead_id

ON CONFLICT (time_key, machine_key, team_key)
DO UPDATE SET
    theoretical_production = EXCLUDED.theoretical_production,
    actual_production = EXCLUDED.actual_production,
    non_production_minutes = EXCLUDED.non_production_minutes,
    explained_minutes = EXCLUDED.explained_minutes,
    unexplained_minutes = EXCLUDED.unexplained_minutes,
    reliability_rate = EXCLUDED.reliability_rate,
    explained_ratio = EXCLUDED.explained_ratio,
    unexplained_ratio = EXCLUDED.unexplained_ratio,
    load_timestamp = CURRENT_TIMESTAMP;

