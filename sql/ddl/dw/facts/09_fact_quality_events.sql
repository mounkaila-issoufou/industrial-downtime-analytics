CREATE TABLE IF NOT EXISTS dw.fact_quality_events (

    quality_event_id VARCHAR(50) NOT NULL,

    time_key INTEGER NOT NULL,

    machine_key INTEGER NOT NULL,
    team_key INTEGER NOT NULL,
    defect_key INTEGER NOT NULL,

    defective_units INTEGER NOT NULL,
    scrap_units INTEGER NOT NULL,
    reworked_units INTEGER NOT NULL,

    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- ✅ PK compatible partitionnement
    CONSTRAINT pk_quality_event 
        PRIMARY KEY (quality_event_id, time_key),

    CONSTRAINT fk_time
        FOREIGN KEY (time_key)
        REFERENCES dw.dim_time(time_key),

    CONSTRAINT fk_machine
        FOREIGN KEY (machine_key)
        REFERENCES dw.dim_machine(machine_key),

    CONSTRAINT fk_team
        FOREIGN KEY (team_key)
        REFERENCES dw.dim_team(team_key),

    CONSTRAINT fk_defect
        FOREIGN KEY (defect_key)
        REFERENCES dw.dim_quality_defect(defect_key)

)
PARTITION BY RANGE (time_key);
