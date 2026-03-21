-- ==========================================================
-- Load FACT QUALITY EVENTS (corrigé PRO)
-- ==========================================================

INSERT INTO dw.fact_quality_events (
    quality_event_id,
    time_key,
    machine_key,
    team_key,
    defect_key,
    defective_units,
    scrap_units,
    reworked_units,
    load_timestamp
)

SELECT
    qe.quality_event_id,
    dt.time_key,
    dm.machine_key,
    dteam.team_key,
    dq.defect_key,
    qe.defective_units,
    qe.scrap_units,
    qe.reworked_units,
    CURRENT_TIMESTAMP

FROM ops.quality_event qe

-- 🔗 1. Lien vers inspection
JOIN ops.quality_inspection qi
  ON qi.inspection_id = qe.inspection_id

-- 🔗 2. Lien vers production horaire
JOIN ops.hourly_production hp
  ON hp.hourly_prod_id = qi.hourly_prod_id

-- ⏱️ DIM TIME
JOIN dw.dim_time dt
  ON dt.date = hp.date
 AND dt.hour_of_day = hp.hour_index

-- 🏭 DIM MACHINE
JOIN dw.dim_machine dm
  ON dm.line_id = hp.line_id

-- 👥 DIM TEAM (⚠️ join complet !)
JOIN dw.dim_team dteam
  ON dteam.team_lead_id = hp.team_lead_id
 AND dteam.session = hp.session
 AND dteam.scope_line_id = hp.line_id

-- 🧪 DIM DEFECT
JOIN dw.dim_quality_defect dq
  ON dq.defect_category = qe.defect_category
 AND dq.defect_family   = qe.defect_family
 AND dq.defect_type     = qe.defect_type

-- 🛡️ IDEMPOTENCE
-- ON CONFLICT (quality_event_id) DO NOTHING;
