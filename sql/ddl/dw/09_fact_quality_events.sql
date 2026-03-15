CREATE TABLE dw.fact_quality_events (

    time_key INTEGER NOT NULL,

    machine_key INTEGER NOT NULL,

    team_key INTEGER NOT NULL,

    defect_key INTEGER NOT NULL,

    inspected_units INTEGER,

    defective_units INTEGER,

    scrap_units INTEGER,

    reworked_units INTEGER,

    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

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
        REFERENCES dw.dim_defect(defect_key)
);
