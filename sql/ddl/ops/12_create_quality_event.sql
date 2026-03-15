CREATE TABLE ops.quality_event (

    quality_event_id VARCHAR(50) PRIMARY KEY,

    inspection_id VARCHAR(50) NOT NULL,

    defect_id INTEGER NOT NULL,

    defective_units INTEGER NOT NULL,

    scrap_units INTEGER,

    reworked_units INTEGER,

    comment TEXT,

    CONSTRAINT fk_inspection
        FOREIGN KEY (inspection_id)
        REFERENCES ops.quality_inspection(inspection_id),

    CONSTRAINT fk_defect
        FOREIGN KEY (defect_id)
        REFERENCES ops.quality_defect(defect_id)
);
