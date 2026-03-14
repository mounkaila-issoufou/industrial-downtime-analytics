CREATE TABLE dw.dim_defect (

    defect_key SERIAL PRIMARY KEY,

    defect_category TEXT NOT NULL,
    defect_family TEXT NOT NULL,
    defect_type TEXT NOT NULL,

    severity_level TEXT,

    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);
