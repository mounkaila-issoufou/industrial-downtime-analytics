COPY stg.quality_events (
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
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);