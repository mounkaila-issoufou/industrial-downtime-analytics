-- ==========================================================
-- STAGING : quality_inspection
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================

CREATE TABLE IF NOT EXISTS stg.quality_inspection (

    inspection_id VARCHAR(50) PRIMARY KEY,

    hourly_prod_id VARCHAR(50) NOT NULL,

    inspection_date DATE NOT NULL,

    session VARCHAR(10) NOT NULL,

    shift_supervision_id VARCHAR(50) NOT NULL,

    inspector_id VARCHAR(20) NOT NULL,

    workshop_id VARCHAR(20) NOT NULL,

    line_id VARCHAR(20) NOT NULL,

    inspection_type VARCHAR(20) NOT NULL,

    inspected_units INTEGER NOT NULL

);

COMMENT ON TABLE stg.quality_inspection IS
'Données brutes d inspections qualité issues du générateur de mock data industriel.';

COMMENT ON COLUMN stg.quality_inspection.hourly_prod_id IS
'Référence à l heure de production inspectée.';

COMMENT ON COLUMN stg.quality_inspection.inspection_type IS
'Type de contrôle qualité : VISUAL / WEIGHT / LAB / PACKAGING.';

COMMENT ON COLUMN stg.quality_inspection.inspected_units IS
'Nombre d unités inspectées lors du contrôle qualité.';
