

-- ==========================================================
-- Chargement de la fact_production_events (DW)
-- ==========================================================

INSERT INTO dw.fact_production_events (
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
    dt.time_key,
    dm.machine_key,
    dteam.team_key,
    doe.organe_element_key,
    de.event_key,
    pe.duration_minutes,
    pe.severity_score,
    pe.is_recurrent,

    -- Flags analytiques (source = données métier fiables)
    CASE 
        WHEN pe.cause_category = 'technical' THEN TRUE
        ELSE FALSE
    END AS is_failure,

    CASE 
        WHEN pe.cause_category = 'micro_stop' THEN TRUE
        ELSE FALSE
    END AS is_micro_stop,

    CASE 
        WHEN pe.cause_category = 'quality' THEN TRUE
        ELSE FALSE
    END AS is_quality_loss,

    CURRENT_TIMESTAMP
FROM ops.production_events pe
JOIN ops.hourly_production hp
  ON hp.hourly_prod_id = pe.hourly_prod_id
-- Dimension temps
JOIN dw.dim_time dt
  ON dt.date = hp.date
 AND dt.hour_of_day = hp.hour_index
-- Dimension machine
JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id
-- Dimension équipe
JOIN dw.dim_team dteam
  ON dteam.team_lead_id = hp.team_lead_id
-- Dimension organe / élément
JOIN dw.dim_organe_element doe
  ON doe.organe = pe.organ
 AND doe.element = pe.element
-- Dimension événement
JOIN dw.dim_event de
  ON de.event_type = pe.event_type
-- Anti-duplication
ON CONFLICT (time_key, machine_key, team_key, organe_element_key, event_key) DO NOTHING;