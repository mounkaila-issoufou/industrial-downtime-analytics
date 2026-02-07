DROP TABLE IF EXISTS ops.shift_operator_assignment CASCADE;

CREATE TABLE ops.shift_operator_assignment (
   shift_operator_assignment_id TEXT PRIMARY KEY,
   shift_supervision_id TEXT,
   operator_id TEXT,
   role TEXT,
   FOREIGN KEY (shift_supervision_id) REFERENCES ops.shift_supervision(shift_supervision_id),
   FOREIGN KEY (operator_id) REFERENCES ops.operator(operator_id)
);