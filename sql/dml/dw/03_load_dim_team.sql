INSERT INTO dw.dim_team (
    team_lead_id,
    session,
    scope_factory_id,
    scope_workshop_id,
    scope_line_id,
    valid_from,
    is_current
)

SELECT DISTINCT
    ss.team_lead_id,
    ss.session,
    ss.factory_id,
    ss.workshop_id,
    ss.line_id,
    CURRENT_TIMESTAMP,
    TRUE

FROM ops.shift_supervision ss

ON CONFLICT DO NOTHING;
