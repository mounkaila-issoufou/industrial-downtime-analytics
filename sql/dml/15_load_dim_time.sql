--=============================================================================
-- Script : 15_load_dim_time.sql    
-- Description : Alimentation de la dimension temps (DW) à partir du modèle OPS
-- Source : ops.hourly_production (date + heure)
--=============================================================================


INSERT INTO dw.dim_time (
    time_key,
    date,
    year,
    month,
    month_name,
    iso_week,
    day_of_week,
    day_name,
    hour_of_day,
    session,
    is_weekend
)
SELECT DISTINCT
    (TO_CHAR(h.date, 'YYYYMMDD')::INT * 100 + h.hour_index),
    h.date,
    EXTRACT(YEAR FROM h.date)::INT,
    EXTRACT(MONTH FROM h.date)::INT,
    TO_CHAR(h.date, 'FMMonth'),
    EXTRACT(WEEK FROM h.date)::INT,
    EXTRACT(ISODOW FROM h.date)::INT,
    TO_CHAR(h.date, 'FMDay'),
    h.hour_index,
    h.session,
    (EXTRACT(DOW FROM h.date) IN (0,6))
FROM ops.hourly_production h

ON CONFLICT (time_key) DO NOTHING;
