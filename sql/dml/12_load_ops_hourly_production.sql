-- ==========================================================
-- LOAD OPS.hourly_production
-- Source : STG.hourly_production
-- Vérification des clés métier
-- ==========================================================

INSERT INTO ops.hourly_production (
    hourly_prod_id,
    shift_supervision_id,
    operator_id,
    team_lead_id,
    line_id,
    date,
    session,
    hour_index,
    hour_timestamp,
    theoretical_production,
    actual_production,
    non_production_minutes,
    explained_minutes,
    unexplained_minutes,
    reliability_rate,
    explained_ratio,
    unexplained_ratio,
    load_timestamp
)

SELECT
    s.hourly_prod_id,
    s.shift_supervision_id,
    s.operator_id,
    s.team_lead_id,
    s.line_id,
    s.date,
    s.session,
    s.hour_index,

    (s.date::timestamp + (s.hour_index || ' hour')::interval),

    s.theoretical_production,
    s.actual_production,
    s.non_production_minutes,
    s.explained_minutes,
    s.unexplained_minutes,
    s.reliability_rate,
    s.explained_ratio,
    s.unexplained_ratio,
    CURRENT_TIMESTAMP

FROM stg.hourly_production s

-- Vérification des clés métier
INNER JOIN ops.shift_supervision ss
    ON ss.shift_supervision_id = s.shift_supervision_id

INNER JOIN ops.operator o
    ON o.operator_id = s.operator_id

INNER JOIN ops.team_lead tl
    ON tl.team_lead_id = s.team_lead_id

INNER JOIN ops.production_line pl
    ON pl.line_id = s.line_id

ON CONFLICT (hourly_prod_id)
DO NOTHING;
