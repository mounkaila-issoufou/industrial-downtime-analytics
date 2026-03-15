CREATE TABLE IF NOT EXISTS  ops.production_line (
   line_id TEXT PRIMARY KEY,
   machine_name TEXT,
   workshop_id TEXT NOT NULL,
   theoretical_capacity_per_hour INTEGER,
   reliability_target FLOAT,
   line_status TEXT,
   FOREIGN KEY (workshop_id) REFERENCES ops.workshop(workshop_id)
);
