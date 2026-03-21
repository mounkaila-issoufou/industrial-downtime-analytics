CREATE TABLE IF NOT EXISTS ops.quality_event (

    quality_event_id VARCHAR(50) PRIMARY KEY,

    inspection_id VARCHAR(50) NOT NULL,

    defect_category VARCHAR(30) NOT NULL,

    defect_family VARCHAR(50) NOT NULL,

    defect_type VARCHAR(100) NOT NULL,

    defective_units INTEGER NOT NULL CHECK (defective_units >= 0),

    scrap_units INTEGER DEFAULT 0 CHECK (scrap_units >= 0),

    reworked_units INTEGER DEFAULT 0 CHECK (reworked_units >= 0),

    comment TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 🔗 Lien inspection
    CONSTRAINT fk_quality_inspection
        FOREIGN KEY (inspection_id)
        REFERENCES ops.quality_inspection(inspection_id)
);
