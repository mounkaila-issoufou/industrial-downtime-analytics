CREATE TABLE ops.quality_defect (

    defect_id SERIAL PRIMARY KEY,

    defect_category VARCHAR(30) NOT NULL,

    defect_family VARCHAR(50) NOT NULL,

    defect_type VARCHAR(100) NOT NULL,

    severity_level VARCHAR(20),

    CONSTRAINT uq_defect UNIQUE (
        defect_category,
        defect_family,
        defect_type
    )
);
