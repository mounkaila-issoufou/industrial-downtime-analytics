-- ==========================================================
-- Alimentation OPS.production_events depuis STG
-- ==========================================================

INSERT INTO ops.production_events (
    event_id,
    hourly_prod_id,
    event_type,

    -- 🔥 STRUCTURE ANALYTIQUE
    cause_category,
    cause_family,
    organ,
    element,

    -- 🔥 TEMPOREL
    start_minute,
    end_minute,
    duration_minutes,

    -- 🔥 KPI
    severity,
    severity_score,
    business_impact,

    -- 🔥 OPERATIONNEL
    operator_action,
    escalation,

    -- 🔥 SMART
    is_recurrent,
    repetition_count,

    -- 🔥 META
    source,
    comment
)

SELECT DISTINCT
    s.event_id,
    s.hourly_prod_id,
    s.event_type,

    -- 🔥 ALIGNEMENT NOMENCLATURE
    s.cause_category,
    s.cause_family,
    s.organ,
    s.element,

    -- 🔥 TEMPOREL
    s.start_minute,
    s.end_minute,

    -- 🔥 GARDE-FOU
    COALESCE(s.duration_minutes, 0),

    -- 🔥 KPI
    s.severity,
    s.severity_score,
    s.business_impact,

    -- 🔥 OPERATIONNEL
    s.operator_action,
    s.escalation,

    -- 🔥 SMART
    COALESCE(s.is_recurrent, FALSE),
    COALESCE(s.repetition_count, 0),

    -- 🔥 META
    s.source,
    s.comment

FROM stg.production_events s

-- ==========================
-- FILTRES QUALITÉ (🔥 important)
-- ==========================
WHERE s.event_id IS NOT NULL
  AND s.event_type IS NOT NULL

-- ==========================
-- ANTI-DUPLICATION
-- ==========================
AND NOT EXISTS (
    SELECT 1
    FROM ops.production_events o
    WHERE o.event_id = s.event_id
);