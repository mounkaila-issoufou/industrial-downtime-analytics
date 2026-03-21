INSERT INTO ops.quality_event (
    quality_event_id,
    inspection_id,
    defect_category,
    defect_family,
    defect_type,
    defective_units,
    scrap_units,
    reworked_units,
    comment
)
SELECT
    s.quality_event_id,
    s.inspection_id,
    s.defect_category,
    s.defect_family,
    s.defect_type,
    s.defective_units,
    COALESCE(s.scrap_units, 0),
    COALESCE(s.reworked_units, 0),
    s.comment
FROM stg.quality_events s
WHERE NOT EXISTS (
    SELECT 1
    FROM ops.quality_event o
    WHERE o.quality_event_id = s.quality_event_id
);
