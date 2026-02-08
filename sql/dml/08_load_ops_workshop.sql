-- ==========================================================
-- Alimentation de la table OPS.workshop depuis STAGING
-- ==========================================================

INSERT INTO ops.workshop (workshop_id, workshop_name, factory_id)
SELECT DISTINCT
    ss.workshop_id,
    ss.workshop_id       AS workshop_name,   -- proxy simple pour ton mock
    ss.factory_id
FROM stg.shift_supervision ss
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.workshop w
    WHERE w.workshop_id = ss.workshop_id
);
