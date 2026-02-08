-- ==========================================================
-- Alimentation de la table OPS.factory depuis STAGING
-- ==========================================================

INSERT INTO ops.factory (factory_id, factory_name, city, country)
SELECT DISTINCT
    ss.factory_id,
    ss.factory_id        AS factory_name,   -- proxy simple dans ton mock
    'UNKNOWN'            AS city,
    'UNKNOWN'            AS country
FROM stg.shift_supervision ss
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.factory f
    WHERE f.factory_id = ss.factory_id
);
