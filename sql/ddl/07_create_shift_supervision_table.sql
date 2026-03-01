CREATE TABLE IF NOT EXISTS  ops.shift_supervision (
   shift_supervision_id TEXT PRIMARY KEY,
   date DATE,
   session TEXT,
   start_time TIME,
   end_time TIME,
   factory_id TEXT,
   workshop_id TEXT,
   line_id TEXT,
   team_lead_id TEXT,
   comment TEXT,
   FOREIGN KEY (factory_id) REFERENCES ops.factory(factory_id),
   FOREIGN KEY (workshop_id) REFERENCES ops.workshop(workshop_id),
   FOREIGN KEY (line_id) REFERENCES ops.production_line(line_id)
);