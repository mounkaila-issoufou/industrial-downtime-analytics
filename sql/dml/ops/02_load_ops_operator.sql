-- ==========================================================
-- Alimentation de OPS.operator
-- Source : STAGING.shift_operator_assignment
-- ==========================================================

INSERT INTO ops.operator (
    operator_id,
    experience_years,
    operator_status
)
SELECT DISTINCT
    s.operator_id,

    -- Hypothèses métier raisonnables pour ton mock
    3 AS experience_years,          -- expérience moyenne
    'ACTIVE' AS operator_status     -- tous actifs par défaut

FROM stg.shift_operator_assignment s

WHERE NOT EXISTS (
    SELECT 1
    FROM ops.operator o
    WHERE o.operator_id = s.operator_id
);
