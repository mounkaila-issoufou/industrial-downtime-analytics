-- ==========================================================
-- Alimentation de OPS.production_line depuis STAGING
-- ==========================================================

INSERT INTO ops.production_line (
    line_id,
    machine_name,
    workshop_id,
    theoretical_capacity_per_hour,
    reliability_target,
    line_status
)
SELECT DISTINCT
    ss.line_id                              AS line_id,

    -- Proxy lisible pour ton mock
    'Ligne ' || ss.line_id                  AS machine_name,

    ss.workshop_id                          AS workshop_id,

    -- Hypothèses métier raisonnables pour ton mock
    4800                                    AS theoretical_capacity_per_hour,
    0.92                                    AS reliability_target,
    'ACTIVE'                                AS line_status

FROM stg.shift_supervision ss

WHERE NOT EXISTS (
    SELECT 1
    FROM ops.production_line l
    WHERE l.line_id = ss.line_id
);
