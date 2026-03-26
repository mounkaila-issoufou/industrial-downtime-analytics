-- ==========================================================
-- Alimentation de la dimension ORGANE / ÉLÉMENT (DW)
-- Source : ops.production_events
-- ==========================================================

INSERT INTO dw.dim_organe_element (
    organe,
    element,
    valid_from,
    is_current
)
SELECT DISTINCT
    pe.organ,
    pe.element,
    CURRENT_TIMESTAMP,
    TRUE
FROM ops.production_events pe
ON CONFLICT (organe, element) DO NOTHING;