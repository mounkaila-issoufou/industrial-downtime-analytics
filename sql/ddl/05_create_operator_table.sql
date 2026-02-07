DROP TABLE IF EXISTS ops.operator CASCADE;

CREATE TABLE ops.operator (
   operator_id TEXT PRIMARY KEY,
   experience_years INTEGER,
   operator_status TEXT
);