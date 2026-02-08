-- ==========================================================
-- Alimentation de la dimension ORGANE / ÉLÉMENT (DW)
-- Source : ops.production_events
-- ==========================================================

INSERT INTO dw.dim_organe_element (
    organe_element_key,
    organe,
    element,
    cause_category,
    cause_family,
    valid_from,
    is_current
)
SELECT DISTINCT
    -- Clé analytique stable et lisible
    pe.event_type AS organe_element_key,

    -- Décomposition métier (proxy à partir de event_type dans ton mock)
    SPLIT_PART(pe.event_type, '_', 1) AS organe,
    SPLIT_PART(pe.event_type, '_', 2) AS element,

    pe.event_category AS cause_category,

    CASE 
        WHEN pe.event_category = 'technical' THEN 'Technique'
        WHEN pe.event_category = 'planned'   THEN 'Organisation'
        ELSE 'Autre'
    END AS cause_family,

    CURRENT_TIMESTAMP AS valid_from,
    TRUE AS is_current

FROM ops.production_events pe

WHERE NOT EXISTS (
    SELECT 1
    FROM dw.dim_organe_element d
    WHERE d.organe_element_key = pe.event_type
);
