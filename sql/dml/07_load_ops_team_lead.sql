-- ==========================================================
-- Alimentation de OPS.team_lead
-- Source : STAGING.shift_supervision
-- ==========================================================

INSERT INTO ops.team_lead (
    team_lead_id,
    scope
)
SELECT DISTINCT
    s.team_lead_id,

    -- Règle métier simple et crédible pour ton mock
    'LINE_MANAGER' AS scope

FROM stg.shift_supervision s

WHERE NOT EXISTS (
    SELECT 1
    FROM ops.team_lead t
    WHERE t.team_lead_id = s.team_lead_id
);
