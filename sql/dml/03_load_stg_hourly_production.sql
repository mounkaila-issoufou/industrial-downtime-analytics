-- ==========================================================
-- Chargement du CSV dans la zone STAGING : hourly_production
-- ==========================================================

TRUNCATE TABLE stg.hourly_production;

COPY stg.hourly_production
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);
