-- ==========================================================
-- STAGING : quality_inspection
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================


CREATE TABLE IF NOT EXISTS stg.quality_inspections (

    inspection_id VARCHAR(50) PRIMARY KEY,

    hourly_prod_id VARCHAR(50) NOT NULL,

    inspection_type VARCHAR(20) NOT NULL,

    inspected_units INTEGER NOT NULL CHECK (inspected_units >= 0),


    inspection_date DATE NOT NULL,

    session VARCHAR(10) NOT NULL,

    shift_supervision_id VARCHAR(50) NOT NULL,

    inspector_id VARCHAR(20) NOT NULL,

    workshop_id VARCHAR(20) NOT NULL,

    line_id VARCHAR(20) NOT NULL,


    source_file_name VARCHAR(255),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- COMMENTAIRES
-- ==========================================================

COMMENT ON TABLE stg.quality_inspections IS
'Données brutes d inspections qualité issues du générateur de mock data industriel (zone STAGING).';

COMMENT ON COLUMN stg.quality_inspections.inspection_id IS
'Identifiant unique de l inspection qualité.';

COMMENT ON COLUMN stg.quality_inspections.hourly_prod_id IS
'Référence à l heure de production inspectée.';

COMMENT ON COLUMN stg.quality_inspections.session IS
'Session de production (ex: MORNING / AFTERNOON / NIGHT).';

COMMENT ON COLUMN stg.quality_inspections.shift_supervision_id IS
'Identifiant du superviseur de shift.';

COMMENT ON COLUMN stg.quality_inspections.inspector_id IS
'Identifiant de l inspecteur qualité.';

COMMENT ON COLUMN stg.quality_inspections.workshop_id IS
'Atelier de production.';

COMMENT ON COLUMN stg.quality_inspections.line_id IS
'Ligne de production.';

COMMENT ON COLUMN stg.quality_inspections.inspection_type IS
'Type de contrôle qualité : VISUAL / WEIGHT / LAB / PACKAGING.';

COMMENT ON COLUMN stg.quality_inspections.inspected_units IS
'Nombre d unités inspectées lors du contrôle qualité.';

COMMENT ON COLUMN stg.quality_inspections.source_file_name IS
'Nom du fichier source CSV (traçabilité).';

COMMENT ON COLUMN stg.quality_inspections.load_timestamp IS
'Horodatage de chargement en base (ingestion).';