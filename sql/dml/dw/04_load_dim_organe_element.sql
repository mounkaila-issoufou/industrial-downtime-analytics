-- ==========================================================
-- Alimentation de la dimension ORGANE / ÉLÉMENT (DW)
-- Source : ops.production_events
-- ==========================================================

INSERT INTO dw.dim_organe_element (
    organe,
    element,
    cause_category,
    cause_family,
    valid_from,
    is_current
)
SELECT DISTINCT
    pe.organ,
    pe.element,

    -- Classification minimale basée sur event_type
    pe.event_type AS cause_category,

    NULL AS cause_family,

    CURRENT_TIMESTAMP,
    TRUE

FROM ops.production_events pe

ON CONFLICT DO NOTHING;
