CREATE TABLE IF NOT EXISTS dw.dim_quality_defect (

    defect_key SERIAL PRIMARY KEY,

    defect_category VARCHAR(30) NOT NULL,
    defect_family VARCHAR(50) NOT NULL,
    defect_type VARCHAR(100) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_defect UNIQUE (
        defect_category,
        defect_family,
        defect_type
    )
);
