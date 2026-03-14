-- ==========================================================
-- Chargement du CSV dans la zone STAGING : production_events
-- ==========================================================

TRUNCATE TABLE stg.production_events;

COPY stg.production_events (
    event_id,
    hourly_prod_id,
    event_type,
    event_category,   -- <-- mapping correct
    organ,
    element,
    operator_action,
    duration_minutes,
    comment
)
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);
