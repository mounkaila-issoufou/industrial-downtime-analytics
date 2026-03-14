-- ==========================================================
-- Chargement du CSV dans la zone STAGING : shift_operator_assignment
-- ==========================================================

TRUNCATE TABLE stg.shift_operator_assignment;

COPY stg.shift_operator_assignment
FROM STDIN
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);
