-- ==========================================================
-- STAGING : hourly_production
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================
DROP TABLE IF EXISTS stg.hourly_production CASCADE;

CREATE TABLE IF NOT EXISTS stg.hourly_production (
    hourly_prod_id VARCHAR(50) PRIMARY KEY,
    date DATE NOT NULL,
    session VARCHAR(10) NOT NULL,
    shift_supervision_id VARCHAR(50) NOT NULL,
    operator_id VARCHAR(20) NOT NULL,
    team_lead_id VARCHAR(20) NOT NULL,
    workshop_id VARCHAR(20) NOT NULL,
    line_id VARCHAR(20) NOT NULL,
    hour_index INTEGER NOT NULL,
    actual_production INTEGER NOT NULL,
    non_production_minutes INTEGER NOT NULL
);

COMMENT ON TABLE stg.hourly_production IS
'Données brutes de production horaire issues du fichier CSV.';

COMMENT ON COLUMN stg.hourly_production.hour_index IS
'Index de l’heure dans le shift (0 à 7).';

COMMENT ON COLUMN stg.hourly_production.actual_production IS
'Production réelle sur l’heure (unités produites).';

COMMENT ON COLUMN stg.hourly_production.non_production_minutes IS
'Minutes sans production sur l’heure (downtime total).';
