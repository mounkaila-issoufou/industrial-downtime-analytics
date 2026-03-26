-- ==========================================================
-- Chargement CSV → STAGING : production_events
-- ==========================================================

TRUNCATE TABLE stg.production_events;

COPY stg.production_events (
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

    -- 🔥 SMART FEATURES
    is_recurrent,
    repetition_count,

    -- 🔥 META
    source,
    comment
)
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);