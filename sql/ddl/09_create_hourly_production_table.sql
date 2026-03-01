CREATE TABLE IF NOT EXISTS  ops.hourly_production (
   hourly_prod_id TEXT PRIMARY KEY,

   -- clés métier
   shift_supervision_id TEXT NOT NULL,
   operator_id TEXT NOT NULL,
   team_lead_id TEXT NOT NULL,
   line_id TEXT NOT NULL,

   -- temps
   date DATE NOT NULL,
   session TEXT NOT NULL,
   hour_index INTEGER NOT NULL,
   hour_timestamp TIMESTAMP NOT NULL,

   -- production
   theoretical_production INTEGER NOT NULL,
   actual_production INTEGER NOT NULL,
   non_production_minutes INTEGER NOT NULL,
   explained_minutes INTEGER NOT NULL,
   unexplained_minutes INTEGER NOT NULL,
   reliability_target NUMERIC(5,2) NOT NULL,
   reliability_gap NUMERIC(5,2) NOT NULL,
   reliability_rate NUMERIC(5,2) NOT NULL,
   explained_ratio NUMERIC(5,2) NOT NULL,
   unexplained_ratio NUMERIC(5,2) NOT NULL,
   load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


   FOREIGN KEY (shift_supervision_id) REFERENCES ops.shift_supervision(shift_supervision_id),
   FOREIGN KEY (operator_id) REFERENCES ops.operator(operator_id),
   FOREIGN KEY (team_lead_id) REFERENCES ops.team_lead(team_lead_id),
   FOREIGN KEY (line_id) REFERENCES ops.production_line(line_id)
);
