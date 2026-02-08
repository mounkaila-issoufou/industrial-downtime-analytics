-- ==========================================================
-- Alimentation de la dimension TEMPS (DW)
-- Source : ops.hourly_production
-- ==========================================================

INSERT INTO dw.dim_time (
    time_key,
    date,
    year,
    month,
    month_name,
    iso_week,
    day_of_week,
    day_name,
    session,
    hour_index
)
SELECT DISTINCT
    TO_CHAR(h.date, 'YYYYMMDD')::INT * 10 + h.hour_index AS time_key,

    h.date,
    EXTRACT(YEAR FROM h.date)::INT        AS year,
    EXTRACT(MONTH FROM h.date)::INT       AS month,
    TO_CHAR(h.date, 'Month')              AS month_name,
    EXTRACT(WEEK FROM h.date)::INT        AS iso_week,
    EXTRACT(ISODOW FROM h.date)::INT      AS day_of_week,
    TO_CHAR(h.date, 'Day')                AS day_name,

    h.session,
    h.hour_index

FROM ops.hourly_production h
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.dim_time t
    WHERE t.time_key =
          TO_CHAR(h.date, 'YYYYMMDD')::INT * 10 + h.hour_index
);
