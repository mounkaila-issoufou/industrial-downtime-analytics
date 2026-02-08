-- ==========================================================
-- Alimentation de la dimension ÉQUIPE (DW)
-- Source : ops.shift_supervision + ops.shift_operator_assignment
-- ==========================================================

INSERT INTO dw.dim_team (
    team_key,
    team_lead_id,
    operator_id,
    role,
    valid_from,
    is_current
)
SELECT DISTINCT
    -- Clé analytique stable par binôme (chef + opérateur)
    ss.team_lead_id || '_' || soa.operator_id AS team_key,

    ss.team_lead_id,
    soa.operator_id,

    CASE 
        WHEN ss.team_lead_id = soa.operator_id THEN 'TEAM_LEAD'
        ELSE 'OPERATOR'
    END AS role,

    CURRENT_TIMESTAMP AS valid_from,
    TRUE AS is_current

FROM ops.shift_supervision ss
JOIN ops.shift_operator_assignment soa
  ON ss.shift_supervision_id = soa.shift_supervision_id

WHERE NOT EXISTS (
    SELECT 1
    FROM dw.dim_team t
    WHERE t.team_key =
          ss.team_lead_id || '_' || soa.operator_id
);
