DROP TABLE IF EXISTS ops.factory CASCADE;

CREATE TABLE ops.factory (
   factory_id TEXT PRIMARY KEY,
   factory_name TEXT NOT NULL,
   city TEXT,
   country TEXT
);