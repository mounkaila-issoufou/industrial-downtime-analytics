-- ==========================================================
-- Alimentation de la dimension dim_event (DW)
-- Source : ops.production_events
-- ==========================================================

INSERT INTO dw.dim_event (
    event_type,
    cause_category,
    cause_family,
    severity,
    business_impact,
    is_planned,
    is_technical
)
SELECT DISTINCT
    pe.event_type,
    pe.cause_category,   -- Technique / Process / Quality / Organization
    pe.cause_family,

    -- ======================
    -- Flags métier / KPI
    -- ======================
    CASE 
        WHEN pe.duration_minutes <= 3 THEN 'minor'
        WHEN pe.duration_minutes <= 10 THEN 'medium'
        ELSE 'critical'
    END AS severity,

    CASE 
        WHEN pe.duration_minutes <= 3 THEN 'low'
        WHEN pe.duration_minutes <= 10 THEN 'medium'
        ELSE 'high'
    END AS business_impact,

    -- est-ce un arrêt planifié ?
    CASE 
        WHEN pe.cause_category = 'Planned' THEN TRUE
        ELSE FALSE
    END AS is_planned,

    -- est-ce un événement technique ?
    CASE 
        WHEN pe.cause_category = 'Technical' THEN TRUE
        ELSE FALSE
    END AS is_technical

FROM ops.production_events pe

-- Anti-duplication
ON CONFLICT (event_type) DO NOTHING;