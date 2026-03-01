CREATE TABLE IF NOT EXISTS  ops.shift_operator_assignment (
   shift_operator_assignment_id TEXT PRIMARY KEY,
   shift_supervision_id TEXT NOT NULL,
   operator_id TEXT NOT NULL,
   line_id TEXT NOT NULL,
   date DATE NOT NULL,
   session TEXT NOT NULL,
   role TEXT,

   FOREIGN KEY (shift_supervision_id) REFERENCES ops.shift_supervision(shift_supervision_id),
   FOREIGN KEY (operator_id) REFERENCES ops.operator(operator_id),
   FOREIGN KEY (line_id) REFERENCES ops.production_line(line_id)
);
