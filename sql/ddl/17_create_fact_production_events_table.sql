-- ==========================================================
-- Table de faits : événements de production
-- Grain : 1 ligne = 1 événement
-- ==========================================================

CREATE TABLE IF NOT EXISTS  dw.fact_production_events (

    -- =========================
    -- Clés dimensionnelles
    -- =========================

    time_key            INTEGER NOT NULL,
    machine_key         INTEGER NOT NULL,
    team_key            INTEGER NOT NULL,
    organe_element_key  INTEGER NOT NULL,

    -- =========================
    -- Mesures
    -- =========================

    duration_minutes    INTEGER NOT NULL,

    -- =========================
    -- Métadonnées
    -- =========================

    load_timestamp      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- =========================
    -- Contraintes
    -- =========================

    CONSTRAINT fk_fact_event_time
        FOREIGN KEY (time_key)
        REFERENCES dw.dim_time(time_key),

    CONSTRAINT fk_fact_event_machine
        FOREIGN KEY (machine_key)
        REFERENCES dw.dim_machine(machine_key),

    CONSTRAINT fk_fact_event_team
        FOREIGN KEY (team_key)
        REFERENCES dw.dim_team(team_key),

    CONSTRAINT fk_fact_event_organe
        FOREIGN KEY (organe_element_key)
        REFERENCES dw.dim_organe_element(organe_element_key),

    CONSTRAINT uq_fact_event UNIQUE (
        time_key,
        machine_key,
        team_key,
        organe_element_key,
        load_timestamp
    )
);

COMMENT ON TABLE dw.fact_production_events IS
'Table de faits détaillant les événements d''arrêt ou de perturbation.';
