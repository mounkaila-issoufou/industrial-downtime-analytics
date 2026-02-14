-- ==========================================================
-- Fait analytique : Performance horaire de production
-- Grain : 1 ligne = 1 heure x 1 ligne x 1 équipe
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

-- Dimension temps
JOIN dw.dim_time dt
  ON dt.date = hp.date

-- Dimension machine
JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id

-- Dimension équipe
JOIN dw.dim_team dteam
  ON dteam.team_lead_id = hp.team_lead_id

WHERE NOT EXISTS (
    SELECT 1
    FROM dw.fact_hourly_performance f
    WHERE f.time_key = dt.time_key
      AND f.machine_key = dm.machine_key
      AND f.team_key = dteam.team_key
);
