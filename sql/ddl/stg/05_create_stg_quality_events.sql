-- ==========================================================
-- STAGING : quality_events
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================

CREATE TABLE IF NOT EXISTS stg.quality_events (

    quality_event_id VARCHAR(50) PRIMARY KEY,

    inspection_id VARCHAR(50) NOT NULL,

    defect_category VARCHAR(30) NOT NULL,

    defect_family VARCHAR(50) NOT NULL,

    defect_type VARCHAR(100) NOT NULL,

    defective_units INTEGER NOT NULL CHECK (defective_units >= 0),

    scrap_units INTEGER CHECK (scrap_units >= 0),

    reworked_units INTEGER CHECK (reworked_units >= 0),

    comment TEXT,

    source_file_name VARCHAR(255),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
