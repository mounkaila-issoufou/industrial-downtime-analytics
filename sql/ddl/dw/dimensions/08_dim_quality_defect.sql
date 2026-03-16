CREATE TABLE dw.dim_defect (

    defect_key SERIAL PRIMARY KEY,

    defect_category VARCHAR(30) NOT NULL,

    defect_family VARCHAR(50) NOT NULL,

    defect_type VARCHAR(100) NOT NULL,

    severity_level VARCHAR(20),

    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);
