-- ==========================================================
-- STAGING : shift_supervision
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================

DROP TABLE IF EXISTS stg.shift_supervision CASCADE;

CREATE TABLE IF NOT EXISTS stg.shift_supervision (
    shift_supervision_id VARCHAR(50) PRIMARY KEY,
    date DATE NOT NULL,
    session VARCHAR(10) NOT NULL,
    factory_id VARCHAR(20) NOT NULL,
    workshop_id VARCHAR(20) NOT NULL,
    line_id VARCHAR(20) NOT NULL,
    team_lead_id VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

COMMENT ON TABLE stg.shift_supervision IS
'Données brutes de supervision des shifts issues du fichier CSV.';

COMMENT ON COLUMN stg.shift_supervision.session IS
'Session de production : MATIN / SOIR / NUIT / SD';
