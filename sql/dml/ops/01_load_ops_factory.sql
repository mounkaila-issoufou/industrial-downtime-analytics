-- ==========================================================
-- Alimentation de la table OPS.factory depuis STAGING
-- ==========================================================

INSERT INTO ops.factory (factory_id, factory_name, city, country)
SELECT DISTINCT
    ss.factory_id,
    ss.factory_id AS factory_name,
    'UNKNOWN',
    'UNKNOWN'
FROM stg.shift_supervision ss
ON CONFLICT (factory_id)
DO NOTHING;
