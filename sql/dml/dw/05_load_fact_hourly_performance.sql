-- ==========================================================
-- Chargement fact_hourly_performance (DW)
-- CORRECTION :
--   - time_key aligné avec fact_production_events
--   - gestion shift nuit + passage minuit
--   - suppression dépendance (date + hour_index direct)
-- ==========================================================

INSERT INTO dw.fact_hourly_performance (
    time_key,
    machine_key,
    team_key,
    hour_index,
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

    hp.hour_index,
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

-- ==========================================================
-- ✅ BASE HOUR (cohérent avec events)
-- ==========================================================
JOIN (
    SELECT
        hp.*,
        CASE 
            WHEN hp.session = 'MATIN' THEN 5
            WHEN hp.session = 'SOIR'  THEN 13
            WHEN hp.session = 'NUIT'  THEN 21
            WHEN hp.session = 'SD'    THEN 6
        END AS base_hour
    FROM ops.hourly_production hp
) hp_base
  ON hp_base.hourly_prod_id = hp.hourly_prod_id

-- ==========================================================
-- ✅ DIM_TIME JOIN SUR TIME_KEY (IMPORTANT)
-- ==========================================================
JOIN dw.dim_time dt
  ON dt.time_key =
(
    TO_CHAR(
        CASE 
            WHEN hp_base.base_hour + hp.hour_index >= 24
                THEN hp.date + INTERVAL '1 day'
            ELSE hp.date
        END,
        'YYYYMMDD'
    )::INT * 100
    +
    ((hp_base.base_hour + hp.hour_index) % 24)
)

JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id

JOIN (
    SELECT DISTINCT
        team_lead_id,
        session,
        scope_line_id,
        team_key
    FROM dw.dim_team
) dteam
  ON dteam.team_lead_id = hp.team_lead_id
 AND dteam.session = hp.session
 AND dteam.scope_line_id = hp.line_id

ON CONFLICT (time_key, machine_key, team_key)
DO NOTHING;