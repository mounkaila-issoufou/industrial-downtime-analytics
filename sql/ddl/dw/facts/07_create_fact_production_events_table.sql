CREATE TABLE IF NOT EXISTS dw.fact_production_events (

    -- 🔥 IDENTIFIANT UNIQUE (corrigé)
    event_id VARCHAR(50) NOT NULL,

    time_key            INTEGER NOT NULL,
    machine_key         INTEGER NOT NULL,
    team_key            INTEGER NOT NULL,
    organe_element_key  INTEGER NOT NULL,
    event_key           INTEGER NOT NULL,

    duration_minutes    INTEGER NOT NULL,
    severity_score      INTEGER,
    is_recurrent        BOOLEAN,

    is_failure          BOOLEAN,
    is_micro_stop       BOOLEAN,
    is_quality_loss     BOOLEAN,

    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 🔥 FIX ICI
    CONSTRAINT pk_fact_production_events
        PRIMARY KEY (event_id, time_key),

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

    CONSTRAINT fk_fact_event_type
        FOREIGN KEY (event_key)
        REFERENCES dw.dim_event(event_key)

)
PARTITION BY RANGE (time_key);