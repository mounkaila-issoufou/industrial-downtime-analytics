-- ==========================================================
-- Alimentation de la dimension ORGANE / ÉLÉMENT (DW)
-- Source : ops.production_events
-- ==========================================================

INSERT INTO dw.dim_organe_element (
    event_type,
    organe,
    element,
    event_category,
    valid_from,
    is_current
)
SELECT DISTINCT
    pe.event_type,
    pe.organ,
    pe.element,
    pe.event_category,

    CURRENT_TIMESTAMP,
    TRUE

FROM ops.production_events pe

ON CONFLICT DO NOTHING;
