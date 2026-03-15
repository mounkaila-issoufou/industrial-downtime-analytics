-- ==========================================================
-- Chargement du CSV dans la zone STAGING : shift_supervision
-- ==========================================================

TRUNCATE TABLE stg.shift_supervision;

COPY stg.shift_supervision
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);
