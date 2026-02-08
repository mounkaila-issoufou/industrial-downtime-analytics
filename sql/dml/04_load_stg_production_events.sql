-- ==========================================================
-- Chargement du CSV dans la zone STAGING : production_events
-- ==========================================================

TRUNCATE TABLE stg.production_events;

COPY stg.production_events
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);
