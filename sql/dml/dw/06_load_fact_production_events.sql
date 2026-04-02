-- ==========================================================
-- Chargement de la fact_production_events (DW)
-- CORRECTION :
--   - Alignement strict avec dim_time
--   - Gestion passage minuit (NUIT)
--   - Même logique de time_key = ZERO mismatch
-- ==========================================================

INSERT INTO dw.fact_production_events (
    event_id,
    time_key,
    machine_key,
    team_key,
    organe_element_key,
    event_key,
    duration_minutes,
    severity_score,
    is_recurrent,
    is_failure,
    is_micro_stop,
    is_quality_loss,
    load_timestamp
)
SELECT
    pe.event_id,

    -- ==========================
    -- ✅ TIME KEY CORRECT (IDENTIQUE À DIM_TIME)
    -- ==========================
    (
        TO_CHAR(
            CASE 
                WHEN base_hour + hp.hour_index >= 24
                    THEN hp.date + INTERVAL '1 day'
                ELSE hp.date
            END,
            'YYYYMMDD'
        )::INT * 100
        +
        ((base_hour + hp.hour_index) % 24)
    ) AS time_key,

    dm.machine_key,
    dteam.team_key,
    doe.organe_element_key,
    de.event_key,

    pe.duration_minutes,
    pe.severity_score,
    pe.is_recurrent,

    (pe.cause_category = 'technical') AS is_failure,
    (pe.cause_category = 'micro_stop') AS is_micro_stop,
    (pe.cause_category = 'quality') AS is_quality_loss,

    CURRENT_TIMESTAMP

FROM ops.production_events pe

-- ==========================
-- ✅ BASE HOUR CENTRALISÉ
-- ==========================
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
) hp
  ON hp.hourly_prod_id = pe.hourly_prod_id

JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id

JOIN dw.dim_team dteam
  ON dteam.team_lead_id = hp.team_lead_id

JOIN dw.dim_organe_element doe
  ON doe.organe = pe.organ
 AND doe.element = pe.element

JOIN dw.dim_event de
  ON de.event_type = pe.event_type

ON CONFLICT (event_id, time_key) DO NOTHING;