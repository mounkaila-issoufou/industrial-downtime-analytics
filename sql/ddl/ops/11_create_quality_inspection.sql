CREATE TABLE ops.quality_inspection (

    inspection_id VARCHAR(50) PRIMARY KEY,

    hourly_prod_id VARCHAR(50) NOT NULL,

    inspector_id VARCHAR(20),

    inspection_type VARCHAR(20),

    inspected_units INTEGER,

    inspection_timestamp TIMESTAMP,

    CONSTRAINT fk_hourly_prod
        FOREIGN KEY (hourly_prod_id)
        REFERENCES ops.hourly_production(hourly_prod_id)
);
