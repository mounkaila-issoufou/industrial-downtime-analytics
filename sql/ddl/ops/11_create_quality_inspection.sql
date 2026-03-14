CREATE TABLE ops.quality_inspection (

    inspection_id SERIAL PRIMARY KEY,

    hourly_prod_id TEXT NOT NULL,

    inspector_id TEXT,

    inspection_type TEXT,

    inspected_units INTEGER,

    inspection_time TIMESTAMP
);
