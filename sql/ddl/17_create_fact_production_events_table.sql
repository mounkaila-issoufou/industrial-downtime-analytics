-- ==========================================================
-- Fait analytique : événements de production (arrêts, pertes)
-- Grain : 1 ligne = 1 événement d'arrêt
-- ==========================================================
DROP TABLE IF EXISTS dw.fact_production_events CASCADE;

CREATE TABLE IF NOT EXISTS dw.fact_production_events (

    -- Clés étrangères vers les dimensions analytiques
    time_key            INTEGER NOT NULL,   -- quand
    machine_key         INTEGER NOT NULL,   -- où
    team_key            INTEGER NOT NULL,   -- sous quelle équipe
    organe_element_key  INTEGER NOT NULL,   -- quoi / pourquoi

    -- Détail de l'événement
    operator_id         TEXT,               -- optionnel : qui était en poste
    event_type          TEXT NOT NULL,      -- ex: DEFECT, ADJUSTMENT, BREAK, MAINTENANCE
    start_minute        INTEGER,            -- minute de début dans l'heure (0-59)
    duration_minutes    INTEGER NOT NULL,   -- durée de l'arrêt

    -- Métadonnées de traçabilité
    source_event_id     TEXT,               -- id venant du système opérationnel
    load_timestamp      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Contraintes de clé étrangère
    CONSTRAINT fk_time_events
        FOREIGN KEY (time_key) REFERENCES dw.dim_time(time_key),

    CONSTRAINT fk_machine_events
        FOREIGN KEY (machine_key) REFERENCES dw.dim_machine(machine_key),

    CONSTRAINT fk_team_events
        FOREIGN KEY (team_key) REFERENCES dw.dim_team(team_key),

    CONSTRAINT fk_organe_element
        FOREIGN KEY (organe_element_key) 
        REFERENCES dw.dim_organe_element(organe_element_key)
);

COMMENT ON TABLE dw.fact_production_events IS
'Table de faits événementielle pour analyser finement les arrêts de production.';

COMMENT ON COLUMN dw.fact_production_events.duration_minutes IS
'Durée de l’arrêt en minutes, utilisée pour Pareto et analyses de pertes.';

COMMENT ON COLUMN dw.fact_production_events.start_minute IS
'Minute de début dans l’heure (0-59), utile pour analyses temporelles fines.';

COMMENT ON COLUMN dw.fact_production_events.operator_id IS
'Opérateur présent lors de l’événement (optionnel).';
