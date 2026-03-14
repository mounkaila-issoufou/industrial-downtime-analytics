-- ==========================================================
-- Alimentation de la table OPS.shift_operator_assignment
-- depuis STAGING
-- ==========================================================

INSERT INTO ops.shift_operator_assignment (
    shift_operator_assignment_id,
    shift_supervision_id,
    operator_id,
    line_id,
    date,
    session
)
SELECT DISTINCT
    s.shift_operator_assignment_id,
    s.shift_supervision_id,
    s.operator_id,
    s.line_id,
    s.date,
    s.session
FROM stg.shift_operator_assignment s
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.shift_operator_assignment o
    WHERE o.shift_operator_assignment_id = s.shift_operator_assignment_id
);
