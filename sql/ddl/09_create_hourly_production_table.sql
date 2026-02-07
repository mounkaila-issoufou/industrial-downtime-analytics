DROP TABLE IF EXISTS ops.hourly_production CASCADE;

CREATE TABLE ops.hourly_production (
   hourly_prod_id TEXT PRIMARY KEY,
   shift_supervision_id TEXT,
   operator_id TEXT,
   team_lead_id TEXT,
   line_id TEXT,
   hour_timestamp TIMESTAMP,
   theoretical_production INTEGER,
   actual_production INTEGER,
   non_production_minutes INTEGER,
   FOREIGN KEY (shift_supervision_id) REFERENCES ops.shift_supervision(shift_supervision_id),
   FOREIGN KEY (operator_id) REFERENCES ops.operator(operator_id),
   FOREIGN KEY (team_lead_id) REFERENCES ops.team_lead(team_lead_id),
   FOREIGN KEY (line_id) REFERENCES ops.production_line(line_id)
);