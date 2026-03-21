-- ==========================================================
-- Dimension Équipe / Encadrement
-- Dérivée du contexte managérial des shifts
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.dim_team (
    team_key SERIAL PRIMARY KEY,          -- clé surrogée analytique

    -- Clés métier sources (traçabilité vers le modèle ops)
    team_lead_id TEXT NOT NULL,           -- vient de ops.team_lead


    -- Contexte du shift (utile en analyse)
    session TEXT NOT NULL,                -- MATIN / SOIR / NUIT / SD
    scope_factory_id TEXT,                -- usine supervisée
    scope_workshop_id TEXT,               -- atelier supervisé
    scope_line_id TEXT,                   -- ligne supervisée

    -- Métadonnées de gestion de versions (SCD type 2 léger)
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE dw.dim_team IS
'Dimension équipe : décrit le contexte managérial d’un shift pour analyses BI.';

COMMENT ON COLUMN dw.dim_team.team_key IS
'Clé surrogée analytique pour simplifier les jointures avec les faits.';

COMMENT ON COLUMN dw.dim_team.session IS
'Session de production supervisée (MATIN, SOIR, NUIT, SD).';
