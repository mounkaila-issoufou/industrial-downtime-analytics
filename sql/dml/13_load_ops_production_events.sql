-- ==========================================================
-- Alimentation de la table OPS.production_events
-- depuis STAGING
-- ==========================================================

INSERT INTO ops.production_events (
    event_id,
    hourly_prod_id,
    event_type,
    organ,
    element,
    duration_minutes,
    operator_action,
    escalation,
    comment
)
SELECT DISTINCT
    s.event_id,
    s.hourly_prod_id,
    s.event_type,

    -- Décomposition métier à partir du mock (ex: outfeed_conveyor_failure)
    SPLIT_PART(s.event_type, '_', 1) AS organ,
    SPLIT_PART(s.event_type, '_', 2) AS element,

    s.duration_minutes,

    -- Règle métier simple mais crédible
    CASE 
        WHEN s.event_category = 'technical' THEN 'Intervention opérateur'
        ELSE 'Pause planifiée'
    END AS operator_action,

    -- Règle métier d'escalade
    CASE 
        WHEN s.duration_minutes >= 15 THEN 'SUPERVISOR'
        ELSE 'NONE'
    END AS escalation,

    s.comment

FROM stg.production_events s
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.production_events o
    WHERE o.event_id = s.event_id
);
