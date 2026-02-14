-- ==========================================================
-- Dimension temps - socle temporel du modèle analytique
-- ==========================================================
DROP TABLE IF EXISTS dw.dim_time CASCADE;

CREATE TABLE IF NOT EXISTS dw.dim_time (
    time_key            INTEGER PRIMARY KEY,   -- ex: 2024011009 (YYYYMMDDHH)
    date                DATE NOT NULL,
    year                INTEGER NOT NULL,
    month               INTEGER NOT NULL,
    month_name          TEXT NOT NULL,
    iso_week            INTEGER NOT NULL,
    day_of_week         INTEGER NOT NULL,      -- 1 = lundi ... 7 = dimanche
    day_name            TEXT NOT NULL,
    hour_of_day         INTEGER NOT NULL,      -- 0 à 23
    session             TEXT NOT NULL,         -- MATIN / SOIR / NUIT / SD
    is_weekend          BOOLEAN NOT NULL
);

COMMENT ON TABLE dw.dim_time IS 
'Dimension temps unifiée pour analyses horaires, journalières et temporelles.';

COMMENT ON COLUMN dw.dim_time.time_key IS 
'Clé surrogée de la dimension temps au grain horaire (YYYYMMDDHH).';

COMMENT ON COLUMN dw.dim_time.session IS 
'Session de production : MATIN, SOIR, NUIT ou SD (service de jour).';
