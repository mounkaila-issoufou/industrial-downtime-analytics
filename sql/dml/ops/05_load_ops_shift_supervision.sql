-- ==========================================================
-- Alimentation de la table OPS.shift_supervision depuis STAGING
-- ==========================================================

INSERT INTO ops.shift_supervision (
    shift_supervision_id,
    date,
    session,
    factory_id,
    workshop_id,
    line_id,
    team_lead_id,
    start_time,
    end_time
)
SELECT DISTINCT
    ss.shift_supervision_id,
    ss.date,
    ss.session,
    ss.factory_id,
    ss.workshop_id,
    ss.line_id,
    ss.team_lead_id,
    ss.start_time,
    ss.end_time
FROM stg.shift_supervision ss
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.shift_supervision o
    WHERE o.shift_supervision_id = ss.shift_supervision_id
);
