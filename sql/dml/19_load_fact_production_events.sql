-- ==========================================================
-- Chargement de la fact_production_events
-- ==========================================================

INSERT INTO dw.fact_production_events (
    time_key,
    machine_key,
    team_key,
    organe_element_key,
    duration_minutes,
    load_timestamp
)

SELECT DISTINCT
    dt.time_key,
    dm.machine_key,
    dteam.team_key,
    doe.organe_element_key,
    pe.duration_minutes,
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

ON CONFLICT DO NOTHING;
