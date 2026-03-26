-- ==========================================================
-- Dimension des événements de production
-- Contient la logique métier / classification des événements
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.dim_event (

    -- ======================
    -- Clé analytique surrogée
    -- ======================
    event_key SERIAL PRIMARY KEY,

    -- ======================
    -- Description de l'événement
    -- ======================
    event_type TEXT NOT NULL,       -- nom de l'événement, unique
    cause_category TEXT,            -- ex: Technical, Process, Quality, Organization
    cause_family TEXT,              -- ex: Mechanical, Electrical, Human, Process

    -- ======================
    -- KPI / flags BI
    -- ======================
    severity TEXT,                  -- ex: minor, medium, critical
    business_impact TEXT,           -- ex: low, medium, high
    is_planned BOOLEAN,             -- arrêt planifié ?
    is_technical BOOLEAN,           -- événement technique ?

    -- ======================
    -- Contraintes
    -- ======================
    UNIQUE(event_type)
);

COMMENT ON TABLE dw.dim_event IS
'Dimension analytique décrivant les types d’événements de production et leur classification métier.';