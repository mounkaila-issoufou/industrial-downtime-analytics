CREATE TABLE IF NOT EXISTS ops.quality_inspection (

    inspection_id VARCHAR(50) PRIMARY KEY,

    hourly_prod_id VARCHAR(50) NOT NULL,

    inspection_date DATE NOT NULL,

    session VARCHAR(10) NOT NULL,

    shift_supervision_id VARCHAR(50) NOT NULL,

    inspector_id VARCHAR(20) NOT NULL,

    workshop_id VARCHAR(20) NOT NULL,

    line_id VARCHAR(20) NOT NULL,

    inspection_type VARCHAR(20) NOT NULL,

    inspected_units INTEGER NOT NULL CHECK (inspected_units >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 🔗 Lien critique vers production
    CONSTRAINT fk_quality_hourly_prod
        FOREIGN KEY (hourly_prod_id)
        REFERENCES ops.hourly_production(hourly_prod_id)
);
