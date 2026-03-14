CREATE TABLE ops.quality_defect (

    defect_id SERIAL PRIMARY KEY,

    defect_category TEXT NOT NULL,
    defect_family TEXT NOT NULL,
    defect_type TEXT NOT NULL,

    severity_level TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
