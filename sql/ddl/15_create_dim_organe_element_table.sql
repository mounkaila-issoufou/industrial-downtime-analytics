-- ==========================================================
-- Dimension Organe / Élément
-- Sert à analyser finement les causes d'arrêts
-- ==========================================================

DROP TABLE IF EXISTS dw.dim_organe_element CASCADE;

CREATE TABLE IF NOT EXISTS dw.dim_organe_element (
    organe_element_key SERIAL PRIMARY KEY,   -- clé surrogée analytique

    -- Clés métier sources (traçabilité vers ops)
    organe TEXT NOT NULL,        -- ex : Emballeuse, Empileur, Encaisseuse
    element TEXT NOT NULL,       -- ex : Porte, Capteur, Trainard

    -- Classification analytique utile pour la BI
    cause_category TEXT NOT NULL,   -- Technique / Opération / Organisation / Qualité
    cause_family TEXT,              -- ex : Mécanique, Électrique, Humain, Process

    -- Métadonnées de chargement
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE dw.dim_organe_element IS
'Dimension analytique décrivant les organes et éléments à l’origine des arrêts.';

COMMENT ON COLUMN dw.dim_organe_element.cause_category IS
'Catégorie principale de perte (Technique, Opération, Organisation, etc.).';

COMMENT ON COLUMN dw.dim_organe_element.cause_family IS
'Sous-classe de la cause (ex : mécanique, électrique, process).';
