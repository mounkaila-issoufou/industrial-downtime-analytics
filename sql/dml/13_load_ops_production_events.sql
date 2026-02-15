-- ==========================================================
-- Alimentation de la table OPS.production_events
-- depuis STAGING
-- ==========================================================

INSERT INTO ops.production_events (
    event_id,
    hourly_prod_id,
    event_type,
    event_category,
    organ,
    element,
    operator_action,
    duration_minutes,
    comment
)
SELECT DISTINCT
    s.event_id,
    s.hourly_prod_id,
    s.event_type,
    s.event_category,
    s.organ,
    s.element,
    s.operator_action,
    s.duration_minutes,

    s.comment

FROM stg.production_events s
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.production_events o
    WHERE o.event_id = s.event_id
);
