DROP TABLE IF EXISTS ops.production_events CASCADE;

CREATE TABLE ops.production_events (
   event_id TEXT PRIMARY KEY,
   hourly_prod_id TEXT,
   event_type TEXT,
   organ TEXT,
   element TEXT,
   duration_minutes INTEGER,
   operator_action TEXT,
   escalation TEXT,
   comment TEXT,
   FOREIGN KEY (hourly_prod_id) REFERENCES ops.hourly_production(hourly_prod_id)
);