CREATE TABLE ops.quality_event (

    quality_event_id SERIAL PRIMARY KEY,

    inspection_id INTEGER NOT NULL,
    defect_id INTEGER NOT NULL,

    defective_units INTEGER,
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
