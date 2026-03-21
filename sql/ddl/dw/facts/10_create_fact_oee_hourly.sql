CREATE TABLE IF NOT EXISTS dw.fact_oee_hourly (

    time_key INTEGER NOT NULL,
    machine_key INTEGER NOT NULL,
    team_key INTEGER NOT NULL,

    availability FLOAT,
    performance FLOAT,
    quality FLOAT,
    oee FLOAT,

    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_oee PRIMARY KEY (time_key, machine_key, team_key)

)
PARTITION BY RANGE (time_key);
