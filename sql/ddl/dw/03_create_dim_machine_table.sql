-- ==========================================================
-- Dimension Machine (usine → atelier → ligne)
-- Dimension centrale du contexte industriel
-- ==========================================================
CREATE TABLE IF NOT EXISTS dw.dim_machine (
    machine_key SERIAL PRIMARY KEY,          -- clé surrogée analytique
    -- Clés métier sources (traçabilité vers le modèle ops)
    line_id  TEXT  NOT NULL,
    factory_id TEXT NOT NULL,
    workshop_id TEXT NOT NULL,

    -- Descriptifs métier (aplatis pour la BI)
    factory_name TEXT NOT NULL,
    workshop_name TEXT NOT NULL,
    machine_name TEXT NOT NULL,
    -- Attributs analytiques utiles
    theoretical_capacity_per_hour INTEGER,
    reliability_target FLOAT,
    line_status TEXT,                        -- RUNNING / STOPPED / MAINTENANCE

    -- Métadonnées de chargement
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE,
    UNIQUE (line_id)
);

COMMENT ON TABLE dw.dim_machine IS
'Dimension machine : vue aplatie usine → atelier → ligne pour analyses BI.';

COMMENT ON COLUMN dw.dim_machine.machine_key IS
'Clé surrogée analytique générée pour simplifier les jointures BI.';

COMMENT ON COLUMN dw.dim_machine.line_status IS
'Statut opérationnel de la ligne (ex: RUNNING, STOPPED, MAINTENANCE).';
