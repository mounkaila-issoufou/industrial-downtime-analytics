

COPY stg.quality_inspections (
    inspection_id,
    hourly_prod_id,
    inspection_type,
    inspected_units,
    inspection_date,
    session,
    shift_supervision_id,
    inspector_id,
    workshop_id,
    line_id,
    source_file_name

)
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ','
);
