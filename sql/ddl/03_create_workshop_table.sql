DROP TABLE IF EXISTS ops.workshop CASCADE;

CREATE TABLE ops.workshop (
   workshop_id TEXT PRIMARY KEY,
   workshop_name TEXT NOT NULL,
   factory_id TEXT NOT NULL,
   FOREIGN KEY (factory_id) REFERENCES ops.factory(factory_id)
);
