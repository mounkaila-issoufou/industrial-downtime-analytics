INSERT INTO ops.quality_inspection (
    inspection_id,
    hourly_prod_id,
    inspection_date,
    session,
    shift_supervision_id,
    inspector_id,
    workshop_id,
    line_id,
    inspection_type,
    inspected_units
)
SELECT
    s.inspection_id,
    s.hourly_prod_id,
    s.inspection_date,
    s.session,
    s.shift_supervision_id,
    s.inspector_id,
    s.workshop_id,
    s.line_id,
    s.inspection_type,
    s.inspected_units
FROM stg.quality_inspections s
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.quality_inspection o
    WHERE o.inspection_id = s.inspection_id
);
